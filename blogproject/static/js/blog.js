$(document).ready(function() {
    $("#comment_form").submit(function(event) {
        event.preventDefault();
        var comment = $("#comment_area").val();
        $.ajax('blog/post_comment', {
            type: 'POST',
            dataType: 'json',
            data: {post_comment: comment},
            success: function(data) {
                $("#comments").append(data);
                $("#comment_form").append("Comment submited!");
            };
        });
    });
});