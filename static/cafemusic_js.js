$(document).ready(function () {
    cafemusic_get()
})

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
                $("#modal-post2").removeClass("is-active")
            }
        }

    })
}