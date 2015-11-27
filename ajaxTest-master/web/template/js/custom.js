document.addEventListener("DOMContentLoaded", function () {

    var popcorn = Popcorn("#ourvideo", {pauseOnLinkClicked: true});

    var kvArray = ["http://annasob.wordpress.com", "https://www.google.co.uk", "https://www.amazon.co.uk"];

    for (var i = 0; i < kvArray.length; i++) {
        popcorn.tagthisperson({
            start: i * 5,
            end: (i * 5) + 4,
            person: kvArray[i],
            href: kvArray[i],
            target: "tags"
        });
    }



}, false);


function pause() {
    document.getElementById("ourvideo").pause();
}



$(document.body).on('hidden.bs.modal', function () {

    document.getElementById("ourvideo").play();


});

$(".playlistButton").click(function () {
    var playerS = $('#playerSource');
    var sourceN = $(this).attr("value");

    playerS.attr('src', sourceN);


    var video_block = $('#ourvideo').get(0);
    video_block.load();
    video_block.play();

});



$("button#tagSubmit").click(function () {
    $.ajax({
        type:'GET',
        url: 'test',
        data: { tagInput : $('#tagInput').val(), urlInput : $('#urlInput').val()},
        success: function () {
            document.getElementById("responseSuccess").removeAttribute('hidden');
            $(".modalHide").modal('hide');
        },
        error: function () {
            document.getElementById("responseFailure").removeAttribute('hidden');
            $(".modalHide").modal('hide');
        }
    });
});