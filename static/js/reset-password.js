const emailField = document.querySelector('#email-field')

emailField.addEventListener('keyup', (e) => {
    const emailValue = e.target.value
    console.log(emailValue)
    const url = "/authentication/validate-reset-email"
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
                    submit.removeAttribute('disabled')
                }

                if (data.email_error) {
                    emailField.classList.add('is-invalid')
                    submit.setAttribute('disabled', 'disabled')
                }
            })
    } else {
        emailField.classList.remove('is-invalid')
        emailField.classList.remove('is-valid')
    }
})