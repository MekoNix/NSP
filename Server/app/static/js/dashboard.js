document.addEventListener('DOMContentLoaded', function() {
    const usernameElement = document.getElementById('username');
    const username = usernameElement ? usernameElement.getAttribute('data-username') : null;

    if (!username) {
        console.error('Username is not defined.');
        return;
    }

    loadAndDisplayFiles(username);
    showChart(username);
    setInterval(() => loadAndDisplayFiles(username), 1000);

    window.toggleSection = function(sectionId) {
        const sections = document.querySelectorAll('.content-section');
        sections.forEach(section => {
            const isTargetSection = section.id === sectionId;
            section.style.display = isTargetSection ? "block" : "none";
            section.classList.toggle("active", isTargetSection);
        });

        const chartContainer = document.getElementById('chartContainer');
        chartContainer.style.display = sectionId === 'chartContainer' ? 'block' : 'none';
        if (sectionId === 'chartContainer') showChart(username);
    };
});

let chart; // Переменная для хранения экземпляра чарта

function showChart(username) {
    fetch(`/api/data/${username}/pf`)
        .then(response => response.json())
        .then(data => {
            if (chart) chart.destroy(); // Удаляем предыдущий чарт, если он существует

            const chartContainer = document.getElementById('myChart').getContext('2d');
            const noDataElement = document.getElementById('noData');
            const info = document.getElementById('info');

            if (!data.Total_scan || data.Total_scan === 0) {
                chartContainer.canvas.style.display = 'none';
                noDataElement.style.display = 'block';
                info.innerHTML = '';
                return;
            }

            chartContainer.canvas.style.display = 'block';
            noDataElement.style.display = 'none';

            chart = new Chart(chartContainer, {
                type: 'doughnut',
                data: {
                    labels: ['Критические', 'Нежелательные', 'Лёгкие'],
                    datasets: [{
                        label: 'Scan Results',
                        data: [data.red, data.yellow, data.green],
                        backgroundColor: [
                            'rgba(255, 99, 132, 0.2)',
                            'rgba(255, 205, 86, 0.2)',
                            'rgba(75, 192, 192, 0.2)'
                        ],
                        borderColor: [
                            'rgba(255, 99, 132, 1)',
                            'rgba(255, 205, 86, 1)',
                            'rgba(75, 192, 192, 1)'
                        ],
                        borderWidth: 1
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                }
            });

            info.innerHTML = `<p>Total Scan: ${data.Total_scan}</p><p>Last Scan: ${data.Last_scan}</p>`;
        })
        .catch(error => {
            console.error('Ошибка при загрузке данных:', error);
        });
}




function loadAndDisplayFiles(username) {
    fetch(`/api/get-html-files/${username}`)
        .then(response => response.json())
        .then(files => {
            let container = document.getElementById('files-container');
            let html = files.map(file => {
                const displayName = file.name.replace(/\.html$/, '');
                const fileDate = file.birthday;
                return `<tr><td><a href="/users/${username}/${file.name}" target="_blank">${displayName}</a></td><td>${fileDate}</td><td><button onclick="downloadPDF('${file.name}', '${username}')">Скачать PDF</button></td></tr>`;
            }).join('');
            container.innerHTML = html;
        })
        .catch(error => console.error('Ошибка при загрузке файлов:', error));
}

function downloadPDF(fileName, username) {
    window.location.href = `/api/download-pdf/${username}/${fileName}`;
}

function submitForm() {
    const host = document.getElementById('host').value;
    const port = document.getElementById('port').value;
    const login = document.getElementById('login').value;
    const pass = document.getElementById('pass').value;
    const comment = document.getElementById('comment').value;

    const data = { host, port, login, pass, comment };

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
            document.getElementById('scannerStatus').textContent = "Сканер заврешил работу перейдите в секцию folder ";
        })
        .catch((error) => {
            console.error('Error:', error);
        });
}


function logout() {
    const dropdownMenu = document.querySelector('.dropdown-menu')
    dropdownMenu.style.display = dropdownMenu.style.display === 'block'? 'none' : 'block';
}