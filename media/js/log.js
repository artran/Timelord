/* Script to log times to Timelord */
/* Timer documentation - http://jquery.offput.ca/every/ */

var INTERVAL = 1;//minutes
var INTERVAL_STR = "" + INTERVAL*60 + "s";
var LOG_RATE = 5;//log after this many intervals

var dataMap = {};
var totalTime = 0;

$(document).ready(function(){
    $(document).everyTime(INTERVAL_STR, "log_timer", log);
    $("#paused").click(clickPaused);
    $("#task-select").change(taskChanged);
})

function log() {
    var idx = $("#task-select").val();
    
    var time = dataMap[idx];
    if (time == undefined) {
        dataMap[idx] = INTERVAL;
    } else {
        dataMap[idx] += INTERVAL;
    }
    
    totalTime += INTERVAL;
    // Log every five minutes
    if (totalTime >= LOG_RATE) {
        dataMap["task"] = idx

        $.post("/timelord/log/", dataMap, function(data){
            $('#task-time').html($('current-task', data).text());
            $('#today-time').html($('today-time', data).text());
        });
        
        totalTime = 0;
        dataMap = {};
    }
}

function clickPaused() {
    if (this.checked) {
        $(document).stopTime("log_timer");
    } else {
        $(document).everyTime(INTERVAL_STR, "log_timer", log);
    }
}

function taskChanged() {
    $.post("/timelord/task-status/", {'task': $("#task-select").val()}, function(data){
        $('#task-time').html($('current-task', data).text());
        $('#today-time').html($('today-time', data).text());
    });
}