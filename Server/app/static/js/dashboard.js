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
        }, 10); // Маленькая задержка перед началом анимации
    }, 50); // Задержка соответствует времени исчезновения предыдущей секции
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

$(document).ready(function(){
    $('#loadFiles').click(function(){
        $.getJSON('/api/get-files', function(files){
            $('#files').empty();
            files.forEach(function(file){
                // Создаем ссылку на файл
                var fileLink = $('<a>').attr('href', '/path/to/files/' + file).text(file);
                // Создаем элемент для отображения ссылки
                var fileElement = $('<div>').addClass('file').append(fileLink);
                // Добавляем элемент в список файлов
                $('#files').append(fileElement);
            });
        });
    });
});


setInterval(updateServerTime, 1000);

