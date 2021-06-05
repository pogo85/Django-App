const usernameField = document.querySelector('#username-field')
const emailField = document.querySelector('#email-field')
const usernameFeedback = document.querySelector('.invalid-username-feedback')
const emailFeedback = document.querySelector('.invalid-email-feedback')
const passwordField = document.querySelector('#password-field')
const password_toggle = document.querySelector('#password-toggle')
const submit = document.querySelector('#submit_btn')

console.log(usernameField)

usernameField.addEventListener('keyup', (e) => {
    const usernameValue = e.target.value
    console.log(usernameValue)
    const url = "/authentication/validate-username"
    if (usernameValue.length > 0) {
        fetch(url, {
            body: JSON.stringify({username: usernameValue}),
            method: "POST",
        }).then(res => res.json())
            .then(data => {
                console.log(data)

                if (data.username_valid) {
                    usernameField.classList.remove('is-invalid')
                    usernameField.classList.add('is-valid')
                    usernameFeedback.style.display = 'None'
                    submit.removeAttribute('disabled')
                }

                if (data.username_number) {
                    usernameField.classList.add('is-invalid')
                    usernameFeedback.style.display = 'block'
                    usernameFeedback.innerHTML = `<p>${data.username_number}</p>`
                    submit.setAttribute('disabled', 'disabled')
                }

                if (data.username_error) {
                    usernameField.classList.add('is-invalid')
                    usernameFeedback.style.display = 'block'
                    usernameFeedback.innerHTML = `<p>${data.username_error}</p>`
                    submit.setAttribute('disabled', 'disabled')
                }

                if (data.username_already_exists) {
                    usernameField.classList.add('is-invalid')
                    usernameFeedback.style.display = 'block'
                    usernameFeedback.innerHTML = `<p>${data.username_already_exists}</p>`
                    submit.setAttribute('disabled', 'disabled')
                }
            })
    } else {
        usernameField.classList.remove('is-invalid')
        usernameField.classList.remove('is-valid')
        usernameFeedback.style.display = 'None'
    }
})

emailField.addEventListener('keyup', (e) => {
    const emailValue = e.target.value
    console.log(emailValue)
    const url = "/authentication/validate-email"
    if (emailValue.length > 0) {
        fetch(url, {
            body: JSON.stringify({email: emailValue}),
            method: "POST",
        }).then(res => res.json())
            .then(data => {
                console.log(data)

                if (data.email_valid) {
                    emailField.classList.remove('is-invalid')
                    emailField.classList.add('is-valid')
                    emailFeedback.style.display = 'None'
                    submit.removeAttribute('disabled')
                }

                if (data.email_error) {
                    emailField.classList.add('is-invalid')
                    emailFeedback.style.display = 'block'
                    emailFeedback.innerHTML = `<p>${data.email_error}</p>`
                    submit.setAttribute('disabled', 'disabled')
                }

                if (data.email_already_exists) {
                    emailField.classList.add('is-invalid')
                    emailFeedback.style.display = 'block'
                    emailFeedback.innerHTML = `<p>${data.email_already_exists}</p>`
                    submit.setAttribute('disabled', 'disabled')
                }
            })
    } else {
        emailField.classList.remove('is-invalid')
        emailField.classList.remove('is-valid')
        emailFeedback.style.display = 'None'
    }
})

password_toggle.addEventListener('click', (e) => {
    if (password_toggle.textContent === 'SHOW') {
        password_toggle.textContent = 'HIDE'
        passwordField.setAttribute('type', 'text')
    } else {
        password_toggle.textContent = 'SHOW'
        passwordField.setAttribute('type', 'password')
    }
})