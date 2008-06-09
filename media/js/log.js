/* Script to log times to Timelord */
/* Timer documentation - http://jquery.offput.ca/every/ */

var INTERVAL = 10;//<--------------------- Change to 60
var INTERVAL_STR = "" + INTERVAL + "s";

var times = [];
var totalTime = 0;

$(document).ready(function(){
    $(document).everyTime(INTERVAL_STR, "log_timer", log);
    $("#paused").click(clickPaused);
})

function log() {
    var idx = $("#task").val();
    
    var time = times[idx];
    if (time == undefined) {
        times[idx] = INTERVAL;
    } else {
        times[idx] += INTERVAL;
    }
    
    totalTime += INTERVAL;
    // Log every five minutes
    if (totalTime >= 30) {//<------------ Change to 300
        alert("log");
        totalTime = 0;
        times = [];
    }
}

function clickPaused() {
    if (this.checked) {
        $(document).stopTime("log_timer");
    } else {
        $(document).everyTime(INTERVAL_STR, "log_timer", log);
    }
}