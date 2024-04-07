from flask import Flask, request, jsonify
from pymongo import MongoClient
from flask_cors import CORS, cross_origin
from bson import ObjectId

# Connexion à la base de données MongoDB
client = MongoClient('mongodb://localhost:27017')
db = client['hexamongo']

# Définir une collection avec un schéma contraignant
schema = {
    'title': {'type': 'string'},
    'description': {'type': 'string'},
    'color': {'type': 'string'},
    'day': {'type': 'string'}
}

# Vérifier si la collection existe avant de la créer
collection_name = 'db-hexa'
if collection_name not in db.list_collection_names():
    collection = db.create_collection(
        collection_name,
        validator={
            '$jsonSchema': {
                'bsonType': 'object',
                'required': list(schema.keys()),  # Assurez-vous que required est une liste
                'properties': schema
            }
        }
    )
    collection.create_index([('day', 1)])  # Ajouter un index sur le champ 'day'

# Si la collection existe déjà, obtenir une référence à cette collection
else:
    collection = db[collection_name]

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
def read_all_by_day(day):
    files = collection.find({"day": day})
    values = [{**file, "_id": str(file["_id"])} for file in files]
    if values:
        return jsonify(values), 200  # Renvoyer les valeurs avec l'id converti en chaîne
    else:
        return jsonify({'message': 'Aucune donnée trouvée pour ce jour'}), 404
    
@app.route('/readAll/', methods=['GET'])
@cross_origin()  # Autoriser les requêtes CORS pour cette route
def read_all():
    files = collection.find()
    values = [{**file, "_id": str(file["_id"])} for file in files]
    if values:
        return jsonify(values), 200  # Renvoyer les valeurs avec l'id converti en chaîne
    else:
        return jsonify({'message': 'Aucune donnée trouvée pour ce jour'}), 404
    
@app.route('/readAll/<string:id>', methods=['GET'])
@cross_origin()  # Autoriser les requêtes CORS pour cette route
def read():
    object_id = ObjectId(id)
    files = collection.find(object_id)
    values = [{**file, "_id": str(file["_id"])} for file in files]
    if values:
        return jsonify(values), 200  # Renvoyer les valeurs avec l'id converti en chaîne
    else:
        return jsonify({'message': 'Aucune donnée trouvée pour ce jour'}), 404
    

# Définir une fonction pour la route "/page3"
@app.route('/update/<string:id>', methods=['PUT'])
@cross_origin()    
def update(id):
    try:
        # Récupérer les données JSON envoyées avec la requête PUT
        data = request.get_json()
        object_id = ObjectId(id)
        
        # Utiliser l'ID fourni dans l'URL pour identifier le document à mettre à jour
        result = collection.update_one({"_id": object_id}, {"$set": data})

        if result.modified_count == 1:
            return jsonify({'message': 'Document mis à jour avec succès'}), 200
        else:
            return jsonify({'error': 'Aucun document mis à jour. ID non trouvé.'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/delete/<string:id>', methods=['DELETE'])
@cross_origin()  
def delete(id):
    try:
        # Convertir l'ID en ObjectId
        object_id = ObjectId(id)

        # Supprimer le document avec l'ID spécifié
        result = collection.delete_one({"_id": object_id})

        if result.deleted_count == 1:
            return jsonify({'message': 'Document supprimé avec succès'})
        else:
            return jsonify({'error': 'Aucun document supprimé. ID non trouvé.'}), 404
    except Exception as e:
        # Journalisez l'erreur pour le débogage
        print("Erreur lors de la suppression du document:", str(e))
        return jsonify({'error': 'Une erreur s\'est produite lors de la suppression du document.'}), 500


if __name__ == '__main__':
    # Exécuter l'application Flask sur le serveur local avec le port 5000
    app.run(debug=True)
