
from datetime import date
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _



# Create your models here.
class Produit(models.Model):
    catégorie = models.ForeignKey('Categorie', on_delete=models.CASCADE, null=True)
    fournisseur = models.ForeignKey('Fournisseur', on_delete=models.CASCADE, null=True)
    TYPE_CHOICES=[  ('em','emballé'),
                    ('fr','Frais'),
                    ('cs','Conserve')]
    
    libellé=models.CharField(max_length=100)
    description=models.TextField(default='non définie')
    prix=models.DecimalField(max_digits=10,decimal_places=3,default=0)
    type=models.CharField(max_length=2,choices=TYPE_CHOICES,default='em')
    img =models.ImageField(upload_to='media/', null=True, blank=True)
    stock = models.IntegerField(default=0)
    
    def __str__(self):
        return self.libellé+","+self.description+","+str(self.prix)+","+self.type

class Categorie(models.Model):
    TYPE_CHOICES=[
    ('Al','Alimentaire'), ('Mb','Meuble'),
    ('Sn','Sanitaire'), ('Vs','Vaisselle'),
    ('Vt','Vêtement'),('Jx','Jouets'),
    ('Lg','Linge de Maison'),('Bj','Bijoux'),('Dc','Décor')
    ]

    name=models.CharField(max_length=50,default='Al',choices=TYPE_CHOICES)
    def __str__(self):
        return self.name
class Fournisseur(models.Model):
    nom=models.CharField(max_length=100,null=True)
    adresse=models.TextField(null=True)
    email=models.EmailField(null=True)
    telephone=models.CharField(max_length=8,null=True)
    logo =models.ImageField(upload_to='media/', null=True, blank=True)
    def __str__(self):
        return (self.nom+','+self.adresse+','+self.email+','+self.telephone)
class Commande(models.Model):
    dateCde = models.DateField(null=True, default=date.today)
    nom_client = models.CharField(max_length=100,default="")
    adresse_livraison = models.CharField(max_length=200,default="")
    totalCde = models.DecimalField(max_digits=10, decimal_places=3)
    produits = models.ManyToManyField(Produit, related_name='produits')

    def __str__(self):
        return str(self.dateCde) + ' - ' + str(self.totalCde)

    def get_produits_info(self):
    
        return [(p.libellé, p.prix,p.qte) for p in self.produits.all()]



class ProduitNC(Produit):
    Duree_garantie=models.CharField(max_length=100)
    
    def __str__(self):
        return "objet ProduitNC:%s"%(self.Duree_garantie)
    






class Panier(models.Model):
    STATUS_CHOICES = [
        ('en_attente', 'En attente'),
        ('en_cours', 'En cours de traitement'),
        ('livree', 'Livrée'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='en_attente')
    utilisateur = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    produit = models.ForeignKey(Produit, on_delete=models.CASCADE, null=True)
    quantite = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.utilisateur.username} - {self.produit.libellé} x {self.quantite}"

    def total_produit(self):
        return self.produit.prix * self.quantite

    class Meta:
        verbose_name = _("Panier")
        verbose_name_plural = _("Paniers")

class ContenuPanier(models.Model):
    panier = models.ForeignKey(Panier, on_delete=models.CASCADE, related_name='contenu')
    produit = models.ForeignKey(Produit, on_delete=models.CASCADE)
    quantite = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.produit.libellé} x {self.quantite} dans le panier de {self.panier.utilisateur.username}"



