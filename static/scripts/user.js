let postButton = document.querySelector("#create_post_button");
let postFrom = document.querySelector("#create_post_form");

postButton.addEventListener("click", function () {
    postFrom.submit();
});

// Get the modal
var modal = document.getElementById("editModal");

// Get the button that opens the modal
var btn = document.getElementById("editButton");

// Get the <span> element that closes the modal
var span = document.getElementsByClassName("close")[0];

// When the user clicks on the button, open the modal
btn.onclick = function() {
  modal.style.display = "block";
}

// When the user clicks on <span> (x), close the modal
span.onclick = function() {
  modal.style.display = "none";
}

// When the user clicks anywhere outside of the modal, close it
window.onclick = function(event) {
  if (event.target == modal) {
    modal.style.display = "none";
  }
}