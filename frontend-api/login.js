let form = document.getElementById('login-form')

form.addEventListener('submit', (e) => {
    e.preventDefault()
    let formData = {
        'username': form.username.value,
        'password': form.password.value,
    }

    fetch("http://127.0.0.1:8000/api/token/", {
        method: 'POST',
        headers: {
            'content-type': 'application/json',
        },
        body: JSON.stringify(formData)
    })
    .then(response => response.json())
    .then(data => {
        if (data.access) {
            localStorage.setItem('token', data.access)
            window.location = "/"
        }
        else {
            window.alert("Wrong usernmae or password.")
        }
    })
})