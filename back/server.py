from flask import Flask, request, jsonify
from pymongo import MongoClient

# Connexion à la base de données MongoDB
client = MongoClient('mongodb://localhost:27017')
db = client['hexamongo']
collection = db['youhou']

app = Flask(__name__)

# Définir une fonction pour la route "/page1"
@app.route('/page1', methods=['GET', 'POST'])
def receive_json():
    if request.method == 'POST':
        json_data = request.get_json()  # Récupère les données JSON de la demande
        print(json_data)  # Affiche les données JSON reçues
        collection.insert_one(json_data)  # Insère les données JSON dans la base de données
        return jsonify({'message': 'Données insérées avec succès'}), 200  # Répond avec un message de succès
    else:
        return 'Méthode GET acceptée pour la route /page1'

# Définir une fonction pour la route "/page2"
@app.route('/page2')
def about():
    return 'À propos de nous'

# Définir une fonction pour la route "/page3"
@app.route('/page3')
def contact():
    return 'Contactez-nous'

if __name__ == '__main__':
    # Exécuter l'application Flask sur le serveur local avec le port 5000
    app.run(debug=True)
