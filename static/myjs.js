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
            window.location.reload()
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


/*
function toggle_like(post_id, type) {
    console.log(post_id, type)
    let $a_like = $(`#${post_id} a[aria-label='heart']`)
    let $i_like = $a_like.find("i")
    if ($i_like.hasClass("fa-heart")) {
        $.ajax({
            type: "POST",
            url: "/update_like",
            data: {
                post_id_give: post_id,
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
                post_id_give: post_id,
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



function get_posts(username) {
    $("#post-box").empty()
    if (username == undefined) {
        username = ""
    }
    $.ajax({
        type: "GET",
        url: `/get_posts?username_give=${username}`,
        data: {},
        success: function (response) {
            if (response["result"] == "success") {
                let posts = response["posts"]
                for (let i = 0; i < posts.length; i++) {
                    let post = posts[i]
                    let time_post = new Date(post["date"])
                    let time_before = time2str(time_post)
                    let class_heart = post['heart_by_me'] ? "fa-heart" : "fa-heart-o"
                    let count_heart = post['count_heart']
                    let html_temp = `<div class="box" id="${post["_id"]}">
                                        <article class="media">
                                            <div class="media-left">
                                                <a class="image is-64x64" href="/user/${post['username']}">
                                                    <img class="is-rounded" src="/static/${post['profile_pic_real']}"
                                                         alt="Image">
                                                </a>
                                            </div>
                                            <div class="media-content">
                                                <div class="content">
                                                    <p>
                                                        <strong>${post['profile_name']}</strong> <small>@${post['username']}</small> <small>${time_before}</small>
                                                        <br>
                                                        ${post['comment']}
                                                    </p>
                                                </div>
                                                <nav class="level is-mobile">
                                                    <div class="level-left">
                                                        <a class="level-item is-sparta" aria-label="heart" onclick="toggle_like('${post['_id']}', 'heart')">
                                                            <span class="icon is-small"><i class="fa ${class_heart}"
                                                                                           aria-hidden="true"></i></span>&nbsp;<span class="like-num">${num2str(count_heart)}</span>
                                                        </a>
                                                    </div>

                                                </nav>
                                            </div>
                                        </article>
                                    </div>`
                    $("#post-box").append(html_temp)
                }
            }
        }
    })
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

 */