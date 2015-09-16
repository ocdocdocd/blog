var page = 1;

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
var csrftoken = getCookie('csrftoken');

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});

function getMoreEntries(page) {
    $.ajax('/blog/get_entries/', {
        type: 'POST',
        dataType: 'html',
        data: {page_num: page},
        success: function(data) {
            $("#posts").append(data);
        }
    })
    return 1;
}

$(window).scroll(function() {
    if ($(window).scrollTop() + $(window).height() >= $(document).height() - 150) {
        page += getMoreEntries(page);
    }
})

$(document).ready(function() {
    $("#comment_form").submit(function(event) {
        event.preventDefault();
        var comment = $("#comment_area").val();
        $.ajax('/blog/post_comment/', {
            type: 'POST',
            dataType: 'html',
            data: {post_comment: comment,
                   path: window.location.pathname},
            success: function(data) {
                $("#comments").append(data);
                $("#comment_form").append("Comment submited!");
                var num_coms = parseInt($("#num").text());
                num_coms++;
                $("#num").text(num_coms.toString());
                $('html, body').animate({
                    scrollTop: $('.comment:last').offset().top
                }, 1000);
            }
        })
    })
})

$(document).ready(function() {
    $(".likebtn").click(function(event) {
        var c_id = this.id;
        $.ajax('/blog/like/', {
            type: 'POST',
            dataType: 'text',
            data: {id: c_id},
            success: function(data) {
                var like_id = "#" + c_id + "_likes";
                $(like_id).text(data.toString());
                $("#" + c_id).toggleClass('liked');
            }
        })
    })
})