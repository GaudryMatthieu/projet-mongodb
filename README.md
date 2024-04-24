# ToDoList 

### Réalisé par Matthieu GAUDRY


## Description du projet :
Ce projet est une application de gestion de tâches personnelles. L'utilisateur peut ajouter, modifier ou supprimer ses tâches. Il peut également les consulter sur la page principale de l'application. En effet, la page s'articule comme un tableau avec les 7 jours de la semaine, à l'intérieur duquel sont listées les tâches du jour. Chaque tâche est cliquable pour ouvrir une modale sur l'écran principal, permettant d'accéder à plus d'informations sur la tâche.


## Guide pour l'API

### Routes
- localhost:5000/create -> POST
- localhost:5000/readAll/{day} -> GET
- localhost:5000/readAll/ -> GET

- localhost:5000/readAll/{id} -> GET
- localhost:5000/update/{id} ->  PUT
- localhost:5000/delete/{id} -> DELETE

### Optimisations
2 index :
   - id
   - day

### Schéma

Vous pouvez retrouvez un schéma qui correspond à la donnée juste en dessous avec donc le jour, le titre, la description, la couleur ainsi que la référence.

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

### Bibliothèques utilisées

Pour le côté back, j'utilise en environnement python pour avoir les dépendances nécessaires

**Package**      **Version**
------------ -------
blinker      1.7.0
click        8.1.7
colorama     0.4.6
dnspython    2.6.1
Flask        3.0.2
Flask-Cors   4.0.0
itsdangerous 2.1.2
Jinja2       3.1.3
MarkupSafe   2.1.5
pip          24.0
pymongo      4.6.3
Werkzeug     3.0.2

