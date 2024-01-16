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
function loadAndDisplayFiles() {
    fetch('/api/get-files')
        .then(response => response.text())
        .then(html => {
            let container = document.getElementById('files-container');
            container.innerHTML = html; // Вставляем HTML-код в контейнер
        })
        .catch(error => console.error('Ошибка при загрузке файлов:', error));
}





function submitForm() {
    const host = document.getElementById('host').value;
    const port = document.getElementById('port').value; // Используйте port
    const login = document.getElementById('login').value;
    const pass = document.getElementById('pass').value;

    const data = { host, port, login, pass };

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
        document.getElementById('scannerStatus').textContent = "Завершение работы проверте floder на pdf ";
        // Обработка успешного ответа
    })
    .catch((error) => {
        console.error('Error:', error);
        // Обработка ошибки
    });
}




setInterval(updateServerTime, 1000);

