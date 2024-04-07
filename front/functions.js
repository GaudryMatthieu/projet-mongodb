function addTask(form) {
    console.log("creation");
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
            clearLocalStorage();
            window.location.href = 'index.html';
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
                    displayContent(task.title, task.description, task._id, task.color, task.day);
                });

                dataContainer.appendChild(button);
                dataContainer.appendChild(document.createElement("br"));
            });
        })
        .catch(error => {
            console.error('Erreur:', error);
        });
}

function displayContent(title, description, id, color, day) {
    const parentCell = document.getElementById(day);
    const modal = document.createElement('div');
    modal.classList.add('modal', 'bg-gray-800', 'bg-opacity-50', 'border', 'border-gray-900', 'p-8');

    const modalContent = document.createElement('div');
    modalContent.classList.add('modal-content');

    const modalTitle = document.createElement('h5');
    modalTitle.textContent = title;
    modalTitle.classList.add('mb-2', 'text-2xl', 'font-bold', 'tracking-tight', 'text-gray-900', 'dark:text-white');
    modalContent.appendChild(modalTitle);

    const modalDescription = document.createElement('p');
    modalDescription.textContent = description;
    modalDescription.classList.add('mb-3', 'font-normal', 'text-gray-700', 'dark:text-gray-400');
    modalContent.appendChild(modalDescription);

    const deleteButton = document.createElement('button');
    deleteButton.textContent = 'Supprimer';
    deleteButton.className = "focus:outline-none text-white bg-red-700 hover:bg-red-800 focus:ring-4 focus:ring-red-300 font-medium rounded-lg text-sm px-5 py-2.5 me-2 mb-2 dark:bg-red-600 dark:hover:bg-red-700 dark:focus:ring-red-900";
    deleteButton.setAttribute('data-task-id', id);
    deleteButton.addEventListener('click', function () {
        deleteTask(id);
    });
    modalContent.appendChild(deleteButton);

    const updateButton = document.createElement('button');
    updateButton.textContent = 'Modifier';
    updateButton.className = "focus:outline-none text-white bg-yellow-700 hover:bg-yellow-800 focus:ring-4 focus:ring-yellow-300 font-medium rounded-lg text-sm px-5 py-2.5 me-2 mb-2 dark:bg-yellow-600 dark:hover:bg-yellow-700 dark:focus:ring-yellow-900";
    updateButton.setAttribute('data-task-id', id);
    updateButton.addEventListener('click', function () {
        openFormToUpdateTask(id, title, description, color, day);
    });
    modalContent.appendChild(updateButton);

    modal.appendChild(modalContent);
    parentCell.appendChild(modal);
    modal.style.display = 'block';

    window.addEventListener('click', function (event) {
        if (event.target !== modal && !modal.contains(event.target)) {
            hideModal();
        }
    });
}

function hideModal() {
    const modal = document.querySelector('.modal');
    if (modal) {
        modal.style.display = 'none';
    }
}

document.addEventListener('click', function(event) {
    const modal = document.querySelector('.modal');
    if (modal && event.target !== modal && !modal.contains(event.target)) {
        hideModal();
    }
});



async function deleteTask(id) {
    console.log('Tentative de suppression de la tâche avec l\'ID:', id);
    try {
        const response = await fetch("http://localhost:5000/delete/" + id, {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json'
            }
        });
        if (!response.ok) {
            throw new Error('Erreur lors de la suppression de la tâche');
        }
        const data = await response.json();
        console.log('Réponse du serveur après la suppression:', data);
        // Vérifier la réponse du serveur
        if (data.message === 'Document supprimé avec succès') {
            // Si la suppression est réussie, mettre à jour les données
            console.log('La tâche a été supprimée avec succès. Rechargement des données.');
            await location.reload();
        } else {
            // Gérer les cas où la suppression échoue
            console.error('Erreur lors de la suppression de la tâche:', data.error);
        }
    } catch (error) {
        console.error('Erreur:', error);
    }
}

async function readAll() {
    try {
        const response = await fetch(`http://localhost:5000/readAll/`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json'
            }
        });
        if (!response.ok) {
            throw new Error('Erreur lors de la demande');
        }
        const data = await response.json();
        // Effacer le contenu actuel de la section
        document.querySelectorAll('.task-container').forEach(container => container.innerHTML = '');

        data.forEach(task => {
            const dataContainer = document.querySelector(task.day);
            if (!dataContainer) {
                console.error("Container introuvable pour le jour spécifié :", task.day);
                return;
            }

            const button = document.createElement('button');
            button.textContent = task.title;
            button.className = "focus:outline-none text-white bg-green-700 hover:bg-green-800 focus:ring-4 focus:ring-green-300 font-medium rounded-lg text-sm px-5 py-2.5 me-2 mb-2 dark:bg-green-600 dark:hover:bg-green-700 dark:focus:ring-green-800";
            button.addEventListener('click', () => {
                displayContent(task.title, task.description, task._id);
            });

            dataContainer.appendChild(button);
            dataContainer.appendChild(document.createElement("br"));
        });
    } catch (error) {
        console.error('Erreur:', error);
    }
}

function openFormToUpdateTask(id, title, description, color, day) {
    // Stocker les données dans le stockage local
    localStorage.setItem('taskId', id);
    localStorage.setItem('taskTitle', title);
    localStorage.setItem('taskDescription', description);
    localStorage.setItem('taskColor', color);
    localStorage.setItem('taskDay', day);

    // Rediriger vers form.html
    window.location.href = 'form.html';
}

async function updateTask(id, day, title, color, description) {
    try {
        const updatedData = { id, day, title, color, description }; // Créez un objet avec les données mises à jour

        const response = await fetch(`http://localhost:5000/update/${id}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(updatedData) // Convertissez les données en format JSON
        });

        if (!response.ok) {
            throw new Error('Erreur lors de la mise à jour de la tâche');
        }

        const data = await response.json();
        console.log('Réponse du serveur après la mise à jour :', data);

        localStorage.clear(); // Effacez le stockage local après la mise à jour
        window.location.href = 'index.html'; // Redirigez l'utilisateur vers la page index.html
    } catch (error) {
        console.error('Erreur :', error);
    }
}


