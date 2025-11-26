# Backend PortfolioX

backend PortfolioX — API Django REST pour gérer les utilisateurs et les portfolios.

## Vue d'ensemble
Ce dépôt contient le backend de PortfolioX, construit avec Django 4.2+ et Django REST Framework. L'architecture est modulaire (applications `utilisateur` et `portfolio`) et s'appuie sur JWT pour l'authentification.

Arborescence principale
```
Backend_PortfolioX/
├── Backend_PortfolioX/             # Configuration Django
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── utilisateur/                     # Gestion des utilisateurs
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   └── admin.py
├── portfolio/                       # Gestion des portfolios
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   └── admin.py
└── manage.py
```

## Prérequis dans le fichier requirement.txt a installer

          python3 -m pip install -r requirements.txt  
          
## Packages / dépendances essentielles
Le projet s'appuie sur les paquets suivants (doivent figurer dans votre requirements.txt ou être installés) :
- django
- djangorestframework
- djangorestframework-simplejwt
- django-cors-headers
- django-filter

Exemple d'installation :
```bash
python -m pip install django djangorestframework djangorestframework-simplejwt django-cors-headers django-filter
```

## Installation rapide
1. Cloner le projet
```bash
git clone [url-du-repo]
cd Backend_PortfolioX
```
2. Créer et activer un environnement virtuel, installer les dépendances
3. Appliquer les migrations
```bash
python3 manage.py makemigrations
python3 manage.py migrate
```
4. Créer un superutilisateur
```bash
python3 manage.py createsuperuser
```
5. Lancer le serveur de développement
```bash
python3 manage.py runserver
```
6. Accéder aux endpoints (exemples) :
- API racine : http://127.0.0.1:8000/api/
- Admin Django : http://127.0.0.1:8000/admin/

## Paramètres importants (extraits et expliqués depuis settings.py)
Les valeurs et comportements ci‑dessous sont ceux définis dans settings.py et doivent être connus lors du déploiement ou du développement.

- SECRET_KEY
  - Présent dans settings.py mais NE DOIT PAS ÊTRE committé dans un dépôt public.
  - Recommandation : utiliser une variable d'environnement pour SECRET_KEY en production.

- DEBUG
  - Defaut: True (pour dev)
  - En production, définir DEBUG=False et configurer correctement ALLOWED_HOSTS.

- ALLOWED_HOSTS
  - Par défaut : ['localhost', '127.0.0.1', '0.0.0.0']
  - Adapter en production.

- DATABASES
  - Par défaut : sqlite3 avec fichier `db.sqlite3` dans BASE_DIR.
  - Remplacer par PostgreSQL/MySQL en production si nécessaire.

- AUTH_USER_MODEL
  - 'utilisateur.Utilisateur'
  - Le projet utilise un modèle utilisateur personnalisé nommé `Utilisateur`. Tenir compte de ce réglage lors des migrations et des fixtures.

- INSTALLED_APPS (essentiels à connaître)
  - django.contrib.* (admin, auth, sessions, messages, staticfiles, contenttypes)
  - rest_framework
  - rest_framework_simplejwt
  - rest_framework_simplejwt.token_blacklist
  - corsheaders
  - django_filters
  - utilisateur
  - portfolio

- MIDDLEWARE (ordre important)
  - `corsheaders.middleware.CorsMiddleware` doit être présent (et idéalement en tête de liste si utilisé).
  - Les middlewares Django standards (SecurityMiddleware, SessionMiddleware, CommonMiddleware, CsrfViewMiddleware, AuthenticationMiddleware, MessageMiddleware, XFrameOptionsMiddleware).

- CORS (configuration backend)
  - CORS_ALLOW_ALL_ORIGINS = True
  - CORS_ALLOW_CREDENTIALS = True
  - Note : en développement autoriser tout peut être pratique, mais en production préférez CORS_ALLOWED_ORIGINS explicite.

- REST_FRAMEWORK (configuration importante)
  - DEFAULT_AUTHENTICATION_CLASSES :
    - 'rest_framework_simplejwt.authentication.JWTAuthentication'
    - 'rest_framework.authentication.SessionAuthentication'
    - 'rest_framework.authentication.BasicAuthentication'
  - DEFAULT_PERMISSION_CLASSES :
    - 'rest_framework.permissions.IsAuthenticatedOrReadOnly'
  - DEFAULT_FILTER_BACKENDS :
    - 'django_filters.rest_framework.DjangoFilterBackend'
    - 'rest_framework.filters.SearchFilter'
    - 'rest_framework.filters.OrderingFilter'
  - Pagination :
    - DEFAULT_PAGINATION_CLASS : 'rest_framework.pagination.PageNumberPagination'
    - PAGE_SIZE : 20

- SIMPLE_JWT (paramètres)
  - ACCESS_TOKEN_LIFETIME : 1 day
  - REFRESH_TOKEN_LIFETIME : 7 days
  - ROTATE_REFRESH_TOKENS : False
  - BLACKLIST_AFTER_ROTATION : False
  - UPDATE_LAST_LOGIN : True
  - AUTH_HEADER_TYPES : ('Bearer',)
  - USER_ID_FIELD : 'id_utilisateur'    ← important : champ PK personnalisé dans votre modèle Utilisateur
  - USER_ID_CLAIM : 'user_id'

- Fichiers statiques et médias
  - STATIC_URL = '/static/'
  - STATIC_ROOT = BASE_DIR / 'staticfiles'
  - MEDIA_URL = '/media/'
  - MEDIA_ROOT = BASE_DIR / 'media'
  - Note : `collectstatic` est requis pour déploiement si DEBUG=False :
    ```bash
    python3 manage.py collectstatic
    ```
