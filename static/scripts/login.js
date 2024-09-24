let loginButton = document.getElementById("LoginButton");
let signupButton = document.getElementById("SignupButton");

document.getElementById("navLoginButton").hidden = true;

loginButton.addEventListener("click", function() {
    console.log("login");
});

signupButton.addEventListener("click", function() {
    console.log("signup");
})