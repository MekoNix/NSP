document.getElementById('loginForm').addEventListener('submit', function(event) {
            event.preventDefault();

            var username = document.getElementsByName('username')[0].value;
            var password = document.getElementsByName('password')[0].value;
            var errorMessage = document.getElementById('errorMessage');

            fetch('/login', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
                body: `username=${encodeURIComponent(username)}&password=${encodeURIComponent(password)}`,
            })
            .then(response => {
                if (!response.ok) {
                    if (response.status === 401) {
                        return response.text().then(text => Promise.reject(text));
                    }
                    return Promise.reject('An error occurred');
                }
                return response.text();
            })
            .then(text => {
                window.location.href = '/dashboard'; // ������ ���������������
            })
            .catch(errorText => {
                errorMessage.textContent = errorText;
                errorMessage.style.display = 'block';
                setTimeout(() => {
                    errorMessage.style.display = 'none';
                }, 4000);
            });
        });