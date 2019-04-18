window.onload = function() {
    var sidebarToggle = document.getElementById('sidebarToggle');
    sidebarToggle.click();
};



//setup before functions
var typingTimer;                //timer identifier
var doneTypingInterval = 500;  //time in ms, 5 second for example
var $input = $('#myInput');

//on keyup, start the countdown
$input.on('keyup', function () {
  clearTimeout(typingTimer);
  typingTimer = setTimeout(doneTyping, doneTypingInterval);
});

//on keydown, clear the countdown
$input.on('keydown', function () {
  clearTimeout(typingTimer);

});

//user is "finished typing," do something
function doneTyping () {
  //do something
    console.log(")))");
}

// $('input[type="text"]').keypress(myFunc);
//
// function myFunc(){
//  alert( $(this).val() );
// }