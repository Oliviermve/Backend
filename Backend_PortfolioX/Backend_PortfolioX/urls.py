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
                'profil': '/api/auth/profil/',
                'rafraichir_token': '/api/auth/rafraichir-token/'
            },
            'portfolios': {
                'liste_portfolios': '/api/portfolio/portfolios/',
                'mes_portfolios': '/api/portfolio/mes-portfolios/',
                'portfolios_publics': '/api/portfolio/public/portfolios/',
                'recherche': '/api/portfolio/public/recherche/'
            },
            'donnees': {
                'competences': '/api/portfolio/competences/',
                'projets': '/api/portfolio/projets/',
                'contacts': '/api/portfolio/contacts/',
                'templates': '/api/portfolio/templates/'
            }
        },
        'documentation': 'Consultez la documentation pour plus de détails'
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
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)