from django.contrib import admin

# Register your models here.
from .models import*
from .models import Produit
admin.site.register(Produit)
from .models import Categorie
admin.site.register(Categorie)
from .models import Fournisseur
admin.site.register(Fournisseur)
from .models import Commande
admin.site.register(Commande)
from .models import ProduitNC
admin.site.register(ProduitNC)
from .models import Panier
admin.site.register(Panier)