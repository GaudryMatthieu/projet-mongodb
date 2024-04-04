// functions.js
function myFunction() {
    // Votre code ici
    const dataToSend = { name: "datatest", status: "done" }

    fetch('http://localhost:5000/page1', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json' // Spécifiez le type de contenu comme étant JSON
        },
        body: JSON.stringify(dataToSend) // Convertissez vos données en JSON
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
