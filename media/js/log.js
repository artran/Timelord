/* Script to log times to Timelord */
/* Timer documentation - http://jquery.offput.ca/every/ */

var times = new Array();

$(document).ready(function(){
    $(document).everyTime("30s", "log_timer", log);
    $("#paused").click(clickPaused);
})

function log() {
    var idx = $("#task").selectedIndex;
    alert(idx);
}

function clickPaused() {
    if (this.checked) {
        $(document).stopTime("log_timer");
    } else {
        $(document).everyTime("30s", "log_timer", log);
    }
}