$(function () {
    cafemusic_get()
})

// function cafemusic() {
//     let url = $('#cafeMusicUrl').val()
//     let form_data = new FormData()
//     form_data.append("url_give", url)
//     console.log(url)
//     $.ajax({
//         type: "POST",
//         url: "/update_music/<username>",
//         data: form_data,
//         cache: false,
//         contentType: false,
//         processData: false,
//         success: function (response) {
//             if (response["result"] == "success") {
//                 window.location.reload()
//             }
//         }
//     })
// }
function cafemusic_accept() {
    $('#cards-box2').empty()
    let url = $('#cafeMusicUrl').val()
    let form_data = new FormData()
    form_data.append("url_give", url)
    console.log(url)
    $.ajax({
        type: 'POST',
        url: '/cafemusic/accept',
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

function cafemusic_get() {
    $.ajax({
        type: 'GET',
        url: '/cafemusic/accept',
        success: function (response) {
            rows = response['cafemusic_list']
            for (i = 0; i < rows.length; i++) {
                let title = rows[i]['title']
                let view = rows[i]['view']
                let embed = rows[i]['embed']
                let author = rows[i]['author']
                let temp_html = `<div class="col">
                                       <div class="card h-100">
                                        <iframe width="100%"  src="${embed}" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
            <div class="card-body">
                <h5 class="card-title">${title}</h5>
                <p><i class="fa fa-youtube-play" aria-hidden="true"></i><span>${view}</span></p>
                <p><i class="fa fa-user" aria-hidden="true"></i><span>${author}</span></p>
                </div>
        </div>
    </div>`
                $('#cards-box2').append(temp_html)
                $("#modal-post2").removeClass("is-active")
            }
        }

    })
}

// function cafemusic_accept() {
//     $('#cards-box2').empty()
//     $.ajax({
//         type: 'GET',
//         url: '/cafemusic/accept/<username>',
//         data: {},
//         success: function (response) {
//             rows = response['cafemusic_list']
//             for (i = 0; i < rows.length; i++) {
//                 let username = rows[i]['username']
//                 let title = rows[i]['title']
//                 let view = rows[i]['view']
//                 let embed = rows[i]['embed']
//                 let author = rows[i]['author']
//                 let temp_html = `<div class="col">
//                                            <div class="card h-100">
//                                             <iframe width="100%"  src="${embed}" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
//                 <div class="card-body">
//                     <h5 class="card-title">${title}</h5>
//                     <p><span>${username}</span></p>
//                     <p><i class="fa fa-youtube-play" aria-hidden="true"></i><span>${view}</span></p>
//                     <p><i class="fa fa-user" aria-hidden="true"></i><span>${author}</span></p>
//                     </div>
//             </div>
//         </div>`
//                 $('#cards-box2').append(temp_html)
//             }
//         }
//     })
// }

// function update_profile() {
//     $('#cards-box').empty()
//     $.ajax({
//         type: 'GET',
//         url: '/',
//         data: {},
//         success: function (response) {
//             rows = response['music_list']
//             for (i = 0; i < rows.length; i++) {
//                 let title = rows[i]['title']
//                 let view = rows[i]['view']
//                 let embed = rows[i]['embed']
//                 let temp_html = `<div class="col">
//                                            <div class="card h-100">
//                                             <iframe width="100%" height="167.5" src="${embed}" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
//                 <div class="card-body">
//                     <h5 class="card-title">${title}</h5>
//                     <p><span>${view}</span><span>👁</span></p>
//                     <p>😍</p>
//                     </div>
//             </div>
//         </div>`
//                     $('#cards-box').append(temp_html)
//             }
//         }
//     })
// }

// function update_profile() {
//     let url = $('#re_url').val()
//     let form_data = new FormData()
//     form_data.append("url_give", url)
//     console.log(name, url)
//     $.ajax({
//         type: "POST",
//         url: "/update_music",
//         data: form_data,
//         cache: false,
//         contentType: false,
//         processData: false,
//         success: function (response) {
//             if (response["result"] == "success") {
//                 alert(response["msg"])
//                 window.location.reload()
//             }
//         }
//     })
// }