from django.urls import path
from . import views

app_name = 'portfolio'

urlpatterns = [
    # ==========================================================================
    # ENDPOINTS DE TEST ET STATISTIQUES
    # ==========================================================================
    
    # GET - Test de l'API portfolio
    path('test/', views.test_api, name='test_api'),
    
    # GET - Statistiques générales de la plateforme
    path('statistiques/', views.portfolio_statistiques, name='statistiques'),
    
    # ==========================================================================
    # ENDPOINTS PORTFOLIOS (GESTION PERSONNELLE)
    # ==========================================================================
    
    # GET - Liste tous les portfolios | POST - Créer un nouveau portfolio
    path('portfolios/', views.PortfolioListCreateView.as_view(), name='portfolio_list_create'),
    
    # GET, PUT, PATCH, DELETE - Gestion d'un portfolio spécifique
    path('portfolios/<int:pk>/', views.PortfolioDetailView.as_view(), name='portfolio_detail'),
    
    # PATCH - Publier un portfolio (changer statut en "publié")
    path('portfolios/<int:pk>/publier/', views.PortfolioPublierView.as_view(), name='portfolio_publier'),
    
    # PATCH - Modifier le design d'un portfolio (titre, description, template)
    path('portfolios/<int:pk>/modifier/', views.PortfolioModifierView.as_view(), name='portfolio_modifier'),
    
    # GET - Liste des portfolios de l'utilisateur connecté
    path('mes-portfolios/', views.MesPortfoliosListView.as_view(), name='mes_portfolios'),
    
    # ==========================================================================
    # ENDPOINTS AJOUT D'ÉLÉMENTS AU PORTFOLIO
    # ==========================================================================
    
    # POST - Ajouter un projet à un portfolio
    path('portfolios/<int:pk>/ajouter-projet/', views.ajouter_projet_portfolio, name='ajouter_projet'),
    
    # POST - Ajouter une compétence à un portfolio
    path('portfolios/<int:pk>/ajouter-competence/', views.ajouter_competence_portfolio, name='ajouter_competence'),
    
    # POST - Ajouter un contact à un portfolio
    path('portfolios/<int:pk>/ajouter-contact/', views.ajouter_contact_portfolio, name='ajouter_contact'),
    
    # ==========================================================================
    # ENDPOINTS PORTFOLIOS PUBLICS (ACCÈS LIBRE)
    # ==========================================================================
    
    # GET - Liste tous les portfolios publiés (accès public)
    path('public/portfolios/', views.PortfolioPublicListView.as_view(), name='portfolios_publics'),
    
    # GET - Détails d'un portfolio publié (accès public)
    path('public/portfolios/<int:pk>/', views.PortfolioPublicDetailView.as_view(), name='portfolio_public_detail'),
    
    # GET - Recherche dans les portfolios publics
    path('public/recherche/', views.PortfolioSearchView.as_view(), name='recherche_portfolios'),
    
    # GET - Portfolios d'un utilisateur spécifique
    path('utilisateurs/<int:utilisateur_id>/portfolios/', views.PortfolioUtilisateurListView.as_view(), name='portfolios_utilisateur'),
    
    # ==========================================================================
    # ENDPOINTS COMPÉTENCES
    # ==========================================================================
    
    # GET - Liste toutes les compétences | POST - Créer une compétence
    path('competences/', views.CompetenceListCreateView.as_view(), name='competence_list_create'),
    
    # GET, PUT, PATCH, DELETE - Gestion d'une compétence spécifique
    path('competences/<int:pk>/', views.CompetenceDetailView.as_view(), name='competence_detail'),
    
    # ==========================================================================
    # ENDPOINTS PROJETS
    # ==========================================================================
    
    # GET - Liste tous les projets | POST - Créer un projet
    path('projets/', views.ProjetListCreateView.as_view(), name='projet_list_create'),
    
    # GET, PUT, PATCH, DELETE - Gestion d'un projet spécifique
    path('projets/<int:pk>/', views.ProjetDetailView.as_view(), name='projet_detail'),
    
    # ==========================================================================
    # ENDPOINTS CONTACTS
    # ==========================================================================
    
    # GET - Liste tous les contacts | POST - Créer un contact
    path('contacts/', views.ContactListCreateView.as_view(), name='contact_list_create'),
    
    # GET, PUT, PATCH, DELETE - Gestion d'un contact spécifique
    path('contacts/<int:pk>/', views.ContactDetailView.as_view(), name='contact_detail'),
    
    # ==========================================================================
    # ENDPOINTS TEMPLATES
    # ==========================================================================
    
    # GET - Liste tous les templates | POST - Créer un template
    path('templates/', views.TemplateListCreateView.as_view(), name='template_list_create'),
    
    # GET, PUT, PATCH, DELETE - Gestion d'un template spécifique
    path('templates/<int:pk>/', views.TemplateDetailView.as_view(), name='template_detail'),
]