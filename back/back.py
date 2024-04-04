""" from pymongo import MongoClient

# Connexion au serveur MongoDB (par défaut, localhost:27017)
client = MongoClient()

# Sélection de la base de données
db = client.hexamongo

# Exemple : Accéder à une collection
collection = db.youhou

# Maintenant, vous pouvez effectuer des opérations sur la collection, par exemple :
result = collection.find_one({"a": 1})
print(result) """

from http.server import BaseHTTPRequestHandler, HTTPServer

# Créer une classe de gestionnaire de requêtes personnalisée
class RequestHandler(BaseHTTPRequestHandler):
    
    # Méthode pour traiter les requêtes GET
    def do_GET(self):
        
        self.custom_function()
        
        self.send_response(200)  # Code de réponse 200 (OK)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(b"<html><body><h1>Hello, World!</h1></body></html>")  # Réponse HTML


    def custom_function(self):
            print("It works")


# Définir l'adresse IP et le port du serveur
host = 'localhost'
port = 8080

# Créer une instance du serveur HTTP avec le gestionnaire de requêtes personnalisé
server = HTTPServer((host, port), RequestHandler)

# Afficher un message pour indiquer que le serveur est en cours d'écoute
print(f'Server listening on {host}:{port}')

# Démarrer le serveur et le maintenir en cours d'exécution jusqu'à ce qu'il soit arrêté
try:
    server.serve_forever()
except KeyboardInterrupt:
    server.shutdown()
    print('Server stopped.')

