from flask import Flask, request, jsonify
from pymongo import MongoClient
from flask_cors import CORS, cross_origin
import json
# Connexion à la base de données MongoDB
client = MongoClient('mongodb://localhost:27017')
db = client['hexamongo']
collection = db['youhou']

app = Flask(__name__)
CORS(app)

# Définir une fonction pour la route "/page1"
@app.route('/page1', methods=['POST'])

@cross_origin()  # Autoriser les requêtes CORS pour cette route
def create():
    json_data = request.get_json()  # Récupère les données JSON de la demande
    collection.insert_one(json_data)  # Insère les données JSON dans la base de données
    return jsonify({'message': 'Données insérées avec succès'}), 200  # Répond avec un message de succès

# Définir une fonction pour la route "/readAll/<day>"
@app.route('/readAll/<string:day>', methods=['GET'])
@cross_origin()  # Autoriser les requêtes CORS pour cette route
def read(day):
    files = collection.find({"day": day}, {"_id": 0})
    values = [file for file in files]  # Convertir les résultats en liste
    print(values)
    if values:
        return jsonify(values), 200  # Renvoyer les valeurs sans envelopper dans un autre dictionnaire
    else:
        return jsonify({'message': 'Aucune donnée trouvée pour ce jour'}), 404
    

# Définir une fonction pour la route "/page3"
@app.route('/page3')

@cross_origin()  # Autoriser les requêtes CORS pour cette route
def contact():
    return 'Contactez-nous'

if __name__ == '__main__':
    # Exécuter l'application Flask sur le serveur local avec le port 5000
    app.run(debug=True)
