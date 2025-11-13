from django.urls import path
from rest_framework_simplejwt.views import TokenVerifyView
from . import views

urlpatterns = [
    # Authentification
    path('inscription/', views.InscriptionView.as_view(), name='inscription'),
    path('connexion/', views.connexion, name='connexion'),
    path('deconnexion/', views.deconnexion, name='deconnexion'),
    path('rafraichir-token/', views.rafraichir_token, name='rafraichir_token'),
    path('verifier-token/', TokenVerifyView.as_view(), name='verifier_token'),
    
    # Profil utilisateur
    path('profil/', views.profil_utilisateur, name='profil_utilisateur'),
    path('profil/modifier/', views.modifier_profil, name='modifier_profil'),
    path('changer-mot-de-passe/', views.changer_mot_de_passe, name='changer_mot_de_passe'),
    
    # Gestion des utilisateurs (admin seulement)
    path('utilisateurs/', views.UtilisateurListView.as_view(), name='liste_utilisateurs'),
    path('utilisateurs/<int:pk>/', views.UtilisateurDetailView.as_view(), name='detail_utilisateur'),
]