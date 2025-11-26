from rest_framework import generics, permissions, status, filters
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from django.db.models import Count
from django.contrib.auth import get_user_model
from .models import Contact, Competence, Projet, Template, Portfolio
from .serializers import (
    ContactSerializer, CompetenceSerializer, ProjetSerializer, TemplateSerializer,
    PortfolioListSerializer, PortfolioDetailSerializer, PortfolioCreateSerializer,
    PortfolioPublicSerializer, PortfolioPublierSerializer, PortfolioModifierSerializer,
    PortfolioAjouterProjetSerializer, PortfolioAjouterCompetenceSerializer,
    PortfolioAjouterContactSerializer, PortfolioUpdateSerializer,
    PortfolioManageCompetencesSerializer, PortfolioManageProjetsSerializer, 
    PortfolioManageContactsSerializer
)

# ============================================================================
# VIEWSETS COMPLETS POUR MODÈLES DE BASE
# ============================================================================

class ContactViewSet(ModelViewSet):
    """
    ViewSet complet pour les contacts (CRUD complet)
    """
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['type_contact']
    search_fields = ['valeur_contact']

class CompetenceViewSet(ModelViewSet):
    """
    ViewSet complet pour les compétences (CRUD complet)
    """
    queryset = Competence.objects.all()
    serializer_class = CompetenceSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['niveau_competence']
    search_fields = ['nom_competence']

class ProjetViewSet(ModelViewSet):
    """
    ViewSet complet pour les projets (CRUD complet)
    """
    queryset = Projet.objects.all()
    serializer_class = ProjetSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ['titre_projet', 'description_projet']

class TemplateViewSet(ModelViewSet):
    """
    ViewSet complet pour les templates (CRUD complet)
    """
    queryset = Template.objects.all()
    serializer_class = TemplateSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

# ============================================================================
# VIEWSET POUR PORTFOLIO
# ============================================================================

class PortfolioViewSet(ModelViewSet):
    """
    ViewSet complet pour les portfolios avec toutes les opérations CRUD
    """
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['statut', 'template']
    search_fields = ['titre', 'description']

    def get_queryset(self):
        if self.action == 'mes_portfolios':
            return Portfolio.objects.filter(utilisateur=self.request.user)
        return Portfolio.objects.all()

    def get_serializer_class(self):
        if self.action == 'create':
            return PortfolioCreateSerializer
        elif self.action == 'list':
            return PortfolioListSerializer
        elif self.action in ['update', 'partial_update']:
            return PortfolioUpdateSerializer
        return PortfolioDetailSerializer

    def perform_create(self, serializer):
        if self.request.user.is_authenticated:
            serializer.save(utilisateur=self.request.user)
        else:
            serializer.save()

    # ============================================================================
    # ACTIONS PERSONNALISÉES
    # ============================================================================

    @action(detail=True, methods=['patch'], permission_classes=[permissions.IsAuthenticated])
    def publier(self, request, pk=None):
        """Action pour publier un portfolio"""
        portfolio = self.get_object()
        if portfolio.utilisateur != request.user:
            return Response(
                {'error': 'Vous ne pouvez publier que vos propres portfolios.'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        serializer = PortfolioPublierSerializer(portfolio, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Portfolio publié avec succès'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['patch'], permission_classes=[permissions.IsAuthenticated])
    def modifier_design(self, request, pk=None):
        """Action pour modifier le design d'un portfolio"""
        portfolio = self.get_object()
        if portfolio.utilisateur != request.user:
            return Response(
                {'error': 'Accès non autorisé.'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        serializer = PortfolioModifierSerializer(portfolio, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Design modifié avec succès'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def ajouter_projet(self, request, pk=None):
        """Action pour ajouter un projet au portfolio"""
        portfolio = self.get_object()
        if portfolio.utilisateur != request.user:
            return Response(
                {'error': 'Accès non autorisé.'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        serializer = PortfolioAjouterProjetSerializer(portfolio, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Projet ajouté avec succès'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def ajouter_competence(self, request, pk=None):
        """Action pour ajouter une compétence au portfolio"""
        portfolio = self.get_object()
        if portfolio.utilisateur != request.user:
            return Response(
                {'error': 'Accès non autorisé.'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        serializer = PortfolioAjouterCompetenceSerializer(portfolio, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Compétence ajoutée avec succès'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def ajouter_contact(self, request, pk=None):
        """Action pour ajouter un contact au portfolio"""
        portfolio = self.get_object()
        if portfolio.utilisateur != request.user:
            return Response(
                {'error': 'Accès non autorisé.'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        serializer = PortfolioAjouterContactSerializer(portfolio, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Contact ajouté avec succès'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['put'], permission_classes=[permissions.IsAuthenticated])
    def gerer_competences(self, request, pk=None):
        """Action pour gérer l'ensemble des compétences du portfolio"""
        portfolio = self.get_object()
        if portfolio.utilisateur != request.user:
            return Response(
                {'error': 'Accès non autorisé.'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        serializer = PortfolioManageCompetencesSerializer(portfolio, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Compétences mises à jour avec succès'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['put'], permission_classes=[permissions.IsAuthenticated])
    def gerer_projets(self, request, pk=None):
        """Action pour gérer l'ensemble des projets du portfolio"""
        portfolio = self.get_object()
        if portfolio.utilisateur != request.user:
            return Response(
                {'error': 'Accès non autorisé.'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        serializer = PortfolioManageProjetsSerializer(portfolio, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Projets mis à jour avec succès'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['put'], permission_classes=[permissions.IsAuthenticated])
    def gerer_contacts(self, request, pk=None):
        """Action pour gérer l'ensemble des contacts du portfolio"""
        portfolio = self.get_object()
        if portfolio.utilisateur != request.user:
            return Response(
                {'error': 'Accès non autorisé.'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        serializer = PortfolioManageContactsSerializer(portfolio, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Contacts mis à jour avec succès'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def mes_portfolios(self, request):
        """Action pour lister les portfolios de l'utilisateur connecté"""
        portfolios = Portfolio.objects.filter(utilisateur=request.user)
        serializer = PortfolioListSerializer(portfolios, many=True)
        return Response(serializer.data)

# ============================================================================
# VUES SPÉCIALISÉES POUR ACCÈS PUBLIC
# ============================================================================

class PortfolioPublicViewSet(ModelViewSet):
    """
    ViewSet public pour l'accès aux portfolios publiés (lecture seule)
    """
    queryset = Portfolio.objects.filter(statut='publie')
    serializer_class = PortfolioPublicSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = [
        'titre', 'description', 'utilisateur__prenom', 'utilisateur__nom',
        'competences__nom_competence', 'projets__titre_projet'
    ]
    ordering_fields = ['date_creation', 'titre']
    ordering = ['-date_creation']
    
    # Désactiver les méthodes non autorisées pour le public
    def create(self, request, *args, **kwargs):
        return Response(
            {'error': 'Création non autorisée pour les utilisateurs publics'},
            status=status.HTTP_403_FORBIDDEN
        )
    
    def update(self, request, *args, **kwargs):
        return Response(
            {'error': 'Modification non autorisée pour les utilisateurs publics'},
            status=status.HTTP_403_FORBIDDEN
        )
    
    def destroy(self, request, *args, **kwargs):
        return Response(
            {'error': 'Suppression non autorisée pour les utilisateurs publics'},
            status=status.HTTP_403_FORBIDDEN
        )

# ============================================================================
# VUES SPÉCIALISÉES POUR RECHERCHE AVANCÉE
# ============================================================================

class PortfolioSearchView(generics.ListAPIView):
    """
    Vue avancée pour la recherche dans les portfolios publics
    """
    serializer_class = PortfolioPublicSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [filters.SearchFilter]
    search_fields = [
        'titre', 'description', 'utilisateur__prenom', 'utilisateur__nom',
        'competences__nom_competence', 'projets__titre_projet'
    ]
    
    def get_queryset(self):
        queryset = Portfolio.objects.filter(statut='publie')
        
        # Filtrage additionnel par compétences
        competences = self.request.query_params.get('competences', None)
        if competences:
            competences_list = competences.split(',')
            queryset = queryset.filter(competences__nom_competence__in=competences_list).distinct()
        
        return queryset

# ============================================================================
# VUES POUR STATISTIQUES ET ADMIN
# ============================================================================

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def portfolio_statistiques(request):
    """
    Vue pour les statistiques générales de la plateforme
    """
    total_portfolios = Portfolio.objects.count()
    portfolios_publies = Portfolio.objects.filter(statut='publie').count()
    portfolios_brouillon = Portfolio.objects.filter(statut='brouillon').count()
    total_competences = Competence.objects.count()
    total_projets = Projet.objects.count()
    total_templates = Template.objects.count()
    total_contacts = Contact.objects.count()
    
    # Statistiques par utilisateur
    if request.user.is_authenticated:
        mes_portfolios = Portfolio.objects.filter(utilisateur=request.user).count()
        mes_portfolios_publies = Portfolio.objects.filter(utilisateur=request.user, statut='publie').count()
    else:
        mes_portfolios = 0
        mes_portfolios_publies = 0
    
    return Response({
        'platforme': {
            'total_portfolios': total_portfolios,
            'portfolios_publies': portfolios_publies,
            'portfolios_brouillon': portfolios_brouillon,
            'total_competences': total_competences,
            'total_projets': total_projets,
            'total_templates': total_templates,
            'total_contacts': total_contacts
        },
        'utilisateur': {
            'mes_portfolios': mes_portfolios,
            'mes_portfolios_publies': mes_portfolios_publies
        }
    })

@api_view(['GET'])
@permission_classes([permissions.IsAdminUser])
def admin_statistiques(request):
    """
    Vue pour les statistiques administrateur
    """
    User = get_user_model()
    
    # Utilisateurs avec le plus de portfolios
    top_utilisateurs = User.objects.annotate(
        portfolio_count=Count('portfolio')
    ).order_by('-portfolio_count')[:10]
    
    # Compétences les plus populaires
    competences_populaires = Competence.objects.annotate(
        portfolio_count=Count('portfolio')
    ).order_by('-portfolio_count')[:10]
    
    # Templates les plus utilisés
    templates_populaires = Template.objects.annotate(
        portfolio_count=Count('portfolio')
    ).order_by('-portfolio_count')[:10]
    
    return Response({
        'top_utilisateurs': [
            {
                'utilisateur': user.prenom + ' ' + user.nom,
                'portfolio_count': user.portfolio_count
            } for user in top_utilisateurs
        ],
        'competences_populaires': [
            {
                'competence': comp.nom_competence,
                'portfolio_count': comp.portfolio_count
            } for comp in competences_populaires
        ],
        'templates_populaires': [
            {
                'template': temp.nom_template,
                'portfolio_count': temp.portfolio_count
            } for temp in templates_populaires
        ]
    })

# ============================================================================
# VUE DE TEST ET SANTÉ DE L'API
# ============================================================================

@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def test_api(request):
    """
    Vue de test pour vérifier que l'API portfolio fonctionne
    """
    return Response({
        'message': 'API Portfolio fonctionne correctement !',
        'endpoints_disponibles': [
            'GET /api/portfolio/contacts/ - CRUD Contacts',
            'GET /api/portfolio/competences/ - CRUD Compétences',
            'GET /api/portfolio/projets/ - CRUD Projets',
            'GET /api/portfolio/templates/ - CRUD Templates',
            'GET /api/portfolio/portfolios/ - CRUD Portfolios',
            'GET /api/portfolio/portfolios/public/ - Portfolios publics',
            'GET /api/portfolio/portfolios/mes-portfolios/ - Mes portfolios',
            'POST /api/portfolio/portfolios/{id}/publier/ - Publier portfolio',
            'POST /api/portfolio/portfolios/{id}/ajouter-projet/ - Ajouter projet',
            'POST /api/portfolio/portfolios/{id}/ajouter-competence/ - Ajouter compétence',
            'POST /api/portfolio/portfolios/{id}/ajouter-contact/ - Ajouter contact'
        ]
    })

@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def api_sante(request):
    """
    Vue pour vérifier la santé de l'API portfolio
    """
    portfolios_count = Portfolio.objects.count()
    competences_count = Competence.objects.count()
    projets_count = Projet.objects.count()
    templates_count = Template.objects.count()
    contacts_count = Contact.objects.count()
    
    return Response({
        'status': 'healthy',
        'message': 'API Portfolio fonctionne correctement !',
        'statistiques': {
            'portfolios': portfolios_count,
            'competences': competences_count,
            'projets': projets_count,
            'templates': templates_count,
            'contacts': contacts_count
        }
    })