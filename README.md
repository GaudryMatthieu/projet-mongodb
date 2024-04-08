# ToDoList 

### Réalisé par Matthieu GAUDRY


## Description du projet :
Ce projet est une application de gestion de tâches personnelles. L'utilisateur peut ajouter, modifier ou supprimer ses tâches. Il peut également les consulter sur la page principale de l'application. En effet, la page s'articule comme un tableau avec les 7 jours de la semaine, à l'intérieur duquel sont listées les tâches du jour. Chaque tâche est cliquable pour ouvrir une modale sur l'écran principal, permettant d'accéder à plus d'informations sur la tâche.


## Guide pour l'API
- localhost:5000/create -> POST
- localhost:5000/readAll/{day} -> GET
- localhost:5000/readAll/ -> GET

- localhost:5000/readAll/{id} -> GET
- localhost:5000/update/{id} ->  PUT
- localhost:5000/delete/{id} -> DELETE

#### Exemple de fichier json stocké dans la base de donnée

```json
{
  "day": "mon",
  "title": "Projet Mongo DB",
  "color": "red",
  "description": "Héberger le site/ inclure un readme/ avoir un back propre/ ...",
  "ref": {
    "$oid": "6612bf4e398f7114cfd1b8e5"
  }
}
```