$(document).ready(function (){
    mycafemusic_get()
})

function update_profile() {
    let name = $('#input-name').val()
    let file = $('#input-pic')[0].files[0]
    let form_data = new FormData()
    form_data.append("file_give", file)
    form_data.append("name_give", name)
    console.log(name, file, form_data)

    $.ajax({
        type: "POST",
        url: "/update_profile",
        data: form_data,
        cache: false,
        contentType: false,
        processData: false,
        success: function (response) {
            if (response["result"] == "success") {
                alert(response["msg"])
                window.location.reload()

            }
        }
    });
}

function sign_out() {
    $.removeCookie('mytoken', {path: '/'});
    alert('로그아웃')
    window.location.href = "/login"
}

function resign_user() {
    $.removeCookie('mytoken', {path: '/user/<username>/resign'});
    $.ajax({
        type: "POST",
        url: "/user/<username>/resign",
        data: {},
        cache: false,
        contentType: false,
        processData: false,
        success: function (response) {
            if (response["result"] == "success") {
                alert(response["msg"])
                window.location.href = "/login"
            }
        }
    });
}

function mycafemusic_get() {
    $.ajax({
        type: 'GET',
        url: '/mycafemusic/accept',
        success: function (response) {
            rows = response['mycafemusic_list']
            for (i = 0; i < rows.length; i++) {
                let title = rows[i]['title']
                let view = rows[i]['view']
                let embed = rows[i]['embed']
                let author = rows[i]['author']
                let temp_html = `<div class="col">
                                       <div class="card h-100" style="height: 275px">
                                        <iframe width="100%"  src="${embed}" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
            <div class="card-body">
                <h5 class="card-title">${title}</h5>
                <p>&nbsp<i class="fa fa-youtube-play" aria-hidden="true"></i>조회수 &nbsp <span>${view}</span>회</p>
                <p>&nbsp<i class="fa fa-user" aria-hidden="true" style="margin: 1px 3px 0px 2px"></i>작성자 &nbsp <span>${author}</span></p>
                </div>
        </div>
    </div>`
                $('#cards-box2').append(temp_html)
            }
        }

    })
}