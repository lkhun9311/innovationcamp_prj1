// 상시 제이쿼리
$(function () {
    // 모달 창에 이미지 파일 삽입되면 감지하는 이벤트 리스너
    $('#input-pic').on("change", function (event) {
        // 이미지 미리보기도 가능
        var file = event.target.files[0];

        var reader = new FileReader();
        reader.onload = function(e) {
            $("#preview").attr("src", e.target.result);
        }
        reader.readAsDataURL(file);

        $('#file-name').removeClass('is-hidden')
        // console.log(event.target.files[0]) // file check
        $('#file-name').text(event.target.files[0]["name"])
    });
});

function post() {
    let cafeImage = $('#input-pic')[0].files[0]
    let cafeName = $("#cafeName").val()
    let cafeAddress = $("#cafeAddress").val()
    let cafeTel = $("#cafeTel").val()
    let cafeOpenHours = $("#textarea-post").val()
    let today = new Date().toISOString()
    let form_data = new FormData()
    form_data.append("cafeimage_give", cafeImage)
    form_data.append("cafename_give", cafeName)
    form_data.append("cafeaddress_give", cafeAddress)
    form_data.append("cafetel_give", cafeTel)
    form_data.append("cafeopenhours_give", cafeOpenHours)
    form_data.append("date_give", today)
    console.log(form_data)
    $.ajax({
        type: "POST",
        url: "/postingCafe",
        data: form_data,
        cache: false,
        contentType: false,
        processData: false,
        success: function (response) {
            $("#modal-post").removeClass("is-active")
            console.log(response["id"])
            window.location.reload()
        }
    })
}

function get_cafes(username, number) {
    $("#card-box").empty()
    if (username == undefined) {
        username = ""
    }
    $.ajax({
        type: "GET",
        url: `/get/cafes?number=${number}`,
        data: {},
        success: function (response) {
            if (response["result"] == "success") {
                console.log(response["cafes"])
            }
        }
    })
}

function cafe_update() {
    let cafeImage = $('#input-pic')[0].files[0]
    let cafe_id = $("#cafe_id").val()
    let cafeName = $("#cafeName").val()
    let cafeAddress = $("#cafeAddress").val()
    let cafeTel = $("#cafeTel").val()
    let cafeOpenHours = $("#textarea-post").val()
    let today = new Date().toISOString()
    let form_data = new FormData()
    form_data.append("cafeid_give", cafe_id)
    form_data.append("cafeimage_give", cafeImage)
    form_data.append("cafename_give", cafeName)
    form_data.append("cafeaddress_give", cafeAddress)
    form_data.append("cafetel_give", cafeTel)
    form_data.append("cafeopenhours_give", cafeOpenHours)
    form_data.append("date_give", today)
    console.log(form_data)
    $.ajax({
        type: "POST",
        url: "/cafe/update",
        data: form_data,
        cache: false,
        contentType: false,
        processData: false,
        success: function (response) {
            alert(response['msg'])
            window.location.href = "/"
        }
    })
}

function time2str(date) {
    let today = new Date()
    let time = (today - date) / 1000 / 60  // 분

    if (time < 60) {
        return parseInt(time) + "분 전"
    }
    time = time / 60  // 시간
    if (time < 24) {
        return parseInt(time) + "시간 전"
    }
    time = time / 24
    if (time < 7) {
        return parseInt(time) + "일 전"
    }
    return `${date.getFullYear()}년 ${date.getMonth() + 1}월 ${date.getDate()}일`
}


function toggle_like(cafe_id, type) {
    console.log(cafe_id, type)
    let $a_like = $(`#${cafe_id} a[aria-label='heart']`)
    let $i_like = $a_like.find("i")
    if ($i_like.hasClass("fa-heart")) {
        $.ajax({
            type: "POST",
            url: "/update_like",
            data: {
                cafe_id_give: cafe_id,
                type_give: type,
                action_give: "unlike"
            },
            success: function (response) {
                console.log("unlike")
                $i_like.addClass("fa-heart-o").removeClass("fa-heart")
                $a_like.find("span.like-num").text(num2str(response["count"]))
            }
        })
    } else {
        $.ajax({
            type: "POST",
            url: "/update_like",
            data: {
                cafe_id_give: cafe_id,
                type_give: type,
                action_give: "like"
            },
            success: function (response) {
                console.log("like")
                $i_like.addClass("fa-heart").removeClass("fa-heart-o")
                $a_like.find("span.like-num").text(num2str(response["count"]))
            }
        })

    }
}


function num2str(count) {
    if (count > 10000) {
        return parseInt(count / 1000) + "k"
    }
    if (count > 500) {
        return parseInt(count / 100) / 10 + "k"
    }
    if (count == 0) {
        return ""
    }
    return count
}
