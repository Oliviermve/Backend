# Backend
backend porfolioX


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

## 🚀 Installation et Démarrage

### Prérequis
- Python 3.8+
- Django 4.2+
- Django REST Framework

### Installation

1. Cloner le projet
```bash
git clone [url-du-repo]
cd Backend_PortfolioX

2. appliquer les migrations si tu utilise "python3"

python3 manage.py makemigrations
python3 manage.py migrate


3. lancer le serveur

python3 manage.py runserver


