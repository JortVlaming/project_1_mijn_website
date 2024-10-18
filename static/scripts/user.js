let postButton = document.querySelector("#create_post_button");
let postFrom = document.querySelector("#create_post_form");

postButton.addEventListener("click", function () {
    postFrom.submit();
})