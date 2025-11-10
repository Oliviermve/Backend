from django.db import models
from utilisateur.models import Utilisateur

class Contact(models.Model):
    TYPE_CONTACT_CHOICES = [
        ('email', 'Email'),
        ('telephone', 'Téléphone'),
        ('linkedin', 'LinkedIn'),
        ('github', 'GitHub'),
        ('twitter', 'Twitter'),
        ('autre', 'Autre'),
    ]
    
    id_contact = models.AutoField(primary_key=True)
    type_contact = models.CharField(max_length=20, choices=TYPE_CONTACT_CHOICES)
    valeur_contact = models.CharField(max_length=255)
    
    def __str__(self):
        return f"{self.type_contact}: {self.valeur_contact}"

class Competence(models.Model):
    NIVEAU_CHOICES = [
        ('debutant', 'Débutant'),
        ('intermediaire', 'Intermédiaire'),
        ('avance', 'Avancé'),
        ('expert', 'Expert'),
    ]
    
    id_competence = models.AutoField(primary_key=True)
    nom_competence = models.CharField(max_length=100)
    niveau_competence = models.CharField(max_length=20, choices=NIVEAU_CHOICES)
    
    def __str__(self):
        return f"{self.nom_competence} ({self.niveau_competence})"

class Projet(models.Model):
    id_projet = models.AutoField(primary_key=True)
    titre_projet = models.CharField(max_length=200)
    description_projet = models.TextField()
    langage_projet = models.CharField(max_length=100)
    lien_projet = models.URLField(blank=True, null=True)
    image_projet = models.ImageField(upload_to='projets/', blank=True, null=True)
    
    def __str__(self):
        return self.titre_projet

class Template(models.Model):
    id_template = models.AutoField(primary_key=True)
    nom_template = models.CharField(max_length=100)
    description_template = models.TextField()
    fichier_html = models.FileField(upload_to='templates/')
    image_template = models.ImageField(upload_to='templates_images/', blank=True, null=True)
    
    def __str__(self):
        return self.nom_template

class Portfolio(models.Model):
    STATUT_CHOICES = [
        ('brouillon', 'Brouillon'),
        ('publie', 'Publié'),
        ('archive', 'Archivé'),
    ]
    
    id_portfolio = models.AutoField(primary_key=True)
    utilisateur = models.OneToOneField(Utilisateur, on_delete=models.CASCADE)
    template = models.ForeignKey(Template, on_delete=models.SET_NULL, null=True, blank=True)
    
    titre = models.CharField(max_length=200)
    date_creation = models.DateTimeField(auto_now_add=True)
    description = models.TextField(blank=True)
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='brouillon')
    
    contacts = models.ManyToManyField(Contact, blank=True)
    competences = models.ManyToManyField(Competence, blank=True)
    projets = models.ManyToManyField(Projet, blank=True)
    
    def __str__(self):
        return f"Portfolio de {self.utilisateur.prenom} {self.utilisateur.nom}"