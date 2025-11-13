from rest_framework import serializers
from .models import Contact, Competence, Projet, Template, Portfolio
from utilisateur.serializers import UtilisateurSerializer

# ============================================================================
# SERIALIZERS DE BASE
# ============================================================================

class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ['id_contact', 'type_contact', 'valeur_contact']
    
    def validate_type_contact(self, value):
        types_valides = ['email', 'telephone', 'linkedin', 'github', 'twitter', 'autre']
        if value not in types_valides:
            raise serializers.ValidationError(f"Type de contact invalide. Types valides: {types_valides}")
        return value

class CompetenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Competence
        fields = ['id_competence', 'nom_competence', 'niveau_competence']
    
    def validate_niveau_competence(self, value):
        niveaux_valides = ['debutant', 'intermediaire', 'avance', 'expert']
        if value not in niveaux_valides:
            raise serializers.ValidationError(f"Niveau invalide. Niveaux valides: {niveaux_valides}")
        return value

class ProjetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Projet
        fields = ['id_projet', 'titre_projet', 'description_projet', 'langage_projet', 'lien_projet', 'image_projet']
        read_only_fields = ['id_projet']

class TemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Template
        fields = ['id_template', 'nom_template', 'description_template', 'fichier_html', 'image_template']
        read_only_fields = ['id_template']

# ============================================================================
# SERIALIZERS SPÉCIAUX POUR LES ACTIONS
# ============================================================================

class PortfolioPublierSerializer(serializers.ModelSerializer):
    """
    Serializer spécifique pour la publication d'un portfolio
    """
    class Meta:
        model = Portfolio
        fields = ['statut']
    
    def validate(self, data):
        portfolio = self.instance
        
        if not portfolio.titre:
            raise serializers.ValidationError({
                'titre': 'Le portfolio doit avoir un titre pour être publié.'
            })
        
        if not portfolio.template:
            raise serializers.ValidationError({
                'template': 'Un template doit être sélectionné pour publier le portfolio.'
            })
        
        if portfolio.competences.count() == 0:
            raise serializers.ValidationError({
                'competences': 'Le portfolio doit contenir au moins une compétence pour être publié.'
            })
        
        return data
    
    def update(self, instance, validated_data):
        instance.statut = 'publie'
        instance.save()
        return instance

class PortfolioModifierSerializer(serializers.ModelSerializer):
    """
    Serializer pour modifier les aspects design d'un portfolio
    """
    class Meta:
        model = Portfolio
        fields = ['titre', 'description', 'template']
    
    def validate_template(self, value):
        return value

class PortfolioAjouterProjetSerializer(serializers.ModelSerializer):
    """
    Serializer pour ajouter un projet à un portfolio
    """
    nouveau_projet = ProjetSerializer(write_only=True, required=False)
    projet_existant_id = serializers.PrimaryKeyRelatedField(
        queryset=Projet.objects.all(),
        write_only=True,
        required=False,
        source='projets'
    )
    
    class Meta:
        model = Portfolio
        fields = ['nouveau_projet', 'projet_existant_id']
    
    def validate(self, data):
        if not data.get('nouveau_projet') and not data.get('projets'):
            raise serializers.ValidationError(
                "Vous devez fournir soit un nouveau projet, soit un projet existant."
            )
        return data
    
    def update(self, instance, validated_data):
        nouveau_projet_data = validated_data.pop('nouveau_projet', None)
        projets_data = validated_data.pop('projets', None)
        
        if nouveau_projet_data:
            nouveau_projet = Projet.objects.create(**nouveau_projet_data)
            instance.projets.add(nouveau_projet)
        
        if projets_data:
            instance.projets.add(projets_data)
        
        return instance

class PortfolioAjouterCompetenceSerializer(serializers.ModelSerializer):
    """
    Serializer pour ajouter une compétence à un portfolio
    """
    nouvelle_competence = CompetenceSerializer(write_only=True, required=False)
    competence_existante_id = serializers.PrimaryKeyRelatedField(
        queryset=Competence.objects.all(),
        write_only=True,
        required=False,
        source='competences'
    )
    
    class Meta:
        model = Portfolio
        fields = ['nouvelle_competence', 'competence_existante_id']
    
    def validate(self, data):
        if not data.get('nouvelle_competence') and not data.get('competences'):
            raise serializers.ValidationError(
                "Vous devez fournir soit une nouvelle compétence, soit une compétence existante."
            )
        return data
    
    def update(self, instance, validated_data):
        nouvelle_competence_data = validated_data.pop('nouvelle_competence', None)
        competences_data = validated_data.pop('competences', None)
        
        if nouvelle_competence_data:
            nouvelle_competence = Competence.objects.create(**nouvelle_competence_data)
            instance.competences.add(nouvelle_competence)
        
        if competences_data:
            instance.competences.add(competences_data)
        
        return instance

class PortfolioAjouterContactSerializer(serializers.ModelSerializer):
    """
    Serializer pour ajouter un contact à un portfolio
    """
    nouveau_contact = ContactSerializer(write_only=True, required=False)
    contact_existant_id = serializers.PrimaryKeyRelatedField(
        queryset=Contact.objects.all(),
        write_only=True,
        required=False,
        source='contacts'
    )
    
    class Meta:
        model = Portfolio
        fields = ['nouveau_contact', 'contact_existant_id']
    
    def validate(self, data):
        if not data.get('nouveau_contact') and not data.get('contacts'):
            raise serializers.ValidationError(
                "Vous devez fournir soit un nouveau contact, soit un contact existant."
            )
        return data
    
    def update(self, instance, validated_data):
        nouveau_contact_data = validated_data.pop('nouveau_contact', None)
        contacts_data = validated_data.pop('contacts', None)
        
        if nouveau_contact_data:
            nouveau_contact = Contact.objects.create(**nouveau_contact_data)
            instance.contacts.add(nouveau_contact)
        
        if contacts_data:
            instance.contacts.add(contacts_data)
        
        return instance

# ============================================================================
# SERIALIZERS PRINCIPAUX PORTFOLIO
# ============================================================================

class PortfolioListSerializer(serializers.ModelSerializer):
    utilisateur_nom = serializers.CharField(source='utilisateur.prenom', read_only=True)
    template_nom = serializers.CharField(source='template.nom_template', read_only=True)
    nombre_competences = serializers.SerializerMethodField()
    nombre_projets = serializers.SerializerMethodField()
    nombre_contacts = serializers.SerializerMethodField()
    
    class Meta:
        model = Portfolio
        fields = [
            'id_portfolio', 
            'titre', 
            'utilisateur_nom',
            'template_nom',
            'statut',
            'date_creation',
            'nombre_competences',
            'nombre_projets',
            'nombre_contacts'
        ]
        read_only_fields = ['date_creation']
    
    def get_nombre_competences(self, obj):
        return obj.competences.count()
    
    def get_nombre_projets(self, obj):
        return obj.projets.count()
    
    def get_nombre_contacts(self, obj):
        return obj.contacts.count()

class PortfolioDetailSerializer(serializers.ModelSerializer):
    utilisateur = UtilisateurSerializer(read_only=True)
    template = TemplateSerializer(read_only=True)
    competences = CompetenceSerializer(many=True, read_only=True)
    contacts = ContactSerializer(many=True, read_only=True)
    projets = ProjetSerializer(many=True, read_only=True)
    
    competences_ids = serializers.PrimaryKeyRelatedField(
        queryset=Competence.objects.all(), 
        many=True, 
        write_only=True,
        source='competences',
        required=False
    )
    contacts_ids = serializers.PrimaryKeyRelatedField(
        queryset=Contact.objects.all(), 
        many=True, 
        write_only=True,
        source='contacts',
        required=False
    )
    projets_ids = serializers.PrimaryKeyRelatedField(
        queryset=Projet.objects.all(), 
        many=True, 
        write_only=True,
        source='projets',
        required=False
    )
    
    class Meta:
        model = Portfolio
        fields = [
            'id_portfolio', 
            'utilisateur', 
            'template',
            'titre', 
            'date_creation', 
            'description', 
            'statut',
            'competences', 
            'contacts', 
            'projets',
            'competences_ids',
            'contacts_ids',
            'projets_ids'
        ]
        read_only_fields = ['id_portfolio', 'date_creation']
    
    def validate_statut(self, value):
        statuts_valides = ['brouillon', 'publie', 'archive']
        if value not in statuts_valides:
            raise serializers.ValidationError(f"Statut invalide. Statuts valides: {statuts_valides}")
        return value

class PortfolioCreateSerializer(serializers.ModelSerializer):
    competences = serializers.PrimaryKeyRelatedField(
        queryset=Competence.objects.all(), 
        many=True, 
        required=False
    )
    contacts = serializers.PrimaryKeyRelatedField(
        queryset=Contact.objects.all(), 
        many=True, 
        required=False
    )
    projets = serializers.PrimaryKeyRelatedField(
        queryset=Projet.objects.all(), 
        many=True, 
        required=False
    )
    
    class Meta:
        model = Portfolio
        fields = [
            'utilisateur',
            'template', 
            'titre', 
            'description', 
            'statut',
            'competences', 
            'contacts', 
            'projets'
        ]
    
    def create(self, validated_data):
        competences_data = validated_data.pop('competences', [])
        contacts_data = validated_data.pop('contacts', [])
        projets_data = validated_data.pop('projets', [])
        
        portfolio = Portfolio.objects.create(**validated_data)
        
        portfolio.competences.set(competences_data)
        portfolio.contacts.set(contacts_data)
        portfolio.projets.set(projets_data)
        
        return portfolio

class PortfolioPublicSerializer(serializers.ModelSerializer):
    utilisateur_nom = serializers.SerializerMethodField()
    competences = CompetenceSerializer(many=True, read_only=True)
    contacts = ContactSerializer(many=True, read_only=True)
    projets = ProjetSerializer(many=True, read_only=True)
    template_nom = serializers.CharField(source='template.nom_template', read_only=True)
    
    class Meta:
        model = Portfolio
        fields = [
            'id_portfolio',
            'titre',
            'description',
            'utilisateur_nom',
            'template_nom',
            'competences',
            'contacts',
            'projets',
            'date_creation'
        ]
        read_only_fields = fields
    
    def get_utilisateur_nom(self, obj):
        return f"{obj.utilisateur.prenom} {obj.utilisateur.nom}"

# ============================================================================
# SERIALIZER TEMPLATE AVEC TYPE (OPTIONNEL)
# ============================================================================

class TemplateAvecTypeSerializer(serializers.ModelSerializer):
    TYPE_TEMPLATE_CHOICES = [
        ('gratuit', 'Gratuit'),
        ('premium', 'Premium'),
    ]
    
    type_template = serializers.ChoiceField(choices=TYPE_TEMPLATE_CHOICES, default='gratuit')
    prix = serializers.DecimalField(max_digits=6, decimal_places=2, required=False, allow_null=True)
    
    class Meta:
        model = Template
        fields = [
            'id_template', 
            'nom_template', 
            'description_template', 
            'fichier_html', 
            'image_template',
            'type_template',
            'prix'
        ]
        read_only_fields = ['id_template']
    
    def validate(self, data):
        if data.get('type_template') == 'premium' and not data.get('prix'):
            raise serializers.ValidationError({
                'prix': 'Les templates premium doivent avoir un prix.'
            })
        
        if data.get('type_template') == 'gratuit' and data.get('prix'):
            raise serializers.ValidationError({
                '.'
            })
        
        return data