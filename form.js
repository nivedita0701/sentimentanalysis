$(document).ready(function(){
    $('form').on('submit',function(event){
        $.ajax({
            data: {
                message: $('#review-ip').val(),
            },
            type : 'POST',
            url : '/prediction'
        })
        .done(function(data){
            $('#user-review-text').text(data.message)
        })
    })
})