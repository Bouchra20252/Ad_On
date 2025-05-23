# Plateforme de Petites Annonces

Une plateforme complète permettant aux utilisateurs de publier et consulter des petites annonces pour l'achat, la vente ou l'échange de biens et services.

## Fonctionnalités

### Gestion des utilisateurs
- Inscription/connexion des utilisateurs
- Profils avec informations personnelles
- Historique des annonces et transactions
- Système de réputation

### Gestion des annonces
- Création, modification, suppression d'annonces
- Catégories et sous-catégories
- Upload de photos multiples
- Durée de publication et renouvellement

### Recherche et navigation
- Recherche par mots-clés
- Filtres avancés (prix, localisation, catégorie)
- Tri des résultats
- Annonces similaires

### Communication
- Messagerie interne entre utilisateurs
- Notifications de nouveaux messages
- Questions/réponses publiques sur les annonces
- Alertes pour nouvelles annonces correspondant aux critères

### Administration
- Modération des annonces
- Gestion des signalements
- Statistiques d'utilisation
- Mise en avant d'annonces premium

## Technologies utilisées

- Django (MVT)
- Base de données MySQL
- Django Forms pour les formulaires
- Django Authentication pour la gestion des utilisateurs
- Bootstrap pour l'interface utilisateur
- JavaScript pour l'interactivité

## Installation et configuration

1. Cloner le dépôt
```
git clone <repository-url>
cd plateforme_petites_annonces_project
```

2. Créer et activer un environnement virtuel
```
python -m venv venv
source venv/bin/activate  # Sur Windows : venv\Scripts\activate
```

3. Installer les dépendances
```
pip install -r requirements.txt
```

4. Configurer la base de données MySQL
   - Créer une base de données nommée `petites_annonces_db`
   - Configurer les paramètres d'accès dans `config/settings.py`

5. Appliquer les migrations
```
python manage.py migrate
```

6. Créer un superutilisateur pour l'administration
```
python manage.py createsuperuser
```

7. Lancer le serveur de développement
```
python manage.py runserver
```

## Structure du projet

- `config/` - Configuration principale du projet Django
- `petites_annonces/` - Application principale
  - `models.py` - Définition des modèles de données
  - `views.py` - Logique de traitement des requêtes
  - `forms.py` - Formulaires
  - `urls.py` - Configuration des routes
  - `templates/` - Templates HTML
  - `static/` - Fichiers statiques (CSS, JS, images)
- `static/` - Fichiers statiques globaux
- `media/` - Fichiers média uploadés par les utilisateurs

## Développement

### Commandes utiles

- Créer de nouvelles migrations après modification des modèles
```
python manage.py makemigrations
```

- Générer les scripts SQL des migrations
```
python manage.py sqlmigrate petites_annonces <migration_number>
```

- Vérifier les problèmes potentiels
```
python manage.py check
```

- Exécuter les tests
```
python manage.py test
```

## Déploiement en production

Pour un déploiement en production, plusieurs ajustements sont nécessaires :

1. Modifier les paramètres dans `settings.py` :
   - Définir `DEBUG = False`
   - Configurer `ALLOWED_HOSTS`
   - Sécuriser la clé secrète

2. Configurer un serveur web comme Nginx ou Apache

3. Configurer un serveur WSGI comme Gunicorn

4. Configurer une base de données robuste et optimisée

5. Mettre en place des certificats SSL pour HTTPS

## Licence

Ce projet est sous licence MIT. Voir le fichier LICENSE pour plus de détails. 