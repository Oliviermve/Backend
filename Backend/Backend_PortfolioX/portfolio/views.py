# portfolio/views.py
from rest_framework import viewsets, status, permissions, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from django.db.models import Q
from django.db import transaction
from django.utils import timezone

from .models import Contact, Competence, Projet, Portfolio
from .serializers import (
    ContactSerializer,
    CompetenceSerializer,
    ProjetSerializer,
    PortfolioListSerializer,
    PortfolioDetailSerializer,
    PortfolioCreateUpdateSerializer,
    PortfolioPublishSerializer
)

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 12
    page_size_query_param = 'page_size'
    max_page_size = 100

class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        # CORRECTION : Utiliser request.user directement
        return obj.utilisateur == request.user

class PortfolioPermissions(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_authenticated
    
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS and obj.is_published():
            return True
        # CORRECTION : Utiliser request.user directement
        return obj.utilisateur == request.user

class ContactViewSet(viewsets.ModelViewSet):
    serializer_class = ContactSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    pagination_class = StandardResultsSetPagination
    
    def get_queryset(self):
        # CORRECTION : Utiliser self.request.user directement
        if self.request.user.is_authenticated:
            return Contact.objects.filter(utilisateur=self.request.user)
        return Contact.objects.none()
    
    def perform_create(self, serializer):
        # CORRECTION : Utiliser self.request.user directement
        serializer.save(utilisateur=self.request.user)
    
    @action(detail=False, methods=['get'])
    def principaux(self, request):
        contacts = self.get_queryset().filter(est_principal=True)
        serializer = self.get_serializer(contacts, many=True)
        return Response(serializer.data)

class CompetenceViewSet(viewsets.ModelViewSet):
    serializer_class = CompetenceSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['nom_competence', 'description']
    filterset_fields = ['categorie', 'niveau_competence', 'est_visible']
    ordering_fields = ['nom_competence', 'categorie', 'ordre', 'annees_experience']
    
    def get_queryset(self):
        # CORRECTION : Utiliser self.request.user directement
        if self.request.user.is_authenticated:
            return Competence.objects.filter(utilisateur=self.request.user)
        return Competence.objects.none()
    
    def perform_create(self, serializer):
        # CORRECTION : Utiliser self.request.user directement
        serializer.save(utilisateur=self.request.user)
    
    @action(detail=False, methods=['get'])
    def par_categorie(self, request):
        competences = self.get_queryset().filter(est_visible=True)
        result = {}
        for competence in competences:
            categorie = competence.get_categorie_display()
            if categorie not in result:
                result[categorie] = []
            serializer = self.get_serializer(competence)
            result[categorie].append(serializer.data)
        return Response(result)

class ProjetViewSet(viewsets.ModelViewSet):
    serializer_class = ProjetSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['titre_projet', 'description_projet', 'langage_projet']
    filterset_fields = ['langage_projet', 'est_public', 'est_termine']
    ordering_fields = ['titre_projet', 'date_realisation', 'ordre']
    
    def get_queryset(self):
        # CORRECTION : Utiliser self.request.user directement
        if self.request.user.is_authenticated:
            return Projet.objects.filter(utilisateur=self.request.user)
        return Projet.objects.none()
    
    def perform_create(self, serializer):
        # CORRECTION : Utiliser self.request.user directement
        serializer.save(utilisateur=self.request.user)
    
    @action(detail=False, methods=['get'])
    def publics(self, request):
        projets = self.get_queryset().filter(est_public=True)
        page = self.paginate_queryset(projets)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(projets, many=True)
        return Response(serializer.data)

class PortfolioViewSet(viewsets.ModelViewSet):
    queryset = Portfolio.objects.all()
    permission_classes = [PortfolioPermissions]
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['titre', 'description', 'titre_professionnel', 'biographie']
    filterset_fields = ['statut', 'layout_type']
    ordering_fields = ['date_creation', 'date_modification', 'vue_count', 'titre']
    
    def get_serializer_class(self):
        if self.action == 'list':
            return PortfolioListSerializer
        elif self.action in ['retrieve', 'stats']:
            return PortfolioDetailSerializer
        elif self.action in ['create', 'update', 'partial_update']:
            return PortfolioCreateUpdateSerializer
        elif self.action == 'publish':
            return PortfolioPublishSerializer
        return PortfolioDetailSerializer
    
    def get_queryset(self):
        queryset = Portfolio.objects.select_related('utilisateur').all()
        statut = self.request.query_params.get('statut', None)
        if statut:
            queryset = queryset.filter(statut=statut)
        
        utilisateur_id = self.request.query_params.get('utilisateur', None)
        if utilisateur_id:
            queryset = queryset.filter(utilisateur__id_utilisateur=utilisateur_id)
        
        competence = self.request.query_params.get('competence', None)
        if competence:
            queryset = queryset.filter(competences__nom_competence__icontains=competence)
        
        langage = self.request.query_params.get('langage', None)
        if langage:
            queryset = queryset.filter(projets__langage_projet__icontains=langage)
        
        if not self.request.user.is_authenticated:
            queryset = queryset.filter(statut='publie')
        elif not self.request.user.is_staff:
            # CORRECTION : Utiliser self.request.user directement
            queryset = queryset.filter(
                Q(statut='publie') | Q(utilisateur=self.request.user)
            )
        
        return queryset.distinct()
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.is_published():
            instance.increment_vue_count()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
    
    @transaction.atomic
    def create(self, request, *args, **kwargs):
        # CORRECTION : Utiliser request.user directement
        if Portfolio.objects.filter(utilisateur=request.user).exists():
            raise ValidationError("Vous avez déjà un portfolio")
        
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        detail_serializer = PortfolioDetailSerializer(
            serializer.instance,
            context={'request': request}
        )
        
        return Response(
            detail_serializer.data,
            status=status.HTTP_201_CREATED
        )
    
    @transaction.atomic
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.statut = 'archive'
        instance.save()
        return Response(
            {'message': 'Portfolio archivé avec succès'},
            status=status.HTTP_200_OK
        )
    
    @action(detail=False, methods=['get'])
    def my_portfolio(self, request):
        # CORRECTION : Supprimer la vérification hasattr
        try:
            portfolio = Portfolio.objects.get(utilisateur=request.user)
            serializer = PortfolioDetailSerializer(
                portfolio,
                context={'request': request}
            )
            return Response(serializer.data)
        except Portfolio.DoesNotExist:
            return Response(
                {'message': 'Aucun portfolio trouvé pour cet utilisateur'},
                status=status.HTTP_404_NOT_FOUND
            )
    
    @action(detail=True, methods=['post'])
    def publish(self, request, pk=None):
        portfolio = self.get_object()
        serializer = PortfolioPublishSerializer(
            data=request.data,
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        
        try:
            serializer.update(portfolio, serializer.validated_data)
        except ValidationError as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        return Response(
            PortfolioDetailSerializer(portfolio, context={'request': request}).data,
            status=status.HTTP_200_OK
        )
    
    @action(detail=True, methods=['get'])
    def stats(self, request, pk=None):
        portfolio = self.get_object()
        stats = {
            'general': {
                'vues': portfolio.vue_count,
                'statut': portfolio.get_statut_display(),
                'date_creation': portfolio.date_creation,
                'date_modification': portfolio.date_modification,
                'date_publication': portfolio.date_publication,
                'jours_actif': (timezone.now() - portfolio.date_creation).days if portfolio.date_creation else 0
            },
            'contenu': {
                'contacts': portfolio.contacts.count(),
                'contacts_principaux': portfolio.contacts.filter(est_principal=True).count(),
                'competences': portfolio.competences.count(),
                'competences_visibles': portfolio.competences.filter(est_visible=True).count(),
                'projets': portfolio.projets.count(),
                'projets_publics': portfolio.projets.filter(est_public=True).count()
            },
            'competences_par_categorie': {},  # Ajouté
            'projets_par_langage': {}  # Ajouté
        }
        
        competences = portfolio.competences.all()
        for competence in competences:
            categorie = competence.get_categorie_display()
            if categorie not in stats['competences_par_categorie']:
                stats['competences_par_categorie'][categorie] = 0
            stats['competences_par_categorie'][categorie] += 1
        
        projets = portfolio.projets.all()
        for projet in projets:
            langage = projet.langage_projet
            if langage not in stats['projets_par_langage']:
                stats['projets_par_langage'][langage] = 0
            stats['projets_par_langage'][langage] += 1
        
        return Response(stats, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['get'])
    def published(self, request):
        portfolios = Portfolio.objects.filter(statut='publie')
        page = self.paginate_queryset(portfolios)
        if page is not None:
            serializer = PortfolioListSerializer(
                page,
                many=True,
                context={'request': request}
            )
            return self.get_paginated_response(serializer.data)
        serializer = PortfolioListSerializer(
            portfolios,
            many=True,
            context={'request': request}
        )
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    @transaction.atomic
    def duplicate(self, request, pk=None):
        portfolio = self.get_object()
        self.check_object_permissions(request, portfolio)
        
        # CORRECTION : Utiliser request.user directement
        if Portfolio.objects.filter(utilisateur=request.user).exists():
            raise ValidationError("Vous avez déjà un portfolio")
        
        new_portfolio = Portfolio.objects.create(
            utilisateur=request.user,
            titre=f"{portfolio.titre} (Copie)",
            description=portfolio.description,
            titre_professionnel=portfolio.titre_professionnel,
            biographie=portfolio.biographie,
            statut='brouillon',
            theme_couleur=portfolio.theme_couleur,
            layout_type=portfolio.layout_type,
            meta_description=portfolio.meta_description,
            meta_keywords=portfolio.meta_keywords,
            afficher_photo=portfolio.afficher_photo,
            afficher_competences=portfolio.afficher_competences,
            afficher_projets=portfolio.afficher_projets,
            afficher_contacts=portfolio.afficher_contacts,
            afficher_formations=portfolio.afficher_formations,
            afficher_experiences=portfolio.afficher_experiences,
            formations=portfolio.formations,
            experiences=portfolio.experiences,
            langues=portfolio.langues,
            certifications=portfolio.certifications,
            interets=portfolio.interets
        )
        
        for contact in portfolio.contacts.all():
            new_contact = Contact.objects.create(
                type_contact=contact.type_contact,
                valeur_contact=contact.valeur_contact,
                utilisateur=request.user,
                est_principal=contact.est_principal,
                ordre=contact.ordre
            )
            new_portfolio.contacts.add(new_contact)
        
        for competence in portfolio.competences.all():
            new_competence = Competence.objects.create(
                nom_competence=competence.nom_competence,
                niveau_competence=competence.niveau_competence,
                categorie=competence.categorie,
                utilisateur=request.user,
                annees_experience=competence.annees_experience,
                description=competence.description,
                est_visible=competence.est_visible,
                ordre=competence.ordre
            )
            new_portfolio.competences.add(new_competence)
        
        for projet in portfolio.projets.all():
            new_projet = Projet.objects.create(
                titre_projet=projet.titre_projet,
                description_projet=projet.description_projet,
                langage_projet=projet.langage_projet,
                utilisateur=request.user,
                lien_projet=projet.lien_projet,
                lien_github=projet.lien_github,
                technologies=projet.technologies,
                date_realisation=projet.date_realisation,
                est_public=projet.est_public,
                est_termine=projet.est_termine,
                ordre=projet.ordre
            )
            new_portfolio.projets.add(new_projet)
        
        return Response(
            PortfolioDetailSerializer(new_portfolio, context={'request': request}).data,
            status=status.HTTP_201_CREATED
        )
    
    @action(detail=True, methods=['post'])
    def add_contact(self, request, pk=None):
        portfolio = self.get_object()
        contact_id = request.data.get('contact_id')
        if not contact_id:
            return Response(
                {'error': 'contact_id est requis'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            contact = Contact.objects.get(id_contact=contact_id)
            # CORRECTION : Utiliser request.user directement
            if contact.utilisateur != request.user:
                raise PermissionDenied("Ce contact ne vous appartient pas")
            portfolio.contacts.add(contact)
            return Response(
                PortfolioDetailSerializer(portfolio, context={'request': request}).data,
                status=status.HTTP_200_OK
            )
        except Contact.DoesNotExist:
            return Response(
                {'error': 'Contact non trouvé'},
                status=status.HTTP_404_NOT_FOUND
            )
    
    @action(detail=True, methods=['post'])
    def add_competence(self, request, pk=None):
        portfolio = self.get_object()
        competence_id = request.data.get('competence_id')
        if not competence_id:
            return Response(
                {'error': 'competence_id est requis'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            competence = Competence.objects.get(id_competence=competence_id)
            # CORRECTION : Utiliser request.user directement
            if competence.utilisateur != request.user:
                raise PermissionDenied("Cette compétence ne vous appartient pas")
            portfolio.competences.add(competence)
            return Response(
                PortfolioDetailSerializer(portfolio, context={'request': request}).data,
                status=status.HTTP_200_OK
            )
        except Competence.DoesNotExist:
            return Response(
                {'error': 'Compétence non trouvé'},
                status=status.HTTP_404_NOT_FOUND
            )
    
    @action(detail=True, methods=['post'])
    def add_projet(self, request, pk=None):
        portfolio = self.get_object()
        projet_id = request.data.get('projet_id')
        if not projet_id:
            return Response(
                {'error': 'projet_id est requis'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            projet = Projet.objects.get(id_projet=projet_id)
            # CORRECTION : Utiliser request.user directement
            if projet.utilisateur != request.user:
                raise PermissionDenied("Ce projet ne vous appartient pas")
            portfolio.projets.add(projet)
            return Response(
                PortfolioDetailSerializer(portfolio, context={'request': request}).data,
                status=status.HTTP_200_OK
            )
        except Projet.DoesNotExist:
            return Response(
                {'error': 'Projet non trouvé'},
                status=status.HTTP_404_NOT_FOUND
            )
    
    @action(detail=False, methods=['get'])
    def search(self, request):
        queryset = Portfolio.objects.filter(statut='publie')
        competence = request.query_params.get('competence', None)
        if competence:
            queryset = queryset.filter(competences__nom_competence__icontains=competence)
        
        langage = request.query_params.get('langage', None)
        if langage:
            queryset = queryset.filter(projets__langage_projet__icontains=langage)
        
        niveau = request.query_params.get('niveau', None)
        if niveau:
            queryset = queryset.filter(competences__niveau_competence=niveau)
        
        categorie = request.query_params.get('categorie', None)
        if categorie:
            queryset = queryset.filter(competences__categorie=categorie)
        
        page = self.paginate_queryset(queryset.distinct())
        if page is not None:
            serializer = PortfolioListSerializer(
                page,
                many=True,
                context={'request': request}
            )
            return self.get_paginated_response(serializer.data)
        
        serializer = PortfolioListSerializer(
            queryset.distinct(),
            many=True,
            context={'request': request}
        )
        return Response(serializer.data)