
$(function(){
    $('input[name="send_req"]').click(function(){
    $.ajax({
        type: "GET",
        url: 'send_req/',
        });
        window.location.reload();
        return false;
    });
});

$(function(){
    $('input[name="cancel_req"]').click(function(){
    $.ajax({
        type: "GET",
        url: 'cancel_req/',
        });
        window.location.reload();
        return false;
    });
});

$(function(){
    $('input[name="accept_req"]').click(function(){
    $.ajax({
        type: "GET",
        url: 'accept_req/',
        });
        window.location.reload();
        return false;
    });
});

$(function(){
    $('input[name="reject_req"]').click(function(){
    $.ajax({
        type: "GET",
        url: 'reject_req/',
        });
        window.location.reload();
        return false;
    });
});

$(function(){
    $('input[name="del_friend"]').click(function(){
    $.ajax({
        type: "GET",
        url: 'del_friend/',
        });
        window.location.reload();
        return false;
    });
});

$(function(){
    $('input[name="send_message"]').click(function(){
        location = "dialog/";
    });
});
