document.getElementById('signupForm').addEventListener('submit', function(event) {
    event.preventDefault();

    var username = document.getElementById('username').value;
    var password = document.getElementById('password').value;
    var errorMessage = document.getElementById('errorMessage');

    fetch('/signup', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: `username=${encodeURIComponent(username)}&password=${encodeURIComponent(password)}`,
    })
    .then(response => {
        if (!response.ok) {
            if (response.status === 400) {
                return response.text().then(text => Promise.reject(text));
            } else if (response.status === 401) {
                return Promise.reject('User already exists. Please choose a different username.');
            }
            return Promise.reject('An error occurred');
        }
        return response.text();
    })
    .then(text => {
        window.location.href = '/login';
    })
    .catch(errorText => {
        errormessage.textContent = errorText;
        errormessage.style.display = 'block';
        setTimeout(() => {
            errormessage.style.display = 'none';
        }, 4000);
    });
});
