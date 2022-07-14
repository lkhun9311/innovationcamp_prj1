from bson import ObjectId
from pymongo import MongoClient
import jwt
import datetime
import hashlib
from flask import Flask, render_template, jsonify, request, redirect, url_for, flash
from datetime import datetime, timedelta

from werkzeug.utils import secure_filename
import pafy

app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config['UPLOAD_FOLDER'] = "./static/profile_pics"
app.secret_key = 'SPARTA'

SECRET_KEY = 'SPARTA'

# mongoDB에 연결하려면 <id>와 <password> 입력 필요
# client = MongoClient('mongodb+srv://<아이디>:<비밀번호>!@cluster0.zykagbk.mongodb.net/?retryWrites=true&w=majority', 27017)
client = MongoClient('mongodb+srv://test:dpfehfkeh11!@cluster0.zykagbk.mongodb.net/?retryWrites=true&w=majority', 27017,
                     username="test", password="dpfehfkeh11!")
db = client.cafejoa

@app.route('/')
def home():
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        user_info = db.users.find_one({"username": payload["id"]})
        cafes = list(db.cafes.find({}, {'id': False}))
        reversed_cafes = cafes[::-1]
        print(len(cafes))
        print(user_info)

        return render_template('index.html', cafes=reversed_cafes, user_info=user_info)
    except jwt.ExpiredSignatureError:
        return redirect(url_for("login", msg="로그인 시간이 만료되었습니다."))
    except jwt.exceptions.DecodeError:
        return redirect(url_for("login", msg="로그인 정보가 존재하지 않습니다."))

@app.route('/login')
def login():
    msg = request.args.get("msg")
    return render_template('login.html', msg=msg)

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
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256').decode('utf-8')

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
        "profile_name": username_receive,  # 프로필 이름 기본값은 유저 아이디
        "profile_pic": "profile_placeholder.png",  # 프로필 사진 파일 이름
        "profile_pic_real": "profile_pics/profile_placeholder.png"  # 프로필 사진 real path
    }
    db.users.insert_one(doc)
    return jsonify({'result': 'success'})

@app.route('/sign_up/check_up', methods=['POST'])
def check_up():
    username_receive = request.form['username_give']
    exists = bool(db.users.find_one({"username": username_receive}))
    return jsonify({'result': 'success', 'exists': exists})

@app.route('/user/<username>')
def user(username):
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        status = (username == payload["id"])  # 내 프로필이면 True, 다른 사람 프로필 페이지면 False

        user_info = db.users.find_one({"username": username}, {"_id": False})
        return render_template('user.html', user_info=user_info, status=status)
    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return redirect(url_for("home"))

@app.route('/update_profile', methods=['POST'])
def save_img():
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        username = payload["id"]
        name_receive = request.form["name_give"]
        new_doc = {
            "profile_name": name_receive
        }
        if 'file_give' in request.files:
            file = request.files["file_give"]
            filename = secure_filename(file.filename)
            extension = filename.split(".")[-1]
            file_path = f"profile_pics/{username}.{extension}"
            file.save("./static/" + file_path)
            new_doc["profile_pic"] = filename
            new_doc["profile_pic_real"] = file_path
        db.users.update_one({'username': payload['id']}, {'$set': new_doc})
        return jsonify({"result": "success", 'msg': '프로필 수정 완료'})
    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return redirect(url_for("home"))

@app.route('/user/<username>/resign', methods=['POST'])
def resign_user(username):
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        username = payload["id"]
        db.users.delete_one({'username': username})
        return jsonify({"result": "success", 'msg': '회원탈퇴 완료'})
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
            "username": user_info["username"],  # 작성자
            "cafe_name": cafename_receive,  # 카페 이름
            "cafe_address": cafeaddress_receive,  # 카페 주소
            "cafe_tel": cafetel_receive,  # 카페 전화번호
            "cafe_open_hours": cafeopenhours_receive,  # 카페 운영시간
            "cafe_image_pic": "",  # 카페 이미지
            "cafe_image_pic_real": "",  # 카페 이미지 path
            "profile_pic_real": user_info["profile_pic_real"],  # 사용자 이미지 path
            "date": date_receive  # 포스팅 날짜
        }
        insert_one = db.cafes.insert_one(doc)
        # print(insert_one._InsertOneResult__inserted_id) # 방금 저장된 id
        # 게시글 id를 img 이름으로 저장하여 유일성 만족. (이미지 수정시 자동 덮어쓰기되어 수정)
        cafe_image_name = insert_one._InsertOneResult__inserted_id

        img_doc = {
            "cafe_image_pic": "default.jpg",  # 카페 이미지
            "cafe_image_pic_real": "default.jpg",  # 카페 이미지 path
        }
        # 카페 이미지 파일 존재시 처리
        if 'cafeimage_give' in request.files:
            file = request.files["cafeimage_give"]
            print(file, file.filename)
            filename = secure_filename(file.filename)
            extension = filename.split(".")[-1]
            file_path = f"cafe_image_pics/{cafe_image_name}.{extension}"
            file.save("./static/" + file_path)
            img_doc["cafe_image_pic"] = cafename_receive + "." + extension
            img_doc["cafe_image_pic_real"] = file_path

        # db에서 기존에 저장된 id값에 img 관련 수정
        db.cafes.update_one({'_id': cafe_image_name}, {'$set': img_doc})

        return jsonify({"result": "success", 'msg': '포스팅 성공'})
    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return redirect(url_for("home"))

@app.route("/get/cafes", methods=['GET'])
def get_cafes():
    token_receive = request.cookies.get('mytoken')
    number = int(request.args.get("number"))
    print(number)
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        cafes = list(db.cafes.find({}).sort("date", -1).limit(number))
        # 포스팅 목록 받아오기
        for cafe in cafes:
            cafe["_id"] = str(cafe["_id"])
            # 사진 관련 수정 필요
            # 좋아요 하트 관련 추후 수정
            # cafe["count_heart"] = db.likes.count_documents({"post_id": post["_id"], "type": "heart"})
            # cafe["heart_by_me"] = bool(
            #     db.likes.find_one({"cafe_id": cafe["_id"], "type": "heart", "username": payload['id']}))

        print(cafes)
        return jsonify({"result": "success", "msg": "포스팅을 가져왔습니다.", "cafes": cafes})
    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return redirect(url_for("home"))


@app.route("/cafe/update", methods=['GET'])
def cafe_update():
    token_receive = request.cookies.get('mytoken')
    cafe_id = request.args.get("cafe_id")
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        user_info = db.users.find_one({"username": payload["id"]})
        cafe = db.cafes.find_one({"_id": ObjectId(cafe_id)})

        return render_template('update_cafe.html', user_info=user_info, cafe=cafe)
    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return redirect(url_for("home"))


@app.route("/cafe/update", methods=['POST'])
def cafe_update_post():
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        user_info = db.users.find_one({"username": payload["id"]})
        cafe_id = request.form["cafeid_give"]
        cafename_receive = request.form["cafename_give"]
        cafeaddress_receive = request.form["cafeaddress_give"]
        cafetel_receive = request.form["cafetel_give"]
        cafeopenhours_receive = request.form["cafeopenhours_give"]
        date_receive = request.form["date_give"]
        doc = {
            "cafe_name": cafename_receive,  # 카페 이름
            "cafe_address": cafeaddress_receive,  # 카페 주소
            "cafe_tel": cafetel_receive,  # 카페 전화번호
            "cafe_open_hours": cafeopenhours_receive,  # 카페 운영시간
            "profile_pic_real": user_info["profile_pic_real"],  # 사용자 이미지 path
            "date": date_receive  # 포스팅 날짜
        }
        # 카페 이미지 파일 존재시 처리
        if 'cafeimage_give' in request.files:
            file = request.files["cafeimage_give"]
            print(file, file.filename)
            filename = secure_filename(file.filename)
            extension = filename.split(".")[-1]
            file_path = f"cafe_image_pics/{cafe_id}.{extension}"
            file.save("./static/" + file_path)
            doc["cafe_image_pic"] = cafename_receive + "." + extension
            doc["cafe_image_pic_real"] = file_path

        # 수정하기
        db.cafes.update_one({'_id': ObjectId(cafe_id)}, {'$set': doc})

        return jsonify({"result": "success", 'msg': '카페 수정 성공'})
    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return redirect(url_for("home"))


@app.route("/cafe/delete", methods=['get'])
def cafe_delete():
    token_receive = request.cookies.get('mytoken')
    cafe_id = request.args.get("cafe_id")
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        user_info = db.users.find_one({"username": payload["id"]})
        username_token = user_info["username"]
        cafe_info = db.cafes.find_one({'_id': ObjectId(cafe_id)})
        username_post = cafe_info["username"]

        # token으로 조회한 username과 글 id로 조회한 username이 같을 때 삭제
        if username_token == username_post:
            print("삭제 성공")
            db.cafes.delete_one({'_id': ObjectId(cafe_id)})
        else:
            flash('카페 삭제 실패')
            return redirect(url_for("home"))

        flash('카페 삭제 성공')
        return redirect(url_for("home"))
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

@app.route("/cafemusic/accept", methods=["POST"])
def cafemusic_post():
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        username = payload["id"]

        url_receive = request.form['url_give']
        embed = url_receive.replace(url_receive.split('/')[-1][0:8], 'embed/')
        video = pafy.new(url_receive)
        title = video.title
        view = video.viewcount
        author = video.author
        print(title, view, author)
        doc = {
            'username': username,
            'embed': embed,
            'url': url_receive,
            'title': title,
            'view': view,
            'author': author
        }
        db.cafemusic.insert_one(doc)
        return jsonify({"result": "success", 'msg': 'cafe music 포스팅 완료'})
    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return redirect(url_for("home"))

@app.route("/cafemusic/accept", methods=["GET"])
def cafemusic_get():
    cafemusic_list = list(db.cafemusic.find({}, {'_id': False}))
    return jsonify({'cafemusic_list': cafemusic_list})

@app.route("/mycafemusic/accept", methods=["GET"])
def mycafemusic_get():
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        mycafemusic_list = list(db.cafemusic.find({'username': payload["id"]},{'_id':False}))
        return jsonify({'mycafemusic_list': mycafemusic_list})
    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return redirect(url_for("home"))

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)