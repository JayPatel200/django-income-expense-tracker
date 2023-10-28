// This file handles functionality for register and login page

const usernameField = document.querySelector("#usernameField");
const feedBackArea = document.querySelector(".invalid_feedback");
const emailField = document.querySelector("#emailField");
const emailFeedBackArea = document.querySelector(".emailFeedBackArea");
const passwordField = document.querySelector("#passwordField");
const usernameSuccesspOutput = document.querySelector(".usernameSuccesspOutput");
const showPasswordToggle = document.querySelector(".showPasswordToggle");
const submitBtn = document.querySelector(".submit-btn");

//handles password reveal and hide functionality
const handleToggleInput = (e) => {
  if (showPasswordToggle.textContent === "SHOW") {
    showPasswordToggle.textContent = "HIDE";
    passwordField.setAttribute("type", "text");
  } else {
    showPasswordToggle.textContent = "SHOW";
    passwordField.setAttribute("type", "password");
  }
};

//onclick reveals/hides password
showPasswordToggle.addEventListener("click", handleToggleInput);

//listens to the user input and sends a request to backend to validate email entered
emailField.addEventListener("keyup", (e) => {
  const emailVal = e.target.value;

  emailField.classList.remove("is-invalid");
  emailFeedBackArea.style.display = "none";

  if (emailVal.length > 0) {
    fetch("/authentication/validate-email", {
      body: JSON.stringify({ email: emailVal }),
      method: "POST",
    })
      .then((res) => res.json())
      .then((data) => {
        //display appropriate prompt/error 
        if (data.email_error) {
          submitBtn.disabled = true;
          emailField.classList.add("is-invalid");
          emailFeedBackArea.style.display = "block";
          emailFeedBackArea.innerHTML = `<p>${data.email_error}</p>`;
        } else {
          //if no errors then enable the submit button
          submitBtn.removeAttribute("disabled");
        }
      });
  }
});

//listens to the user input and sends a request to backend to validate username entered
usernameField.addEventListener("keyup", (e) => {
  const usernameVal = e.target.value;

  usernameField.classList.remove("is-invalid");
  feedBackArea.style.display = "none";

  if (usernameVal.length > 0) {
    fetch("/authentication/validate-username", {
      body: JSON.stringify({ username: usernameVal }),
      method: "POST",
    })
      .then((res) => res.json())
      .then((data) => {
        //display appropriate prompt/error 
        if (data.username_error) {
          submitBtn.disabled = true;
          usernameField.classList.add("is-invalid");
          feedBackArea.style.display = "block";
          feedBackArea.innerHTML = `<p>${data.username_error}</p>`;
        } else {
          //if no errors then enable the submit button
          submitBtn.removeAttribute("disabled");
        }
      });
  }
});
