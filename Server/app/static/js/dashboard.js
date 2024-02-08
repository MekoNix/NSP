
document.addEventListener('DOMContentLoaded', function() {
    const usernameElement = document.getElementById('username');
    const username = usernameElement ? usernameElement.getAttribute('data-username') : null;

    if (username) {
        loadAndDisplayFiles(username);
        setInterval(() => loadAndDisplayFiles(username), 1000);
    } else {
        console.error('Username is not defined.');
    }

});

document.addEventListener('DOMContentLoaded', function() {
    const usernameElement = document.getElementById('username');
    const username = usernameElement ? usernameElement.getAttribute('data-username') : null;

    if (username) {
        loadAndDisplayFiles(username);
        showChart(username);
        setInterval(() => loadAndDisplayFiles(username), 1000);
    } else {
        console.error('Username is not defined.');
    }

    window.toggleSection = function(sectionId) {
        const sections = document.querySelectorAll('.content-section');
        sections.forEach(section => {
            if (section.id === sectionId) {
                if (section.style.display === "none" || section.style.display === "") {
                    section.style.display = "block";
                    section.classList.add("active");
                } else {
                    section.classList.remove("active");
                    setTimeout(() => {
                        section.style.display = "none";
                    }, 500);
                }
            } else {
                section.classList.remove("active");
                setTimeout(() => {
                    section.style.display = "none";
                }, 500);
            }
        });

        const chartContainer = document.getElementById('chartContainer');
        if (sectionId !== 'chartContainer') {
            chartContainer.style.display = 'none';
        } else {
            chartContainer.style.display = 'block';
            showChart(username);
        }
    };

function toggleSection(sectionId) {
    const sections = document.querySelectorAll('.content-section');
    const targetSection = document.getElementById(sectionId);

    sections.forEach(section => {
        if (section === targetSection) {
            section.classList.toggle('hidden');
            if (!section.classList.contains('hidden')) {
                section.classList.add('flexible');
            } else {
                section.classList.remove('flexible');
            }
        } else {
            section.classList.add('hidden');
            section.classList.remove('flexible');
        }
    });
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

    function showChart(username) {
        fetch(`/api/data/${username}/pf`)
            .then(response => response.json())
            .then(data => {
                const chartContainer = document.getElementById('myChart').getContext('2d');
                const noDataElement = document.getElementById('noData');
                const info = document.getElementById('info');

                if (!data.Total_scan || data.Total_scan === 0) {
                    chartContainer.canvas.style.display = 'none';
                    noDataElement.style.display = 'block';
                    info.innerHTML = '';
                } else {
                    chartContainer.canvas.style.display = 'block';
                    noDataElement.style.display = 'none';

                    const chart = new Chart(chartContainer, {
                        type: 'doughnut',
                        data: {
                            labels: ['Критические', 'Нежелательные', 'Информационые'],
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
                }
            })
            .catch(error => {
                console.error('Ошибка при загрузке данных:', error);
            });
    }
});




function loadAndDisplayFiles(username) {
    fetch(`/api/get-html-files/${username}`)
        .then(response => response.json())
        .then(files => {
            let container = document.getElementById('files-container');
            let html = files.map(file => {
                const displayName = file.replace(/\.html$/, '');
                return `<a href="/users/${username}/${file}" target="_blank">${displayName}</a>`;
            }).join('<br>');
            container.innerHTML = html;
        })
        .catch(error => console.error('Ошибка при загрузке файлов:', error));
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
            document.getElementById('scannerStatus').textContent = "Вы будете перенаправленны после ";
        })
        .catch((error) => {
            console.error('Error:', error);
        });
}

