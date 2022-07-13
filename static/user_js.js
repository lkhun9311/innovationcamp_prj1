// $(document).ready(function (){
//     get_posts('{{user_info.username');
// })

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