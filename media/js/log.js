/* Script to log times to Timelord */
/* Timer documentation - http://jquery.offput.ca/every/ */

var INTERVAL = 1;//minutes
var INTERVAL_STR = "" + INTERVAL*60 + "s";
var LOG_RATE = 5;//log after this many intervals

var dataMap = {};
var totalTime = 0;
var csrfToken = '';

$(document).ready(function(){
    csrfToken = $('input[name="csrfmiddlewaretoken"]').val();

    $(document).everyTime(INTERVAL_STR, "log_timer", log);
    $("#paused").click(clickPaused);
    $("#task-select").change(taskChanged);
    $("#plus5").click(function(){
        $.post("/timelord/adjust-time/", {'csrfmiddlewaretoken': csrfToken, 'task': $("#task-select").val(), 'adjust': 5}, function(data){
            updateDisplay(data);
        });
    });
    $("#minus5").click(function(){
        $.post("/timelord/adjust-time/", {'csrfmiddlewaretoken': csrfToken, 'task': $("#task-select").val(), 'adjust': -5}, function(data){
            updateDisplay(data);
        });
    });
    // Now update the task time value
    taskChanged();
})

// Keep track of the times on each task. Periodocally update the main server
function log() {
    var idx = $("#task-select").val();
    dataMap['csrfmiddlewaretoken'] = csrfToken;
    
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
            updateDisplay(data);
        });
        
        totalTime = 0;
        dataMap = {};
    }
}

// Stop recording time
function clickPaused() {
    if (this.checked) {
        $(document).stopTime("log_timer");
    } else {
        $(document).everyTime(INTERVAL_STR, "log_timer", log);
    }
}

// When the selected task changes update the task time value on screen
function taskChanged() {
    $.post("/timelord/task-status/", {'csrfmiddlewaretoken': csrfToken, 'task': $("#task-select").val()}, function(data){
        updateDisplay(data);
    });
}

function updateDisplay(data) {
    $('#task-time').html($('current-task', data).text());
    $('#today-time').html($('today-time', data).text());
}
