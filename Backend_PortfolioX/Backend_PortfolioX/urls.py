"""
URL configuration for Backend_PortfolioX project.
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import TokenVerifyView
from rest_framework.decorators import api_view
from rest_framework.response import Response

# Vue racine de l'API - remplace api_root.urls
@api_view(['GET'])
def api_root(request):
    """
    Page d'accueil de l'API PortfolioX
    Affiche tous les endpoints disponibles
    """
    return Response({
        'message': '🚀 Bienvenue sur l\'API PortfolioX',
        'description': 'Plateforme de création de portfolios en ligne',
        'version': '1.0',
        'endpoints': {
            'administration': {
                'admin': '/admin/',
                'verification_token': '/api/token/verify/'
            },
            'authentification': {
                'inscription': '/api/auth/inscription/',
                'connexion': '/api/auth/connexion/',
                'deconnexion': '/api/auth/deconnexion/',
                'rafraichir_token': '/api/auth/rafraichir-token/',
                'verifier_token': '/api/auth/verifier-token/',
                'profil': '/api/auth/profil/',
                'modifier_profil': '/api/auth/profil/modifier/',
                'statistiques': '/api/auth/profil/stats/',
                'exporter_donnees': '/api/auth/profil/export/',
                'changer_mot_de_passe': '/api/auth/changer-mot-de-passe/',
                'reinitialiser_mot_de_passe': '/api/auth/reinitialiser-mot-de-passe/',
                'verifier_email': '/api/auth/verifier-email/',
                'modifier_coordonnees': '/api/auth/coordonnees/',
                'supprimer_compte': '/api/auth/supprimer-compte/',
                'mes_portfolios': '/api/auth/portfolios/'
            },
            'administration_utilisateurs': {
                'liste_utilisateurs': '/api/auth/admin/utilisateurs/',
                'detail_utilisateur': '/api/auth/admin/utilisateurs/<int:pk>/'
            },
            'portfolios': {
                'crud_portfolios': {
                    'liste_portfolios': 'GET    /api/portfolio/portfolios/',
                    'creer_portfolio': 'POST   /api/portfolio/portfolios/',
                    'detail_portfolio': 'GET    /api/portfolio/portfolios/{id}/',
                    'modifier_portfolio': 'PUT    /api/portfolio/portfolios/{id}/',
                    'modifier_partiel': 'PATCH  /api/portfolio/portfolios/{id}/',
                    'supprimer_portfolio': 'DELETE /api/portfolio/portfolios/{id}/'
                },
                'actions_portfolios': {
                    'mes_portfolios': 'GET    /api/portfolio/portfolios/mes-portfolios/',
                    'publier_portfolio': 'PATCH  /api/portfolio/portfolios/{id}/publier/',
                    'modifier_design': 'PATCH  /api/portfolio/portfolios/{id}/modifier_design/',
                    'ajouter_projet': 'POST   /api/portfolio/portfolios/{id}/ajouter_projet/',
                    'ajouter_competence': 'POST   /api/portfolio/portfolios/{id}/ajouter_competence/',
                    'ajouter_contact': 'POST   /api/portfolio/portfolios/{id}/ajouter_contact/',
                    'gerer_competences': 'PUT    /api/portfolio/portfolios/{id}/gerer_competences/',
                    'gerer_projets': 'PUT    /api/portfolio/portfolios/{id}/gerer_projets/',
                    'gerer_contacts': 'PUT    /api/portfolio/portfolios/{id}/gerer_contacts/'
                },
                'portfolios_publics': {
                    'liste_publics': 'GET    /api/portfolio/public/portfolios/',
                    'detail_public': 'GET    /api/portfolio/public/portfolios/{id}/'
                }
            },
            'competences': {
                'liste_competences': 'GET    /api/portfolio/competences/',
                'creer_competence': 'POST   /api/portfolio/competences/',
                'detail_competence': 'GET    /api/portfolio/competences/{id}/',
                'modifier_competence': 'PUT    /api/portfolio/competences/{id}/',
                'modifier_partiel': 'PATCH  /api/portfolio/competences/{id}/',
                'supprimer_competence': 'DELETE /api/portfolio/competences/{id}/'
            },
            'projets': {
                'liste_projets': 'GET    /api/portfolio/projets/',
                'creer_projet': 'POST   /api/portfolio/projets/',
                'detail_projet': 'GET    /api/portfolio/projets/{id}/',
                'modifier_projet': 'PUT    /api/portfolio/projets/{id}/',
                'modifier_partiel': 'PATCH  /api/portfolio/projets/{id}/',
                'supprimer_projet': 'DELETE /api/portfolio/projets/{id}/'
            },
            'contacts': {
                'liste_contacts': 'GET    /api/portfolio/contacts/',
                'creer_contact': 'POST   /api/portfolio/contacts/',
                'detail_contact': 'GET    /api/portfolio/contacts/{id}/',
                'modifier_contact': 'PUT    /api/portfolio/contacts/{id}/',
                'modifier_partiel': 'PATCH  /api/portfolio/contacts/{id}/',
                'supprimer_contact': 'DELETE /api/portfolio/contacts/{id}/'
            },
            'templates': {
                'liste_templates': 'GET    /api/portfolio/templates/',
                'creer_template': 'POST   /api/portfolio/templates/',
                'detail_template': 'GET    /api/portfolio/templates/{id}/',
                'modifier_template': 'PUT    /api/portfolio/templates/{id}/',
                'modifier_partiel': 'PATCH  /api/portfolio/templates/{id}/',
                'supprimer_template': 'DELETE /api/portfolio/templates/{id}/'
            },
            'utilitaires': {
                'test_api': 'GET    /api/portfolio/test/',
                'statistiques': 'GET    /api/portfolio/statistiques/',
                'statistiques_admin': 'GET    /api/portfolio/admin-stats/',
                'sante_api': 'GET    /api/portfolio/sante/',
                'recherche_public': 'GET    /api/portfolio/public/recherche/'
            }
        },
        'documentation': {
            'authentification_requise': 'Les endpoints marqués nécessitent une authentification JWT',
            'format_token': 'Utiliser le header: Authorization: Bearer <votre_token>',
            'filtres_disponibles': 'La plupart des endpoints supportent le filtrage et la recherche',
            'pagination': 'Toutes les listes sont paginées (20 éléments par page)'
        }
    })

urlpatterns = [
    # Interface d'administration Django
    path('admin/', admin.site.urls),
    
    # API Authentication JWT
    path('api/auth/', include('utilisateur.urls')),
    
    # API Portfolio
    path('api/portfolio/', include('portfolio.urls')),
    
    # Vérification de token JWT
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    
    # API Root - Utilise la vue locale au lieu d'inclure api_root.urls
    path('api/', api_root, name='api_root'),
]

# Servir les fichiers médias en développement
# Ajouter les fichiers statiques seulement en mode DEBUG
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)