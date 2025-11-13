from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken  # Import pour gérer les tokens JWT
from django.contrib.auth import login
from .models import Utilisateur, Administrateur
from .serializers import (
    UtilisateurSerializer,
    UtilisateurInscriptionSerializer,
    UtilisateurConnexionSerializer,
    UtilisateurProfileSerializer,
    ChangementMotDePasseSerializer,
    AdministrateurSerializer
)

# Vue pour l'inscription des nouveaux utilisateurs
class InscriptionView(generics.CreateAPIView):
    queryset = Utilisateur.objects.all()  # Tous les utilisateurs peuvent s'inscrire
    serializer_class = UtilisateurInscriptionSerializer  # Serializer avec validation mot de passe
    permission_classes = [permissions.AllowAny]  # Accès public - pas besoin d'être connecté

# Vue de connexion - génère les tokens JWT
@api_view(['POST'])  # Seulement accessible via POST
@permission_classes([permissions.AllowAny])  # Public - pour se connecter
def connexion(request):
    serializer = UtilisateurConnexionSerializer(data=request.data)  # Valide email/mot de passe
    
    if serializer.is_valid():
        user = serializer.validated_data['user']  # Utilisateur authentifié
        
        # Générer les tokens JWT
        refresh = RefreshToken.for_user(user)  # Crée un nouveau token de rafraîchissement
        
        # Retourner les tokens et les informations utilisateur
        user_serializer = UtilisateurSerializer(user)
        return Response({
            'message': 'Connexion réussie',
            'user': user_serializer.data,  # Données de l'utilisateur
            'tokens': {
                'refresh': str(refresh),  # Token long terme pour rafraîchir
                'access': str(refresh.access_token),  # Token court terme pour les requêtes
            }
        }, status=status.HTTP_200_OK)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  # Erreurs de validation

# Vue de déconnexion - blacklist le token
@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])  # Seulement si connecté
def deconnexion(request):
    try:
        refresh_token = request.data.get('refresh_token')  # Récupère le token à blacklister
        if refresh_token:
            token = RefreshToken(refresh_token)
            token.blacklist()  # Ajoute le token à la blacklist - ne peut plus être utilisé
        
        return Response({'message': 'Déconnexion réussie'}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)  # Token invalide

# Vue pour récupérer le profil de l'utilisateur connecté
@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])  # Doit être connecté
def profil_utilisateur(request):
    serializer = UtilisateurProfileSerializer(request.user)  # Serializer l'utilisateur courant
    return Response(serializer.data)  # Retourne nom, prénom, email...

# Vue pour modifier le profil utilisateur
@api_view(['PUT'])
@permission_classes([permissions.IsAuthenticated])
def modifier_profil(request):
    serializer = UtilisateurProfileSerializer(
        request.user,  # Utilisateur à modifier
        data=request.data,  # Nouvelles données
        partial=True  # Permet modification partielle (PATCH)
    )
    
    if serializer.is_valid():
        serializer.save()  # Sauvegarde les modifications
        return Response(serializer.data)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Vue pour changer le mot de passe
@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def changer_mot_de_passe(request):
    serializer = ChangementMotDePasseSerializer(
        data=request.data, 
        context={'request': request}  # Passe l'utilisateur connecté au serializer
    )
    
    if serializer.is_valid():
        serializer.save()  # Hash et sauvegarde le nouveau mot de passe
        return Response({'message': 'Mot de passe modifié avec succès'})
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Vue ADMIN - Lister tous les utilisateurs
class UtilisateurListView(generics.ListAPIView):
    queryset = Utilisateur.objects.all()
    serializer_class = UtilisateurSerializer
    permission_classes = [permissions.IsAdminUser]  # Réservé aux administrateurs

# Vue ADMIN - Gérer un utilisateur spécifique
class UtilisateurDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Utilisateur.objects.all()
    serializer_class = UtilisateurSerializer
    permission_classes = [permissions.IsAdminUser]  # Admin seulement

# Vue pour rafraîchir le token JWT (quand access token expire)
@api_view(['POST'])
@permission_classes([permissions.AllowAny])  # Public car besoin de nouveau token
def rafraichir_token(request):
    refresh_token = request.data.get('refresh')  # Token de rafraîchissement
    
    if not refresh_token:
        return Response(
            {'error': 'Le token de rafraîchissement est requis'}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    try:
        refresh = RefreshToken(refresh_token)  # Vérifie le token
        new_access_token = str(refresh.access_token)  # Génère nouveau token d'accès
        
        return Response({
            'access': new_access_token  # Nouveau token pour continuer à utiliser l'API
        })
    except Exception as e:
        return Response(
            {'error': 'Token invalide'},  # Token expiré ou corrompu
            status=status.HTTP_400_BAD_REQUEST
        )