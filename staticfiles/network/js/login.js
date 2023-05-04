// This file contains the javascript code for login and register page

// animation from the slide
const signInButton = document.querySelector(".L_btn");
const registerButton = document.querySelector(".R_btn");
const formBox = document.querySelector(".formBox");

registerButton.onclick = () => {
    formBox.classList.add("active");
}
signInButton.onclick = () => {
    formBox.classList.remove("active");
}

// function to login
function login(){
    event.preventDefault();
    const csrfToken = document.getElementsByName('csrfmiddlewaretoken')[0].value;
    const L_alert = document.querySelector('#L_alert');
    const form = document.querySelector('.L_form');
    const formData = new FormData(form);
    fetch("/login", {
        method: 'POST',
        headers: {
            'X-CSRFToken': csrfToken
          },
        body: formData
    })
    .then(response => response.json())
    .then(data =>{
        showAlert(data,L_alert)
    })
    .catch(error => {
        console.log(error);
    });
  }

// function to register
function register(){
    event.preventDefault();
    const csrfToken = document.getElementsByName('csrfmiddlewaretoken')[0].value;
    const R_alert = document.querySelector('#R_alert');
    const form = document.querySelector('.R_form');
    const formData = new FormData(form);
    fetch("/register", {
        method: 'POST',
        headers: {
            'X-CSRFToken': csrfToken
          },
        body: formData
    })
    .then(response => response.json())
    .then(data =>{
        showAlert(data,R_alert)
    })
    .catch(error => {
        console.log(error);
    });
}

// function to show alert
function showAlert(data,alert){
    if (data.success){
        window.location.href = data.redirect;
    }
    else {
        document.querySelector('#alertText').innerHTML = data.message;
        document.querySelector('#alertText2').innerHTML = data.message;
        alert.classList.remove('hidden');
        
        setTimeout(function(){
            alert.classList.add('hidden');
        }, 4500);
    }
}