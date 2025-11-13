from rest_framework import generics, permissions, status, filters
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from .models import Contact, Competence, Projet, Template, Portfolio
from .serializers import (
    ContactSerializer,
    CompetenceSerializer,
    ProjetSerializer,
    TemplateSerializer,
    PortfolioListSerializer,
    PortfolioDetailSerializer,
    PortfolioCreateSerializer,
    PortfolioPublicSerializer,
    PortfolioModifierSerializer,
    PortfolioPublierSerializer,
    PortfolioAjouterProjetSerializer,
    PortfolioAjouterCompetenceSerializer,
    PortfolioAjouterContactSerializer
)

# ============================================================================
# VUES POUR LES CONTACTS - Gestion des informations de contact
# ============================================================================

class ContactListCreateView(generics.ListCreateAPIView):
    """
    Vue pour lister tous les contacts et en créer de nouveaux
    GET: Liste tous les contacts
    POST: Créer un nouveau contact (email, téléphone, LinkedIn, etc.)
    """
    queryset = Contact.objects.all()  # Récupère tous les contacts de la base
    serializer_class = ContactSerializer  # Utilise le serializer Contact
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]  # Lecture publique, écriture authentifiée
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]  # Active filtrage et recherche
    filterset_fields = ['type_contact']  # Filtre par type (email, téléphone, etc.)
    search_fields = ['valeur_contact']  # Recherche dans la valeur du contact

class ContactDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Vue pour afficher, modifier ou supprimer un contact spécifique
    GET: Affiche les détails d'un contact
    PUT/PATCH: Modifie un contact existant
    DELETE: Supprime un contact
    """
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]  # Opérations sécurisées

# ============================================================================
# VUES POUR LES COMPÉTENCES - Gestion des compétences techniques
# ============================================================================

class CompetenceListCreateView(generics.ListCreateAPIView):
    """
    Vue pour lister et créer des compétences techniques
    GET: Liste toutes les compétences avec filtrage
    POST: Ajoute une nouvelle compétence (Python, Django, etc.)
    """
    queryset = Competence.objects.all()
    serializer_class = CompetenceSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['niveau_competence']  # Filtre par niveau (débutant, expert, etc.)
    search_fields = ['nom_competence']  # Recherche par nom de compétence
    ordering_fields = ['nom_competence', 'niveau_competence']  # Tri possible
    ordering = ['nom_competence']  # Tri par défaut par nom

class CompetenceDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Vue pour gérer une compétence spécifique
    Permet de voir, modifier ou supprimer une compétence
    """
    queryset = Competence.objects.all()
    serializer_class = CompetenceSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

# ============================================================================
# VUES POUR LES PROJETS - Gestion des projets personnels
# ============================================================================

class ProjetListCreateView(generics.ListCreateAPIView):
    """
    Vue pour lister et créer des projets personnels
    GET: Liste tous les projets avec recherche
    POST: Ajoute un nouveau projet (Site web, application, etc.)
    Correspond au cas d'utilisation "Ajouter projet"
    """
    queryset = Projet.objects.all()
    serializer_class = ProjetSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['titre_projet', 'description_projet', 'langage_projet']  # Recherche multi-champs
    ordering_fields = ['titre_projet']  # Tri par titre
    ordering = ['-id_projet']  # Plus récents en premier par défaut

class ProjetDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Vue pour gérer un projet spécifique
    Permet de modifier les détails d'un projet existant
    """
    queryset = Projet.objects.all()
    serializer_class = ProjetSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

# ============================================================================
# VUES POUR LES TEMPLATES - Gestion des modèles de portfolio
# ============================================================================

class TemplateListCreateView(generics.ListCreateAPIView):
    """
    Vue pour lister et créer des templates de portfolio
    GET: Liste tous les templates disponibles
    POST: Créer un nouveau template (admin seulement)
    Correspond au cas d'utilisation "Choisir template"
    """
    queryset = Template.objects.all()
    serializer_class = TemplateSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class TemplateDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Vue pour gérer un template spécifique
    GET: Voir les détails d'un template
    PUT/PATCH: Modifier un template (admin)
    DELETE: Supprimer un template (admin)
    """
    queryset = Template.objects.all()
    serializer_class = TemplateSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

# ============================================================================
# VUES PRINCIPALES POUR LES PORTFOLIOS
# ============================================================================

class PortfolioListCreateView(generics.ListCreateAPIView):
    """
    Vue principale pour lister et créer des portfolios
    GET: Liste tous les portfolios avec filtres avancés
    POST: Créer un nouveau portfolio (cas d'utilisation "Créer portfolio")
    """
    queryset = Portfolio.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['statut', 'template']  # Filtrage par statut et template
    search_fields = ['titre', 'description']  # Recherche texte
    ordering_fields = ['date_creation', 'titre']  # Tri possible
    ordering = ['-date_creation']  # Plus récents en premier
    
    def get_serializer_class(self):
        """
        Choisit le serializer approprié selon la méthode HTTP
        POST: Utilise PortfolioCreateSerializer pour la création
        GET: Utilise PortfolioListSerializer pour l'affichage liste
        """
        if self.request.method == 'POST':
            return PortfolioCreateSerializer
        return PortfolioListSerializer
    
    def perform_create(self, serializer):
        """
        Surcharge de la création pour assigner automatiquement l'utilisateur connecté
        Comme propriétaire du portfolio
        """
        if self.request.user.is_authenticated:
            serializer.save(utilisateur=self.request.user)  # Auto-assignation utilisateur
        else:
            serializer.save()

class PortfolioDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Vue détaillée pour un portfolio spécifique
    GET: Voir tous les détails d'un portfolio
    PUT/PATCH: Modifier un portfolio existant
    DELETE: Supprimer un portfolio
    """
    queryset = Portfolio.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    def get_serializer_class(self):
        """
        Choisit le serializer selon la méthode HTTP
        PUT/PATCH: Utilise PortfolioCreateSerializer pour la modification
        GET: Utilise PortfolioDetailSerializer pour l'affichage détaillé
        """
        if self.request.method in ['PUT', 'PATCH']:
            return PortfolioCreateSerializer
        return PortfolioDetailSerializer

# ============================================================================
# VUES SPÉCIALISÉES POUR LES ACTIONS MÉTIER
# ============================================================================

class PortfolioPublierView(generics.UpdateAPIView):
    """
    Vue spécialisée pour publier un portfolio
    PATCH: Change le statut en "publié" avec validations
    Correspond au cas d'utilisation "Publier/Partager portfolio"
    """
    queryset = Portfolio.objects.all()
    serializer_class = PortfolioPublierSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """
        Restreint aux portfolios de l'utilisateur connecté
        Un utilisateur ne peut publier que ses propres portfolios
        """
        return Portfolio.objects.filter(utilisateur=self.request.user)

class PortfolioModifierView(generics.UpdateAPIView):
    """
    Vue pour modifier le design d'un portfolio
    PATCH: Modifie titre, description ou template
    Correspond au cas d'utilisation "Modifier template"
    """
    queryset = Portfolio.objects.all()
    serializer_class = PortfolioModifierSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """Restreint aux portfolios de l'utilisateur connecté"""
        return Portfolio.objects.filter(utilisateur=self.request.user)

# ============================================================================
# VUES POUR L'AJOUT D'ÉLÉMENTS AU PORTFOLIO
# ============================================================================

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def ajouter_projet_portfolio(request, pk):
    """
    Vue pour ajouter un projet à un portfolio
    POST: Ajoute un projet existant ou crée un nouveau
    Correspond au cas d'utilisation "Ajouter projet"
    """
    portfolio = get_object_or_404(Portfolio, pk=pk, utilisateur=request.user)
    serializer = PortfolioAjouterProjetSerializer(portfolio, data=request.data, partial=True)
    
    if serializer.is_valid():
        serializer.save()
        return Response({'message': 'Projet ajouté avec succès'}, status=status.HTTP_200_OK)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def ajouter_competence_portfolio(request, pk):
    """
    Vue pour ajouter une compétence à un portfolio
    POST: Ajoute une compétence existante ou crée une nouvelle
    Correspond au cas d'utilisation "Ajouter compétence"
    """
    portfolio = get_object_or_404(Portfolio, pk=pk, utilisateur=request.user)
    serializer = PortfolioAjouterCompetenceSerializer(portfolio, data=request.data, partial=True)
    
    if serializer.is_valid():
        serializer.save()
        return Response({'message': 'Compétence ajoutée avec succès'}, status=status.HTTP_200_OK)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def ajouter_contact_portfolio(request, pk):
    """
    Vue pour ajouter un contact à un portfolio
    POST: Ajoute un contact existant ou crée un nouveau
    Correspond au cas d'utilisation "Ajouter contact"
    """
    portfolio = get_object_or_404(Portfolio, pk=pk, utilisateur=request.user)
    serializer = PortfolioAjouterContactSerializer(portfolio, data=request.data, partial=True)
    
    if serializer.is_valid():
        serializer.save()
        return Response({'message': 'Contact ajouté avec succès'}, status=status.HTTP_200_OK)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# ============================================================================
# VUES POUR LA CONSULTATION DES PORTFOLIOS
# ============================================================================

class PortfolioUtilisateurListView(generics.ListAPIView):
    """
    Vue pour lister les portfolios d'un utilisateur spécifique
    GET: Tous les portfolios d'un utilisateur donné
    """
    serializer_class = PortfolioListSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    def get_queryset(self):
        """Filtre par ID utilisateur"""
        utilisateur_id = self.kwargs['utilisateur_id']
        return Portfolio.objects.filter(utilisateur_id=utilisateur_id)

class MesPortfoliosListView(generics.ListAPIView):
    """
    Vue pour lister les portfolios de l'utilisateur connecté
    GET: Mes portfolios personnels
    """
    serializer_class = PortfolioListSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """Retourne uniquement les portfolios de l'utilisateur connecté"""
        return Portfolio.objects.filter(utilisateur=self.request.user)

# ============================================================================
# VUES PUBLIQUES (ACCÈS SANS AUTHENTIFICATION)
# ============================================================================

class PortfolioPublicListView(generics.ListAPIView):
    """
    Vue publique pour lister les portfolios publiés
    GET: Liste tous les portfolios avec statut "publié"
    Accès libre sans authentification
    """
    queryset = Portfolio.objects.filter(statut='publie')  # Seulement les publiés
    serializer_class = PortfolioPublicSerializer
    permission_classes = [permissions.AllowAny]  # Accès public
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['titre', 'description', 'utilisateur__prenom', 'utilisateur__nom']
    ordering_fields = ['date_creation']
    ordering = ['-date_creation']  # Plus récents en premier

class PortfolioPublicDetailView(generics.RetrieveAPIView):
    """
    Vue publique pour voir un portfolio publié
    GET: Détails complets d'un portfolio publié
    Accès libre sans authentification
    """
    queryset = Portfolio.objects.filter(statut='publie')  # Seulement les publiés
    serializer_class = PortfolioPublicSerializer
    permission_classes = [permissions.AllowAny]  # Accès public

class PortfolioSearchView(generics.ListAPIView):
    """
    Vue de recherche dans les portfolios publics
    GET: Recherche texte dans les portfolios publiés
    """
    serializer_class = PortfolioPublicSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [filters.SearchFilter]
    search_fields = [
        'titre', 
        'description',
        'competences__nom_competence',  # Recherche dans les compétences
        'projets__titre_projet',        # Recherche dans les projets
        'utilisateur__prenom',          # Recherche dans le prénom
        'utilisateur__nom'              # Recherche dans le nom
    ]
    
    def get_queryset(self):
        """Retourne seulement les portfolios publiés"""
        return Portfolio.objects.filter(statut='publie')

# ============================================================================
# VUES ADMIN ET STATISTIQUES
# ============================================================================

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def portfolio_statistiques(request):
    """
    Vue pour les statistiques générales de la plateforme
    GET: Retourne des chiffres clés (nombre portfolios, compétences, etc.)
    """
    total_portfolios = Portfolio.objects.count()
    portfolios_publies = Portfolio.objects.filter(statut='publie').count()
    portfolios_brouillon = Portfolio.objects.filter(statut='brouillon').count()
    total_competences = Competence.objects.count()
    total_projets = Projet.objects.count()
    
    return Response({
        'total_portfolios': total_portfolios,
        'portfolios_publies': portfolios_publies,
        'portfolios_brouillon': portfolios_brouillon,
        'total_competences': total_competences,
        'total_projets': total_projets
    })

# ============================================================================
# VUE DE TEST (à supprimer en production)
# ============================================================================

@api_view(['GET'])
def test_api(request):
    """
    Vue de test pour vérifier que l'API portfolio fonctionne
    À supprimer ou désactiver en environnement de production
    """
    return Response({
        'message': 'API Portfolio fonctionne correctement !',
        'endpoints_disponibles': [
            'GET /api/portfolio/portfolios/ - Liste portfolios',
            'POST /api/portfolio/portfolios/ - Créer portfolio',
            'GET /api/portfolio/public/portfolios/ - Portfolios publics',
            'GET /api/portfolio/competences/ - Liste compétences',
            'GET /api/portfolio/projets/ - Liste projets'
        ]
    })