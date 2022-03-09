/*Save it*/

$(document).ready(function(){
  $('[data-toggle="popover"]').popover();
});


/*BMI TAB*/

function openUnit(evt, unitName) {
  let i, tabcontent, tablinks;


  tabcontent = document.querySelectorAll(".tabcontent");
  for (i = 0; i < tabcontent.length; i++) {
    tabcontent[i].style.display = "none";
  }


  tablinks = document.querySelectorAll(".tablinks");//select the two buttons 
  for (i = 0; i < tablinks.length; i++) {
    tablinks[i].className = tablinks[i].className.replace(" active", ""); // For each of the buttons (Metric and Imperial) remove the active class styling on them
  }
  
  document.getElementById(unitName).style.display = "block";
  evt.currentTarget.className += " active"; // add the active class back to the current target
}

// To enable the user when clicked on any of the contents to view the contents if not clicked the content won't display;


// Initializing our tool tip, this must be done with jquery
$(document).ready(function(){
  $('[data-toggle="popover"]').popover();
})