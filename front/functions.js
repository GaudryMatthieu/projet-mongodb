function addTask(form) {
    const day = form.get("days");
    const title = form.get("title");
    const color = form.get("color");
    const description = form.get("description");

    const data = { day, title, color, description };

    fetch('http://localhost:5000/page1', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
        .then(response => {
            if (!response.ok) {
                throw new Error('Erreur lors de la demande');
            }
            return response.json();
        })
        .then(data => {
            console.dir(data);
        })
        .catch(error => {
            console.error('Erreur:', error);
        });
}

function readTaskByDay(day) {
    fetch(`http://localhost:5000/readAll/${day}`, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json'
        }
    })
        .then(response => {
            if (!response.ok) {
                throw new Error('Erreur lors de la demande');
            }
            return response.json();
        })
        .then(data => {
            const dataContainer = document.querySelector(`#${day}`);
            if (!dataContainer) {
                console.error("Container introuvable pour le jour spécifié :", day);
                return;
            }

            data.forEach(task => {
                const button = document.createElement('button');
                button.textContent = task.title;
                button.className = "focus:outline-none text-white bg-green-700 hover:bg-green-800 focus:ring-4 focus:ring-green-300 font-medium rounded-lg text-sm px-5 py-2.5 me-2 mb-2 dark:bg-green-600 dark:hover:bg-green-700 dark:focus:ring-green-800";
                button.addEventListener('click', () => {
                    displayContent();
                });

                dataContainer.appendChild(button);
                dataContainer.appendChild(document.createElement("br"));
            });
        })
        .catch(error => {
            console.error('Erreur:', error);
        });
}

function displayContent() {
    document.querySelector('#modal').style.display = 'block';
}

function hideModal() {
    document.querySelector('#modal').style.display = 'none';
}

// Masquer la boîte modale lorsque l'utilisateur clique en dehors
document.querySelector('.modal').addEventListener('click', function(event) {
    if (event.target === this) {
        hideModal();
    }
});