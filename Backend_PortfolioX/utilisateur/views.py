from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.contrib.auth import login, authenticate, update_session_auth_hash
from django.contrib.auth.models import User
from .models import Utilisateur, Administrateur
from .serializers import (
    UtilisateurSerializer,
    UtilisateurInscriptionSerializer,
    UtilisateurConnexionSerializer,
    UtilisateurProfileSerializer,
    ChangementMotDePasseSerializer,
    AdministrateurSerializer
)

# =============================================================================
# VUES D'AUTHENTIFICATION
# =============================================================================

# Vue pour l'inscription des nouveaux utilisateurs
class InscriptionView(generics.CreateAPIView):
    queryset = Utilisateur.objects.all()
    serializer_class = UtilisateurInscriptionSerializer
    permission_classes = [permissions.AllowAny]

# Vue de connexion - génère les tokens JWT
@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def connexion(request):
    try:
        email = request.data.get('email')
        password = request.data.get('password')
        
        if not email or not password:
            return Response(
                {'error': 'Email et mot de passe requis'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Authentification
        user = authenticate(username=email, password=password)
        
        if user is not None:
            # ✅ GÉNÉRER DE VRAIS TOKENS JWT (sans blacklist)
            refresh = RefreshToken.for_user(user)
            
            return Response({
                'success': True,
                'message': 'Connexion réussie',
                'user': {
                    'id_utilisateur': user.id_utilisateur,
                    'email': user.email,
                    'nom': user.nom,
                    'prenom': user.prenom,
                    'telephone': getattr(user, 'telephone', ''),
                    'profession': getattr(user, 'profession', ''),
                    'bio': getattr(user, 'bio', '')
                },
                'access': str(refresh.access_token),  # ✅ Vrai token JWT
                'refresh': str(refresh)  # ✅ Token de rafraîchissement
            }, status=status.HTTP_200_OK)
        else:
            return Response(
                {'error': 'Email ou mot de passe incorrect'}, 
                status=status.HTTP_401_UNAUTHORIZED
            )
            
    except Exception as e:
        print("ERREUR CONNEXION:", str(e))
        return Response(
            {'error': f'Erreur lors de la connexion: {str(e)}'}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
# Vue de déconnexion - blacklist le token
@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([permissions.IsAuthenticated])
def deconnexion(request):
    try:
        refresh_token = request.data.get('refresh_token')
        if refresh_token:
            token = RefreshToken(refresh_token)
            token.blacklist()
        
        return Response({'message': 'Déconnexion réussie'}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

# Vue pour rafraîchir le token JWT
@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def rafraichir_token(request):
    refresh_token = request.data.get('refresh')
    
    if not refresh_token:
        return Response(
            {'error': 'Le token de rafraîchissement est requis'}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    try:
        refresh = RefreshToken(refresh_token)
        new_access_token = str(refresh.access_token)
        
        return Response({
            'access': new_access_token
        })
    except Exception as e:
        return Response(
            {'error': 'Token de rafraîchissement invalide'},
            status=status.HTTP_400_BAD_REQUEST
        )

# Vue pour vérifier le token
@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([permissions.IsAuthenticated])
def verifier_token(request):
    """Vérifier si le token est toujours valide"""
    return Response({
        'valid': True,
        'user': {
            'id_utilisateur': request.user.id_utilisateur,
            'email': request.user.email,
            'nom': request.user.nom,
            'prenom': request.user.prenom
        }
    })

# =============================================================================
# VUES DE PROFIL UTILISATEUR
# =============================================================================

# Vue pour récupérer le profil de l'utilisateur connecté
@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([permissions.IsAuthenticated])
def profil_utilisateur(request):
    serializer = UtilisateurProfileSerializer(request.user)
    return Response(serializer.data)

# Vue pour récupérer le profil complet utilisateur (avec statistiques)
@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([permissions.IsAuthenticated])
def user_profile(request):
    """Endpoint pour récupérer le profil complet avec statistiques"""
    try:
        user = request.user
        profile_data = {
            'id_utilisateur': user.id_utilisateur,
            'email': user.email,
            'nom': user.nom,
            'prenom': user.prenom,
            'telephone': getattr(user, 'telephone', ''),
            'profession': getattr(user, 'profession', ''),
            'bio': getattr(user, 'bio', ''),
            'portfolio_count': getattr(user, 'portfolios', []).count() if hasattr(user, 'portfolios') else 0,
            'created_at': user.date_joined,
            'last_login': user.last_login
        }
        return Response(profile_data)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

# Vue pour modifier le profil utilisateur
@api_view(['PUT'])
@authentication_classes([JWTAuthentication])
@permission_classes([permissions.IsAuthenticated])
def modifier_profil(request):
    serializer = UtilisateurProfileSerializer(
        request.user,
        data=request.data,
        partial=True
    )
    
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Vue pour mettre à jour les informations personnelles
@api_view(['PUT'])
@authentication_classes([JWTAuthentication])
@permission_classes([permissions.IsAuthenticated])
def update_profile(request):
    """Mettre à jour les informations personnelles de l'utilisateur"""
    try:
        user = request.user
        data = request.data
        
        # Mettre à jour les champs de base
        if 'firstname' in data:
            user.prenom = data['firstname']
        if 'lastname' in data:
            user.nom = data['lastname']
        if 'email' in data:
            user.email = data['email']
        if 'phone' in data:
            user.telephone = data['phone']
        if 'profession' in data:
            user.profession = data['profession']
        if 'bio' in data:
            user.bio = data['bio']
        
        user.save()
        
        # Retourner les données mises à jour
        updated_data = {
            'firstname': user.prenom,
            'lastname': user.nom,
            'email': user.email,
            'phone': getattr(user, 'telephone', ''),
            'profession': getattr(user, 'profession', ''),
            'bio': getattr(user, 'bio', '')
        }
        
        return Response({
            'message': 'Profil mis à jour avec succès',
            'user': updated_data
        })
        
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

# Vue pour modifier les coordonnées utilisateur
@api_view(['PUT'])
@authentication_classes([JWTAuthentication])
@permission_classes([permissions.IsAuthenticated])
def modifier_coordonnees(request):
    """Modifier les coordonnées de l'utilisateur (email, téléphone, etc.)"""
    try:
        user = request.user
        data = request.data
        
        # Mettre à jour les champs autorisés
        if 'email' in data:
            user.email = data['email']
        if 'telephone' in data:
            user.telephone = data['telephone']
        if 'profession' in data:
            user.profession = data['profession']
        if 'bio' in data:
            user.bio = data['bio']
        
        user.save()
        
        return Response({
            'message': 'Coordonnées mises à jour avec succès',
            'user': {
                'email': user.email,
                'telephone': getattr(user, 'telephone', ''),
                'profession': getattr(user, 'profession', ''),
                'bio': getattr(user, 'bio', '')
            }
        })
        
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

# =============================================================================
# VUES DE GESTION DES MOTS DE PASSE
# =============================================================================

# Vue pour changer le mot de passe (avec sérialiseur)
@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([permissions.IsAuthenticated])
def changer_mot_de_passe(request):
    serializer = ChangementMotDePasseSerializer(
        data=request.data, 
        context={'request': request}
    )
    
    if serializer.is_valid():
        serializer.save()
        return Response({'message': 'Mot de passe modifié avec succès'})
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Vue pour changer le mot de passe (version alternative)
@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([permissions.IsAuthenticated])
def change_password(request):
    """Changer le mot de passe de l'utilisateur"""
    try:
        current_password = request.data.get('current_password')
        new_password = request.data.get('new_password')
        confirm_password = request.data.get('confirm_password')
        
        # Validation
        if not current_password or not new_password or not confirm_password:
            return Response(
                {'error': 'Tous les champs sont obligatoires'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
            
        if new_password != confirm_password:
            return Response(
                {'error': 'Les nouveaux mots de passe ne correspondent pas'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
            
        # Vérifier l'ancien mot de passe
        if not request.user.check_password(current_password):
            return Response(
                {'error': 'Mot de passe actuel incorrect'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
            
        # Changer le mot de passe
        request.user.set_password(new_password)
        request.user.save()
        
        # Mettre à jour la session pour éviter la déconnexion
        update_session_auth_hash(request, request.user)
        
        return Response({'message': 'Mot de passe changé avec succès'})
        
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

# Vue pour réinitialiser le mot de passe (oublié)
@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def reset_password(request):
    """Réinitialiser le mot de passe (mot de passe oublié)"""
    try:
        email = request.data.get('email')
        
        if not email:
            return Response(
                {'error': 'Email requis'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Vérifier si l'utilisateur existe
        try:
            user = Utilisateur.objects.get(email=email)
        except Utilisateur.DoesNotExist:
            return Response(
                {'error': 'Aucun utilisateur trouvé avec cet email'}, 
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Ici vous pouvez implémenter la logique d'envoi d'email de réinitialisation
        return Response({
            'message': 'Email de réinitialisation envoyé avec succès',
            'email': email
        })
        
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

# =============================================================================
# VUES DE GESTION DES PORTFOLIOS
# =============================================================================

# Vue pour récupérer les portfolios de l'utilisateur
@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([permissions.IsAuthenticated])
def user_portfolios(request):
    """Récupérer tous les portfolios de l'utilisateur"""
    try:
        # Supposons que vous avez un modèle Portfolio lié à Utilisateur
        portfolios = getattr(request.user, 'portfolios', []).all()
        
        portfolios_data = []
        for portfolio in portfolios:
            portfolios_data.append({
                'id': portfolio.id,
                'title': portfolio.titre,
                'description': portfolio.description,
                'template': portfolio.template,
                'is_published': portfolio.publie,
                'created_at': portfolio.date_creation,
                'updated_at': portfolio.date_modification
            })
        
        return Response(portfolios_data)
        
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

# =============================================================================
# VUES DE STATISTIQUES ET DONNÉES
# =============================================================================

# Vue pour obtenir les statistiques utilisateur
@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([permissions.IsAuthenticated])
def user_stats(request):
    """Obtenir les statistiques de l'utilisateur"""
    try:
        user = request.user
        
        stats = {
            'portfolio_count': getattr(user, 'portfolios', []).count() if hasattr(user, 'portfolios') else 0,
            'projects_count': 0,  # À adapter selon vos modèles
            'views_count': 0,     # À adapter selon vos modèles
            'likes_count': 0,     # À adapter selon vos modèles
            'member_since': user.date_joined,
            'last_login': user.last_login
        }
        
        return Response(stats)
        
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

# Vue pour exporter les données utilisateur
@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([permissions.IsAuthenticated])
def export_data(request):
    """Exporter toutes les données de l'utilisateur"""
    try:
        user = request.user
        
        # Récupérer toutes les données de l'utilisateur
        user_data = {
            'profile': {
                'nom': user.nom,
                'prenom': user.prenom,
                'email': user.email,
                'telephone': getattr(user, 'telephone', ''),
                'profession': getattr(user, 'profession', ''),
                'bio': getattr(user, 'bio', ''),
                'date_inscription': user.date_joined,
                'derniere_connexion': user.last_login
            },
            'portfolios': [],
            'activity': []  # À compléter avec d'autres données
        }
        
        return Response(user_data)
        
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

# =============================================================================
# VUES DE GESTION DU COMPTE
# =============================================================================

# Vue pour vérifier l'email
@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([permissions.IsAuthenticated])
def verify_email(request):
    """Vérifier l'adresse email de l'utilisateur"""
    try:
        # Ici vous pouvez implémenter la logique d'envoi d'email de vérification
        user = request.user
        
        # Simuler l'envoi d'email (à remplacer par votre logique réelle)
        return Response({
            'message': 'Email de vérification envoyé avec succès',
            'email': user.email
        })
        
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

# Vue pour supprimer le compte utilisateur
@api_view(['DELETE'])
@authentication_classes([JWTAuthentication])
@permission_classes([permissions.IsAuthenticated])
def delete_account(request):
    """Supprimer le compte utilisateur"""
    try:
        user = request.user
        password_confirmation = request.data.get('password')
        
        if not password_confirmation:
            return Response(
                {'error': 'Confirmation par mot de passe requise'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
            
        # Vérifier le mot de passe
        if not user.check_password(password_confirmation):
            return Response(
                {'error': 'Mot de passe incorrect'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Supprimer l'utilisateur
        user.delete()
        
        return Response({'message': 'Compte supprimé avec succès'})
        
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

# =============================================================================
# VUES ADMINISTRATEUR
# =============================================================================

# Vue ADMIN - Lister tous les utilisateurs
class UtilisateurListView(generics.ListAPIView):
    queryset = Utilisateur.objects.all()
    serializer_class = UtilisateurSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAdminUser]

# Vue ADMIN - Gérer un utilisateur spécifique
class UtilisateurDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Utilisateur.objects.all()
    serializer_class = UtilisateurSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAdminUser]