let loginButton = document.getElementById("LoginButton");
let login_error_holder = document.getElementById("login_error");
let login_error = document.getElementById("login_error_text");
let login_form = document.getElementById("loginForm");

let signupButton = document.getElementById("SignupButton");
let signup_error_holder = document.getElementById("signup_error");
let signup_error = document.getElementById("signup_error_text");
let signup_form = document.getElementById("signupForm");



loginButton.addEventListener("click", function() {
    login_form.submit();
});

signupButton.addEventListener("click", function() {
    const data = new FormData(signup_form);
    let p1 = data.get("password")[0];
    let p2 = data.get("confirm_password")[0];

    if (p1 !== p2) {
        signup_error.innerText = "Passwords do not match";
        signup_error_holder.display = "block";
        return;
    }

    signup_form.submit();
});
