// functions.js
function addTask(form) {
    console.log("tete");
    const day = form.get("days");
    const title = form.get("title");
    const color = form.get("color");
    const description = form.get("description");

    const data = {"day": day, "title": title, "color": color, "description": description};
    //console.dir(data);

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
            console.log(data);
        })
        .catch(error => {
            console.error('Erreur:', error);
        });

}

function readTaskByDay(day){
    console.log("tete");
    const data =  {'day': day};

    fetch('http://127.0.0.1:5000/readAll', {
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
            console.log(data);
        })
        .catch(error => {
            console.error('Erreur:', error);
        });
}
