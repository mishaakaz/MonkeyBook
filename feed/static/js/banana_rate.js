$(function(){
    $('input[name="rate"]').click(function(){
        note_id = $(this).attr("class");

        $.ajax({
            type: "GET",
            url: '/note/' + note_id + '/like/' + $(this).val(),
            });
            window.location.reload();
            return false;
    });
});

$(function(){
    $('input[name="unrate"]').click(function(){
        note_id = $(this).attr("class");

        $.ajax({
            type: "GET",
            url: '/note/' + note_id + '/unlike/',
            });
            window.location.reload();
            return false;
    });
});

$(function(){
    $('input[name="repost-button"]').click(function(){
        link = $(this).val();

        navigator.clipboard.writeText('/note/' + link)
        .then(() => {
            alert("Ссылка на пост успешно скопирована!");
        })
        .catch(err => {
            console.log('При копировании ссылки в буфер обмена что-то пошло не так', err);
        });
    });
});

$(function(){
    $('input[name="delete-post"]').click(function(){
        note_id = $(this).attr("class");
        window.location.replace('/note/' + note_id + '/delete/');
    });
});

