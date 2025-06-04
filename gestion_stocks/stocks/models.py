from django.db import models
from django.contrib.auth.hashers import check_password, make_password

# Create your models here.

class User(models.Model):
    ROLE = [
        ('', '---- Sélectionnez un rôle ----'),
        ('Administrateur', 'Administrateur'),
        ('Gestionnaire de stock', 'Gestionnaire de stock'),
        ('Consultant', 'Consultant')
    ]
    
    prenom = models.CharField(max_length=100)
    nom = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    telephone = models.CharField(unique=True, max_length=20)
    username = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=128)
    role = models.CharField(max_length=50, choices=ROLE)
    valide = models.BooleanField(default=False)
    actif = models.BooleanField(default=True)
    photo_profil = models.ImageField(upload_to='static/users/photodeprofil/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)
    
    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def __str__(self):
        return f"{self.prenom} {self.nom}"

    class Meta:
        verbose_name = "Utilisateur"
        verbose_name_plural = "Utilisateurs"

class Fournisseur(models.Model):
    nom = models.CharField(max_length=255)
    contact = models.CharField(max_length=20)
    adresse = models.TextField()

    def __str__(self):
        return self.nom
    
    class Meta:
        verbose_name = "Fournisseur"
        verbose_name_plural = "Fournisseurs"

class Entree(models.Model):
    fournisseur = models.ForeignKey(Fournisseur, on_delete=models.CASCADE, related_name="produits")
    prixTotal = models.DecimalField(max_digits=10, decimal_places=2)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="utilisateurs")
    date = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Entrée"
        verbose_name_plural = "Entrées"

class Produit(models.Model):
    UNITE_CHOICES = [
        ('kg', 'Kilogramme'),
        ('litre', 'Litre'),
        ('unité', 'Unité')
    ]

    nom = models.CharField(max_length=255)
    reference = models.CharField(max_length=100, unique=True)
    categorie = models.CharField(max_length=255)
    quantite_fournie = models.PositiveIntegerField()
    quantite_disponible = models.PositiveIntegerField()
    unite_mesure = models.CharField(max_length=10, choices=UNITE_CHOICES)
    prix_achat_unitaire = models.DecimalField(max_digits=10, decimal_places=2)
    prix_vente = models.DecimalField(max_digits=10, decimal_places=2)
    prix_total = models.DecimalField(max_digits=10, decimal_places=2)
    date_peremption = models.DateField()
    entree = models.ForeignKey(Entree, on_delete=models.CASCADE, related_name="entrees")

    def __str__(self):
        return f"{self.nom} ({self.reference})"
    
    class Meta:
        verbose_name = "Produit"
        verbose_name_plural = "Produits"

class Sortie(models.Model):
    TYPE_CHOICES = [
        ('Vente', 'Vente'),
        ('Utilisations internes', 'Utilisations internes'),
        ('Destructions(Produits périmés)', 'Destructions(Produits périmés)'),
        ('Transferts entre entrepôts', 'Transferts entre entrepôts')
    ]
    motif = models.CharField(max_length=100, choices=TYPE_CHOICES)
    prixTotal = models.DecimalField(max_digits=10, decimal_places=2)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="utilisateurs_sortie")
    date = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Sortie"
        verbose_name_plural = "Sorties"

class ProduitSortie(models.Model):
    nom = models.CharField(max_length=255)
    reference = models.CharField(max_length=100)
    quantite_sortie = models.PositiveIntegerField()
    prix_vente = models.DecimalField(max_digits=10, decimal_places=2)
    prixTotal = models.DecimalField(max_digits=10, decimal_places=2)
    sortie = models.ForeignKey(Sortie, on_delete=models.CASCADE, related_name="sortiesId")
    
    class Meta:
        verbose_name = "Produit sortie"
        verbose_name_plural = "Produits sorties"