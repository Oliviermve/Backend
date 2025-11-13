# Backend
backend porfolioX


### Prérequis
- Python 3.8+
- Django 4.2+
- Django REST Framework + simple JWT token 


# Architectire modulaire Backend

Backend_PortfolioX/
├── Backend_PortfolioX/             # Configuration Django
│ ├── settings.py
│ ├── urls.py
│ └── wsgi.py
├─── utilisateur/               # Gestion des utilisateurs
│ ├── models.py
│ ├── serializers.py
│ ├── views.py
│ └── admin.py
├── portfolio/                   # Gestion des portfolios
│ ├── models.py
│ ├── serializers.py
│ ├── views.py
│ └── admin.py
└── manage.py

## 📊 Modèles de Données

### Utilisateur
- `id_utilisateur` (Primary Key)
- `nom`, `prenom`, `email`
- `date_joined`, `last_login`

### Administrateur (Hérite de Utilisateur)
- `id_administrateur` (Primary Key)

### Portfolio
- `id_portfolio` (Primary Key)
- `utilisateur` (OneToOne)
- `template` (ForeignKey)
- `titre`, `description`, `statut`
- Relations ManyToMany: `competences`, `contacts`, `projets`

### Compétence
- `id_competence` (Primary Key)
- `nom_competence`, `niveau_competence`

### Contact
- `id_contact` (Primary Key)
- `type_contact`, `valeur_contact`

### Projet
- `id_projet` (Primary Key)
- `titre_projet`, `description_projet`
- `langage_projet`, `lien_projet`, `image_projet`

### Template
- `id_template` (Primary Key)
- `nom_template`, `description_template`
- `fichier_html`, `image_template`

## Sécurité Implémentée

Mesures de protection :

    Mots de passe hashés (bcrypt)

    Tokens JWT avec expiration

    Blacklisting des tokens révoqués

    Validation CORS pour le frontend

    Protection CSRF pour sessions

    Rate limiting possible


## 🚀 Installation et Démarrage



### Installation

1. Cloner le projet
```bash
git clone [url-du-repo]
cd Backend_PortfolioX

2. appliquer les migrations si tu utilise "python3"

python3 manage.py makemigrations
python3 manage.py migrate

3. creer un super utilisateur(Administrateur)

python3 manage.py createsuperuser

4. lancer le serveur

python3 manage.py runserver


5. dans le navigateur lancer lancer l'URL en ajoutant /api/  pour voir toute les endpoints disponible

exemple http://127.0.0.1:8000/api/


