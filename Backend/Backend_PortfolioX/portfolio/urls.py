from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

app_name = 'portfolio'

# Création du router pour les ViewSets
router = DefaultRouter()

# ==========================================================================
# ROUTES AUTOMATIQUES DES VIEWSETS
# ==========================================================================

# Contacts - CRUD complet: GET, POST, PUT, PATCH, DELETE
router.register(r'contacts', views.ContactViewSet, basename='contact')

# Compétences - CRUD complet: GET, POST, PUT, PATCH, DELETE  
router.register(r'competences', views.CompetenceViewSet, basename='competence')

# Projets - CRUD complet: GET, POST, PUT, PATCH, DELETE
router.register(r'projets', views.ProjetViewSet, basename='projet')

# Portfolios - CRUD complet avec actions personnalisées
router.register(r'portfolios', views.PortfolioViewSet, basename='portfolio')

# ==========================================================================
# URLS PERSONNALISÉES (EN PLUS DES VIEWSETS)
# ==========================================================================

urlpatterns = [
    # ==========================================================================
    # INCLUSION DES ROUTES AUTOMATIQUES DES VIEWSETS
    # ==========================================================================
    path('', include(router.urls)),
    
    # ==========================================================================
    # ENDPOINTS SPÉCIFIQUES POUR PORTFOLIO
    # ==========================================================================
    
    # GET - Mon portfolio (utilisateur connecté)
    path('portfolios/my/', 
         views.PortfolioViewSet.as_view({'get': 'my_portfolio'}), 
         name='my_portfolio'),
    
    # GET - Liste des portfolios publiés
    path('portfolios/published/', 
         views.PortfolioViewSet.as_view({'get': 'published'}), 
         name='published_portfolios'),
    
    # GET - Recherche avancée
    path('portfolios/search/', 
         views.PortfolioViewSet.as_view({'get': 'search'}), 
         name='portfolio_search'),
    
    # ==========================================================================
    # ACTIONS SUR UN PORTFOLIO SPÉCIFIQUE
    # ==========================================================================
    
    # POST - Publier/dépublier un portfolio
    path('portfolios/<int:pk>/publish/', 
         views.PortfolioViewSet.as_view({'post': 'publish'}), 
         name='publish_portfolio'),
    
    # GET - Statistiques d'un portfolio
    path('portfolios/<int:pk>/stats/', 
         views.PortfolioViewSet.as_view({'get': 'stats'}), 
         name='portfolio_stats'),
    
    # POST - Dupliquer un portfolio
    path('portfolios/<int:pk>/duplicate/', 
         views.PortfolioViewSet.as_view({'post': 'duplicate'}), 
         name='duplicate_portfolio'),
    
    # POST - Ajouter un contact existant au portfolio
    path('portfolios/<int:pk>/add-contact/', 
         views.PortfolioViewSet.as_view({'post': 'add_contact'}), 
         name='add_contact_to_portfolio'),
    
    # POST - Ajouter une compétence existante au portfolio
    path('portfolios/<int:pk>/add-competence/', 
         views.PortfolioViewSet.as_view({'post': 'add_competence'}), 
         name='add_competence_to_portfolio'),
    
    # POST - Ajouter un projet existant au portfolio
    path('portfolios/<int:pk>/add-projet/', 
         views.PortfolioViewSet.as_view({'post': 'add_projet'}), 
         name='add_projet_to_portfolio'),
    
    # ==========================================================================
    # ENDPOINTS SPÉCIAUX POUR COMPÉTENCES ET PROJETS
    # ==========================================================================
    
    # GET - Contacts principaux
    path('contacts/principaux/', 
         views.ContactViewSet.as_view({'get': 'principaux'}), 
         name='contacts_principaux'),
    
    # GET - Compétences par catégorie
    path('competences/par-categorie/', 
         views.CompetenceViewSet.as_view({'get': 'par_categorie'}), 
         name='competences_par_categorie'),
    
    # GET - Projets publics
    path('projets/publics/', 
         views.ProjetViewSet.as_view({'get': 'publics'}), 
         name='projets_publics'),
]

# ==========================================================================
# DOCUMENTATION DES ENDPOINTS DISPONIBLES
# ==========================================================================

"""
ENDPOINTS AUTOMATIQUES GÉNÉRÉS PAR LES VIEWSETS:

CONTACTS:
  GET    /api/portfolio/contacts/          - Liste tous les contacts
  POST   /api/portfolio/contacts/          - Créer un nouveau contact
  GET    /api/portfolio/contacts/{id}/     - Détails d'un contact
  PUT    /api/portfolio/contacts/{id}/     - Modifier complètement un contact
  PATCH  /api/portfolio/contacts/{id}/     - Modifier partiellement un contact
  DELETE /api/portfolio/contacts/{id}/     - Supprimer un contact

  ACTIONS PERSONNALISÉES:
  GET    /api/portfolio/contacts/principaux/ - Contacts principaux

COMPÉTENCES:
  GET    /api/portfolio/competences/       - Liste toutes les compétences
  POST   /api/portfolio/competences/       - Créer une nouvelle compétence
  GET    /api/portfolio/competences/{id}/  - Détails d'une compétence
  PUT    /api/portfolio/competences/{id}/  - Modifier complètement une compétence
  PATCH  /api/portfolio/competences/{id}/  - Modifier partiellement une compétence  
  DELETE /api/portfolio/competences/{id}/  - Supprimer une compétence

  ACTIONS PERSONNALISÉES:
  GET    /api/portfolio/competences/par-categorie/ - Compétences par catégorie

PROJETS:
  GET    /api/portfolio/projets/           - Liste tous les projets
  POST   /api/portfolio/projets/           - Créer un nouveau projet
  GET    /api/portfolio/projets/{id}/      - Détails d'un projet
  PUT    /api/portfolio/projets/{id}/      - Modifier complètement un projet
  PATCH  /api/portfolio/projets/{id}/      - Modifier partiellement un projet
  DELETE /api/portfolio/projets/{id}/      - Supprimer un projet

  ACTIONS PERSONNALISÉES:
  GET    /api/portfolio/projets/publics/   - Projets publics seulement

PORTFOLIOS (CRUD STANDARD):
  GET    /api/portfolio/portfolios/        - Liste tous les portfolios
  POST   /api/portfolio/portfolios/        - Créer un nouveau portfolio
  GET    /api/portfolio/portfolios/{id}/   - Détails d'un portfolio
  PUT    /api/portfolio/portfolios/{id}/   - Modifier complètement un portfolio
  PATCH  /api/portfolio/portfolios/{id}/   - Modifier partiellement un portfolio
  DELETE /api/portfolio/portfolios/{id}/   - Archiver un portfolio

PORTFOLIOS (ACTIONS PERSONNALISÉES):
  GET    /api/portfolio/portfolios/my/         - Mon portfolio (utilisateur connecté)
  GET    /api/portfolio/portfolios/published/  - Liste des portfolios publiés
  GET    /api/portfolio/portfolios/search/     - Recherche avancée
  
  ACTIONS SUR UN PORTFOLIO SPÉCIFIQUE:
  POST   /api/portfolio/portfolios/{id}/publish/      - Publier/dépublier
  GET    /api/portfolio/portfolios/{id}/stats/        - Statistiques
  POST   /api/portfolio/portfolios/{id}/duplicate/    - Dupliquer
  POST   /api/portfolio/portfolios/{id}/add-contact/  - Ajouter un contact
  POST   /api/portfolio/portfolios/{id}/add-competence/ - Ajouter une compétence
  POST   /api/portfolio/portfolios/{id}/add-projet/   - Ajouter un projet

FILTRES DISPONIBLES:
  Contacts: Aucun filtre spécifique
  Compétences: ?categorie=frontend, ?niveau_competence=avance, ?est_visible=true
  Projets: ?langage_projet=Python, ?est_public=true, ?est_termine=true
  Portfolios: ?statut=publie, ?utilisateur=1, ?competence=Python, ?langage=JavaScript

RECHERCHE (search_fields):
  Contacts: valeur_contact, utilisateur__prenom, utilisateur__nom
  Compétences: nom_competence, description
  Projets: titre_projet, description_projet, langage_projet
  Portfolios: titre, description, titre_professionnel, biographie

TRI (ordering_fields):
  Contacts: ordre, date_ajout
  Compétences: nom_competence, categorie, ordre, annees_experience
  Projets: titre_projet, date_realisation, ordre
  Portfolios: date_creation, date_modification, vue_count, titre

PAGINATION:
  Toutes les listes sont paginées (12 éléments par page)
  Modifier avec ?page_size=20
  Maximum: 100 éléments par page

PERMISSIONS:
  Contacts/Compétences/Projets: Lecture pour tous, écriture pour propriétaire/admin
  Portfolios: Lecture pour portfolios publiés, écriture pour propriétaire/admin
  Mon portfolio: Authentification requise
"""