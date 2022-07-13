from pymongo import MongoClient
import jwt
import datetime
import hashlib
from flask import Flask, render_template, jsonify, request, redirect, url_for
from datetime import datetime, timedelta

from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config['UPLOAD_FOLDER'] = "./static/profile_pics"

SECRET_KEY = 'SPARTA'

# mongoDB에 연결하려면 <id>와 <password> 입력 필요
client = MongoClient('mongodb+srv://<아이디>:<비밀번호>!@cluster0.zykagbk.mongodb.net/?retryWrites=true&w=majority', 27017)
db = client.cafejoa


@app.route('/')
def home():
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])

        return render_template('index.html')
    except jwt.ExpiredSignatureError:
        return redirect(url_for("login", msg="로그인 시간이 만료되었습니다."))
    except jwt.exceptions.DecodeError:
        return redirect(url_for("login", msg="로그인 정보가 존재하지 않습니다."))


@app.route('/login')
def login():
    msg = request.args.get("msg")
    return render_template('login.html', msg=msg)


@app.route('/user/<username>')
def user(username):
    # 각 사용자의 프로필과 글을 모아볼 수 있는 공간
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        status = (username == payload["id"])  # 내 프로필이면 True, 다른 사람 프로필 페이지면 False

        user_info = db.users.find_one({"username": username}, {"_id": False})
        return render_template('user.html', user_info=user_info, status=status)
    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return redirect(url_for("home"))


@app.route('/sign_in', methods=['POST'])
def sign_in():
    # 로그인
    username_receive = request.form['username_give']
    password_receive = request.form['password_give']

    pw_hash = hashlib.sha256(password_receive.encode('utf-8')).hexdigest()
    result = db.users.find_one({'username': username_receive, 'password': pw_hash})

    if result is not None:
        payload = {
         'id': username_receive,
         'exp': datetime.utcnow() + timedelta(seconds=60 * 60 * 24)  # 로그인 24시간 유지
        }
        # token = jwt.encode(payload, SECRET_KEY, algorithm='HS256').decode('utf-8')
        # 버전이 상향되어 .decode('utf-8') 생략 가능
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')

        return jsonify({'result': 'success', 'token': token})
    # 찾지 못하면
    else:
        return jsonify({'result': 'fail', 'msg': '아이디/비밀번호가 일치하지 않습니다.'})


@app.route('/sign_up/save', methods=['POST'])
def sign_up():
    username_receive = request.form['username_give']
    password_receive = request.form['password_give']
    password_hash = hashlib.sha256(password_receive.encode('utf-8')).hexdigest()
    userrealname_receive = request.form['userrealname_give']
    age_receive = request.form['age_give']
    # gender_receive = request.form['gender_option']
    gender_receive = request.form['gender_give']
    doc = {
        "username": username_receive,  # 아이디
        "password": password_hash,  # 비밀번호
        "userrealname": userrealname_receive,  # 유저 실제 이름
        "gender": gender_receive,  # 유저 성별
        "age": age_receive,  # 유저 나이
        "profile_name": username_receive,  # 프로필 이름 기본값은 아이디
        "profile_pic": "",  # 프로필 사진 파일 이름
        "profile_pic_real": "profile_pics/profile_placeholder.png"  # 프로필 사진 기본 이미지
    }
    db.users.insert_one(doc)
    return jsonify({'result': 'success'})


@app.route('/sign_up/check_up', methods=['POST'])
def check_up():
    username_receive = request.form['username_give']
    exists = bool(db.users.find_one({"username": username_receive}))
    return jsonify({'result': 'success', 'exists': exists})


@app.route('/update_profile', methods=['POST'])
def save_img():
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        return jsonify({"result": "success", 'msg': '프로필을 업데이트했습니다.'})
    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return redirect(url_for("home"))


@app.route('/postingCafe', methods=['POST'])
def posting():
    token_receive = request.cookies.get('mytoken')

    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        # 포스팅하기
        user_info = db.users.find_one({"username": payload["id"]})
        cafename_receive = request.form["cafename_give"]
        cafeaddress_receive = request.form["cafeaddress_give"]
        cafetel_receive = request.form["cafetel_give"]
        cafeopenhours_receive = request.form["cafeopenhours_give"]
        date_receive = request.form["date_give"]
        doc = {
            "username": user_info["username"],
            "cafe_name": cafename_receive,
            "cafe_address": cafeaddress_receive,
            "cafe_tel": cafetel_receive,
            "cafe_open_hours": cafeopenhours_receive,
            "cafe_image_pic": "",
            "cafe_image_pic_real": "",
            "date": date_receive
        }
        # 카페 이미지 파일 존재시 처리
        # 추후에 ec2 local에 저장하고 s3로 url만 저장하도록 변경 해야할지 의논 필요.
        # 그리고 각 카페 후기 게시글에 대한 넘버링 전략을 세워야함.
        if 'cafeimage_give' in request.files:
            file = request.files["cafeimage_give"]
            print(file, file.filename)
            filename = secure_filename(file.filename)
            extension = filename.split(".")[-1]
            file_path = f"cafe_image_pics/{cafename_receive}.{extension}"
            file.save("./static/" + file_path)
            doc["cafe_image_pic"] = cafename_receive + "." + extension
            doc["cafe_image_pic_real"] = file_path

        print(doc)
        db.cafes.insert_one(doc)
        return jsonify({"result": "success", 'msg': '포스팅 성공'})
    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return redirect(url_for("home"))


@app.route("/get/cafes", methods=['GET'])
def get_cafes():
    token_receive = request.cookies.get('mytoken')
    print(token_receive)
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        cafes = list(db.cafes.find({}).sort("date", -1).limit(24))
        # 포스팅 목록 받아오기
        for cafe in cafes:
            cafe["_id"] = str(cafe["_id"])
            # 좋아요 하트 관련 추후 수정
            # cafe["count_heart"] = db.likes.count_documents({"post_id": post["_id"], "type": "heart"})
            # cafe["heart_by_me"] = bool(
            #     db.likes.find_one({"cafe_id": cafe["_id"], "type": "heart", "username": payload['id']}))

        print(cafes)
        return jsonify({"result": "success", "msg": "포스팅을 가져왔습니다.", "cafes": cafes})
    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return redirect(url_for("home"))


# @app.route('/update_like', methods=['POST'])
# def update_like():
#     token_receive = request.cookies.get('mytoken')
#     try:
#         payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
#         # 좋아요 수 변경
#         user_info = db.users.find_one({"username": payload["id"]})
#         post_id_receive = request.form["post_id_give"]
#         type_receive = request.form["type_give"]
#         action_receive = request.form["action_give"]
#         doc = {
#             "post_id": post_id_receive,
#             "username": user_info["username"],
#             "type": type_receive
#         }
#         if action_receive == "like":
#             db.likes.insert_one(doc)
#         else:
#             db.likes.delete_one(doc)
#         count = db.likes.count_documents({"post_id": post_id_receive, "type": type_receive})
#         return jsonify({"result": "success", 'msg': 'updated', "count": count})
#     except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
#         return redirect(url_for("home"))


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
