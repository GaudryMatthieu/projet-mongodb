from flask import Flask, request, jsonify
from pymongo import MongoClient
from flask_cors import CORS

# Connexion à la base de données MongoDB
client = MongoClient('mongodb://localhost:27017')
db = client['hexamongo']
collection = db['youhou']

app = Flask(__name__)
CORS(app)

# Définir une fonction pour la route "/page1"
@app.route('/page1', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        json_data = request.get_json()  # Récupère les données JSON de la demande
        collection.insert_one(json_data)  # Insère les données JSON dans la base de données
        return jsonify({'message': 'Données insérées avec succès'}), 200  # Répond avec un message de succès
    else:
        return 'Méthode GET acceptée pour la route /page1'

# Définir une fonction pour la route "/page2"
@app.route('/readAll', methods=['GET', 'POST'])
def read():
    if request.method == 'POST':
        collection.insert_one({"test":"test"})
        json_data = request.get_json()  # Récupère les données JSON de la demande
        day = json_data.get("day")  # Utilisation de .get() pour éviter une erreur si "day" n'est pas dans le JSON
        files = collection.find({"day": day})  # Correction pour utiliser la clé "day" dans la recherche
        return jsonify({'files': list(files)}), 200  # Conversion de "files" en liste pour jsonify
    else:
        return 'Méthode GET acceptée pour la route /readAll'


# Définir une fonction pour la route "/page3"
@app.route('/page3')
def contact():
    return 'Contactez-nous'

if __name__ == '__main__':
    # Exécuter l'application Flask sur le serveur local avec le port 5000
    app.run(debug=True)
