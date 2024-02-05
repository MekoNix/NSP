

document.addEventListener('DOMContentLoaded', function() {
    const usernameElement = document.getElementById('username');
    const username = usernameElement ? usernameElement.getAttribute('data-username') : null;
    console.log(username); // Должно выводить фактическое значение username

    if (username) {
        loadAndDisplayFiles(username);
        setInterval(() => loadAndDisplayFiles(username), 1000); // Автоматическое обновление каждые 10 секунд
    } else {
        console.error('Username is not defined.');
    }
});

function toggleSection(sectionId) {
    const sections = document.querySelectorAll('.content-section');
    sections.forEach(section => {
        section.classList.remove('active');
        section.style.display = 'none'; // Скрываем секции
    });

    setTimeout(() => {
        const activeSection = document.getElementById(sectionId);
        activeSection.style.display = 'block'; // Отображаем нужную секцию
        setTimeout(() => {
            activeSection.classList.add('active'); // Добавляем класс для анимации
        }, 10); //  задержка перед началом анимации
    }, 50);
}

function toggleDropdownMenu() {
    const dropdownMenu = document.querySelector('.dropdown-menu');
    dropdownMenu.style.display = dropdownMenu.style.display === 'block' ? 'none' : 'block';
}

function updateServerTime() {
    const serverTimeElement = document.getElementById('serverTime');
    const currentTime = new Date().toLocaleTimeString();
    serverTimeElement.textContent = currentTime;
}

function loadAndDisplayFiles(username) {
    fetch(`/api/get-html-files/${username}`)
        .then(response => response.json())
        .then(files => {
            let container = document.getElementById('files-container');
            // Удаляем расширение .html из текста ссылки, но оставляем в URL
            let html = files.map(file => {
                const displayName = file.replace(/\.html$/, ''); // Удаляем расширение .html для отображения
                return `<a href="/users/${username}/${file}" target="_blank">${displayName}</a>`; // Ссылка ведёт на .html файл
            }).join('<br>');
            container.innerHTML = html; // Вставляем HTML-код в контейнер
        })
        .catch(error => console.error('Ошибка при загрузке файлов:', error));
}



function submitForm() {
    const host = document.getElementById('host').value;
    const port = document.getElementById('port').value;
    const login = document.getElementById('login').value;
    const pass = document.getElementById('pass').value;
    const comment = document.getElementById('comment').value;

    const data = { host, port, login, pass, comment};

    fetch('/dashboard', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(data => {
        console.log('Success:', data);
        document.getElementById('scannerStatus').textContent = "Вы будете перенаправленны после "; // НЕ ЗАБУДЬ СДЕЛТЬА ПЕРЕНАПРОВЛЕНИЕ ПОСЛЕ ТОГО КАК СКНЕР СДЕЛАЕТ РАБОТУ
    })
    .catch((error) => {
        console.error('Error:', error);
        // Обработка ошибки
    });
}

setInterval(updateServerTime, 1000);
loadAndDisplayFiles(username); // Автоматически вызываем функцию при загрузке страницы
