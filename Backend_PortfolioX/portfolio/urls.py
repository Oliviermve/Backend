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

# Templates - CRUD complet: GET, POST, PUT, PATCH, DELETE
router.register(r'templates', views.TemplateViewSet, basename='template')

# Portfolios - CRUD complet avec actions personnalisées
router.register(r'portfolios', views.PortfolioViewSet, basename='portfolio')

# Portfolios publics - Lecture seule
router.register(r'public/portfolios', views.PortfolioPublicViewSet, basename='portfolio-public')

# ==========================================================================
# URLS PERSONNALISÉES (EN PLUS DES VIEWSETS)
# ==========================================================================

urlpatterns = [
    # ==========================================================================
    # INCLUSION DES ROUTES AUTOMATIQUES DES VIEWSETS
    # ==========================================================================
    path('', include(router.urls)),
    
    # ==========================================================================
    # ENDPOINTS DE TEST ET STATISTIQUES
    # ==========================================================================
    
    # GET - Test de l'API portfolio
    path('test/', views.test_api, name='test_api'),
    
    # GET - Statistiques générales de la plateforme
    path('statistiques/', views.portfolio_statistiques, name='statistiques'),
    
    # GET - Statistiques administrateur
    path('admin-stats/', views.admin_statistiques, name='admin_stats'),
    
    # GET - Santé de l'API
    path('sante/', views.api_sante, name='api_sante'),
    
    # ==========================================================================
    # ENDPOINTS SPÉCIALISÉS POUR RECHERCHE
    # ==========================================================================
    
    # GET - Recherche avancée dans les portfolios publics
    path('public/recherche/', views.PortfolioSearchView.as_view(), name='recherche_portfolios'),
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

COMPÉTENCES:
  GET    /api/portfolio/competences/       - Liste toutes les compétences
  POST   /api/portfolio/competences/       - Créer une nouvelle compétence
  GET    /api/portfolio/competences/{id}/  - Détails d'une compétence
  PUT    /api/portfolio/competences/{id}/  - Modifier complètement une compétence
  PATCH  /api/portfolio/competences/{id}/  - Modifier partiellement une compétence  
  DELETE /api/portfolio/competences/{id}/  - Supprimer une compétence

PROJETS:
  GET    /api/portfolio/projets/           - Liste tous les projets
  POST   /api/portfolio/projets/           - Créer un nouveau projet
  GET    /api/portfolio/projets/{id}/      - Détails d'un projet
  PUT    /api/portfolio/projets/{id}/      - Modifier complètement un projet
  PATCH  /api/portfolio/projets/{id}/      - Modifier partiellement un projet
  DELETE /api/portfolio/projets/{id}/      - Supprimer un projet

TEMPLATES:
  GET    /api/portfolio/templates/         - Liste tous les templates
  POST   /api/portfolio/templates/         - Créer un nouveau template
  GET    /api/portfolio/templates/{id}/    - Détails d'un template
  PUT    /api/portfolio/templates/{id}/    - Modifier complètement un template
  PATCH  /api/portfolio/templates/{id}/    - Modifier partiellement un template
  DELETE /api/portfolio/templates/{id}/    - Supprimer un template

PORTFOLIOS (CRUD + ACTIONS):
  GET    /api/portfolio/portfolios/                    - Liste tous les portfolios
  POST   /api/portfolio/portfolios/                    - Créer un nouveau portfolio
  GET    /api/portfolio/portfolios/{id}/               - Détails d'un portfolio
  PUT    /api/portfolio/portfolios/{id}/               - Modifier complètement un portfolio
  PATCH  /api/portfolio/portfolios/{id}/               - Modifier partiellement un portfolio
  DELETE /api/portfolio/portfolios/{id}/               - Supprimer un portfolio
  
  ACTIONS PERSONNALISÉES:
  GET    /api/portfolio/portfolios/mes-portfolios/     - Mes portfolios (utilisateur connecté)
  PATCH  /api/portfolio/portfolios/{id}/publier/       - Publier un portfolio
  PATCH  /api/portfolio/portfolios/{id}/modifier_design/ - Modifier le design
  POST   /api/portfolio/portfolios/{id}/ajouter_projet/  - Ajouter un projet
  POST   /api/portfolio/portfolios/{id}/ajouter_competence/ - Ajouter une compétence
  POST   /api/portfolio/portfolios/{id}/ajouter_contact/   - Ajouter un contact
  PUT    /api/portfolio/portfolios/{id}/gerer_competences/ - Gérer les compétences
  PUT    /api/portfolio/portfolios/{id}/gerer_projets/     - Gérer les projets
  PUT    /api/portfolio/portfolios/{id}/gerer_contacts/    - Gérer les contacts

PORTFOLIOS PUBLICS (LECTURE SEULE):
  GET    /api/portfolio/public/portfolios/             - Liste portfolios publiés
  GET    /api/portfolio/public/portfolios/{id}/        - Détails portfolio publié

ENDPOINTS PERSONNALISÉS:
  GET    /api/portfolio/test/              - Test de l'API
  GET    /api/portfolio/statistiques/      - Statistiques plateforme
  GET    /api/portfolio/admin-stats/       - Statistiques admin
  GET    /api/portfolio/sante/             - Santé de l'API
  GET    /api/portfolio/public/recherche/  - Recherche portfolios publics
"""