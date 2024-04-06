// functions.js
function addTask(form) {
    console.log("tete");
    const day = form.get("days");
    const title = form.get("title");
    const color = form.get("color");
    const description = form.get("description");

    const data = { "day": day, "title": title, "color": color, "description": description };

    fetch('http://localhost:5000/page1', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json' // Spécifiez le type de contenu comme étant JSON
        },
        body: JSON.stringify(data) // Convertissez vos données en JSON
    })
        .then(response => {
            if (!response.ok) {
                throw new Error('Erreur lors de la demande');
            }
            return response.json();
        })
        .then(data => {
            console.dir(data)
        })
        .catch(error => {
            console.error('Erreur:', error);
        });
}

function readTaskByDay(day) {
    fetch('http://localhost:5000/readAll/' + day, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json' // Spécifiez le type de contenu comme étant JSON
        }
    })
        .then(response => {
            if (!response.ok) {
                throw new Error('Erreur lors de la demande');
            }
            return response.json();
        })
        .then(data => {
            let premierElement = []
            if (data && data.length > 0) {
                // Accédez au premier élément du tableau
                premierElement = data[0];
            }
                // Utilisez le premier élément comme vous le souhaitez
                /* console.log(premierElement);
            } else {
                console.log('Aucune donnée n\'a été récupérée ou le tableau est vide');
            } */

            const dataContainer = document.querySelector("#" + day);
            //const dataToDisplay = data;
            dataContainer.textContent = premierElement["title"];
        })
        .catch(error => {
            console.error('Erreur:', error);
        });
}

