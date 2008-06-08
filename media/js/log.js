/* Script to log times to Timelord */
/* Timer documentation - http://jquery.offput.ca/every/ */

$(document).ready(function(){
    $(this).everyTime("5s", "log_timer", log);
    $("#paused").change(changePaused);
})

function log() {
    alert("summat to log");
}

function changePaused() {
    alert("change")
    $(this).stopTime("log_timer");
}