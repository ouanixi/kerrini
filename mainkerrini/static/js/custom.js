//Video play page Scripts
document.addEventListener("DOMContentLoaded", function () {

    $.getJSON('/get_links/', {'video_id': $("#video_id").val()}, function (data) {
        $.each(data, function () {
            popcorn.tagthisperson({
                start: data['time_tag'],
                end: data['time_tag'] + 4,
                person: data['comment'],
                href: data['url'],
                target: "tags"
            });
        });

    });
    var popcorn = Popcorn("#ourvideo", {pauseOnLinkClicked: true});

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


//Video upload page Scripts

$("#inputTag").change(function () {
    var selectedValues = $('#inputTag').val();
    var area = document.getElementById("selectedTags");
    area.value = selectedValues.join("  ");
});

