/**
 * Created by jamie on 01/12/15.
 */
$(document).ready(function() {
    $('#correct').click(function(){

        var data = {'video_id': $("#video_id").val(),
                    'vote': 'yes',
                    'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val()
                    }
        $.post("/video_vote/", data, function(data){
            $('#ajax_correctness').html("Correctness: " + data + "%")
            $('#close').click()
        });
    });

    $('#incorrect').click(function(){

        var data = {'video_id': $("#video_id").val(),
                    'vote': 'no',
                    'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val()
                    }
        $.post("/video_vote/", data, function(data){
            $('#ajax_correctness').html("Correctness: " + data + "%")
            $('#close').click()
        });
    });

    $('#submit_link').click(function(){
        var video = document.getElementById("ourvideo").currentTime;
        var data = {'video_id': $("#video_id").val(),
                    'link': $("#urlInput").val(),
                    'time_tag' : video,
                    'description': $("#tagInput").val(),
                    'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val()
                    }
        $.post("/add_video_link/", data, function(data){
            //$('#ajax_correctness').html("Correctness: " + data + "%")
            $('#close_link').click()
        });
    });
});