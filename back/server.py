from flask import Flask, request, jsonify
from pymongo import MongoClient
from flask_cors import CORS, cross_origin
from bson import ObjectId
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

uri = "mongodb+srv://matthieugaudry78:matthieu@mongohexa.nag4wuq.mongodb.net/?retryWrites=true&w=majority&appName=mongohexa"

# crée un nouveau client et le co à la db
client = MongoClient(uri, server_api=ServerApi('1'))

try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

# Fonction pour se connecter à la base de données MongoDB
def connect_to_database(database_name):
    try:
        client.admin.command('ping')  # Vérifier la connexion en envoyant un ping
        print("Pinged your deployment. You successfully connected to MongoDB!")
        db = client[database_name]  # Accéder à la base de données spécifiée
        return db
    except Exception as e:
        print(e)
        return None  # Retourner None en cas d'échec de la connexion    

# Connexion à la base de données MongoDB
db = connect_to_database('hexamongo')

# Vérifier si la connexion a réussi
if db is not None:
    # Créer une collection pour stocker les références
    references_collection_name = 'references'
    references_collection = db.get_collection(references_collection_name)
    
    # Vérifier si la collection des références existe
    if references_collection.count_documents({}) == 0:
        # Insérer un document de référence bidon
        reference_doc = {'reference': 'reference'}
        references_collection.insert_one(reference_doc)
        # Récupérer l'ID du document de référence
        ref = reference_doc['_id']
else:
    # Gérer l'échec de la connexion à la base de données
    print("Failed to connect to MongoDB.")


# Définir une collection principale avec un schéma contraignant
schema = {
    'title': {'type': 'string'},
    'description': {'type': 'string'},
    'color': {'type': 'string'},
    'day': {'type': 'string'},
    'ref': {'bsonType': 'objectId'}
}

# Vérifier si la collection principale existe avant de la créer
collection_name = 'db-hexa'
if collection_name not in db.list_collection_names():
    collection = db.create_collection(
        collection_name,
        validator={
            '$jsonSchema': {
                'bsonType': 'object',
                'required': list(schema.keys()),
                'properties': schema
            }
        }
    )
    collection.create_index([('day', 1)])

# Si la collection principale existe déjà, obtenir une référence à cette collection
else:
    collection = db[collection_name]

app = Flask(__name__)
CORS(app)

# Définir une fonction pour la route "/create"
@app.route('/create', methods=['POST'])
@cross_origin()  # Autoriser les requêtes CORS pour cette route
def create():
    json_data = request.get_json()  # Récupère les données JSON de la demande
    reference_doc = references_collection.find_one({'reference': 'reference'})
    ref = reference_doc['_id']
    # Ajouter le champ ref à vos données JSON
    json_data['ref'] = ref
    collection.insert_one(json_data)  # Insère les données JSON dans la base de données
    return jsonify({'message': 'Données insérées avec succès'}), 200

# Définir une fonction pour la route "/readAll/<day>"
@app.route('/readAll/<string:day>', methods=['GET'])
@cross_origin()
def read_all_by_day(day):
    files = collection.find({"day": day})
    values = [{**file, "_id": str(file["_id"])} for file in files]

    # Supprimer le champ 'ref' de chaque dictionnaire
    for file in values:
        if 'ref' in file:
            del file['ref']
    if values:
        return jsonify(values), 200
    else:
        return jsonify({'message': 'Aucune donnée trouvée pour ce jour'}), 200

#lecture de tous les éléments en db
@app.route('/readAll/', methods=['GET'])
@cross_origin()  # Autoriser les requêtes CORS pour cette route
def read_all():
    files = collection.find()
    values = [{**file, "_id": str(file["_id"])} for file in files]
    if values:
        return jsonify(values), 200
    else:
        return jsonify({'message': 'Aucune donnée trouvée pour ce jour'}), 200
    
#lire un objet grace à son id
@app.route('/readAll/<string:id>', methods=['GET'])
@cross_origin()  # Autoriser les requêtes CORS pour cette route
def read():
    object_id = ObjectId(id)
    files = collection.find(object_id)
    values = [{**file, "_id": str(file["_id"])} for file in files]
    if values:
        return jsonify(values), 200  # Renvoyer les valeurs avec l'id converti en chaîne
    else:
        return jsonify({'message': 'Aucune donnée trouvée pour ce jour'}), 200
    

# modification d'un objet grace à l'id
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
            return jsonify({'error': 'Aucun document mis à jour. ID non trouvé.'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 200

# supprime l'objet grace à l'id
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
            return jsonify({'error': 'Aucun document supprimé. ID non trouvé.'}), 200
    except Exception as e:
        # Journalisez l'erreur pour le débogage
        print("Erreur lors de la suppression du document:", str(e))
        return jsonify({'error': 'Une erreur s\'est produite lors de la suppression du document.'}), 200


if __name__ == '__main__':
    # Exécuter l'application Flask sur le serveur local avec le port 5000
    app.run(debug=True)
