from django.shortcuts import redirect, render , get_object_or_404
from .models import Categorie, Produit
from .models import Fournisseur,Commande,Panier
from .forms import ProduitForm, FournisseurForm,UserRegistrationForm,UserCreationForm,CommandeForm,AjouterPanierForm,CategorieForm
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets

from magasin.models import Categorie
from magasin.serializers import CategorySerializer
from magasin.serializers import ProduitSerializer
class ProductViewset(viewsets.ReadOnlyModelViewSet):

    serializer_class = ProduitSerializer

    def get_queryset(self):
        queryset = Produit.objects.filter(active=True)
        category_id = self.request.GET.get('category_id')
        if category_id:
            queryset = queryset.filter(categorie_id=category_id)
        return queryset
class CategoryAPIView(APIView):
 
    def get(self, *args, **kwargs):
        categories = Categorie.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)

class ProduitAPIView(APIView):
    def get(self, *args, **kwargs):
         produits = Produit.objects.all()
         serializer = ProduitSerializer(produits, many=True)
         return Response(serializer.data)



def index(request):
       if request.method == "POST" :
         form = ProduitForm(request.POST,request.FILES)
         if form.is_valid():
              form.save() 
              list=Produit.objects.all()
              return render(request,'Produits/vitrineP.html',{'list':list})
       else : 
            form = ProduitForm() #créer formulaire vide 
            list=Produit.objects.all()
            return render(request,'Produits/create_product.html',{'form':form,'list':list})

def edit_product(request, pk):
    product = get_object_or_404(Produit, pk=pk)
    if request.method == 'POST':
        form = ProduitForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            # Récupérer l'instance du modèle produit
            produit = form.save(commit=False)
            # Récupérer la nouvelle image téléchargée
            nouvelle_image = form.cleaned_data['img']
            # Si une nouvelle image a été téléchargée, la sauvegarder
            if nouvelle_image:
                produit.img = nouvelle_image
            # Sauvegarder le produit
            produit.save()
            return redirect('Catalogue')
    else:
        form = ProduitForm(instance=product)
        return render(request, 'Produits/edit_product.html', {'form': form})

def delete_product(request, pk):
    product = get_object_or_404(Produit, pk=pk)
    if request.method == 'POST':
        product.delete()
        return redirect('Catalogue')
    return render(request, 'Produits/delete_product.html', {'product': product})

def detail_product(request, product_id):
    produit = get_object_or_404(Produit, id=product_id)
    context = {'produit': produit}
    return render(request, 'Produits/detail_product.html', context)

def Catalogue(request):
        products= Produit.objects.all()
        context={'products':products}
        return render( request,'Produits/mesProduits.html',context )
        

def indexA(request):
     return render(request,'magasin/acceuil.html' )


def ListFournisseur(request):
    fournisseurs = Fournisseur.objects.all()
    context = {'fournisseurs': fournisseurs}
    return render(request, 'Fournisseurs/mesFournisseurs.html', context)

def nouveauFournisseur(request):
    if request.method == "POST" :
         form = FournisseurForm(request.POST,request.FILES)
         if form.is_valid():
               # Récupérer l'instance du modèle produit
            frns = form.save(commit=False)
            # Récupérer la nouvelle image téléchargée
            nouvelle_image = form.cleaned_data['logo']
            # Si une nouvelle image a été téléchargée, la sauvegarder
            if nouvelle_image:
                frns.logo= nouvelle_image
            # Sauvegarder le produit
            form.save() 
            fournisseurs=Fournisseur.objects.all()
            return render(request,'Fournisseurs/mesFournisseurs.html',{'fournisseurs':fournisseurs})
    else : 
            form = FournisseurForm() #créer formulaire vide 
            fournisseurs=Fournisseur.objects.all()
            return render(request,'Fournisseurs/create_For.html',{'form':form,'fournisseurs':fournisseurs})


def register(request):
     if request.method == 'POST' :
          form = UserCreationForm(request.POST)
          if form.is_valid():
               form.save()
               username = form.cleaned_data.get('username')
               password = form.cleaned_data.get('password1')
               user = authenticate(username=username, password=password)
               login(request,user)
               messages.success(request, f'Coucou {username}, Votre compte a été créé avec succès !')
               return redirect('home')
     else :
          form = UserCreationForm()
     return render(request,'registration/register.html',{'form' : form})

class ChangePasswordView(PasswordChangeView):
    template_name = 'registration/change_password.html'
    success_url = reverse_lazy('home')






def edit_Fournisseur(request, fk):
    fournisseur = get_object_or_404(Fournisseur, id=fk)
    if request.method == 'POST':
        form = FournisseurForm(request.POST, request.FILES, instance=fournisseur)
        if form.is_valid():
            # Récupérer l'instance du modèle produit
            frns = form.save(commit=False)
            # Récupérer la nouvelle image téléchargée
            nouvelle_image = form.cleaned_data['logo']
            # Si une nouvelle image a été téléchargée, la sauvegarder
            if nouvelle_image:
                frns.logo= nouvelle_image
            # Sauvegarder le produit
            frns.save()
            return redirect('fournisseurs')
    else:
        form = FournisseurForm(instance=fournisseur)
        return render(request, 'Fournisseurs/edit_For.html', {'form': form})

def delete_Fournisseur(request, fk):
    fournisseur = get_object_or_404(Fournisseur, id=fk)
    if request.method == 'POST':
        fournisseur.delete()
        return redirect('fournisseurs')
    return render(request,'Fournisseurs/delete_For.html', {'fournisseur': fournisseur})

def detail_Fournisseur(request, for_id):
    fournisseur = get_object_or_404(Fournisseur, id=for_id)
    context = {'fournisseur': fournisseur}
    return render(request, 'Fournisseurs/detail_For.html', context)

def create_commande(request):
       if request.method == "POST" :
         form = CommandeForm(request.POST)
         if form.is_valid():
              form.save() 
              commandes=Commande.objects.all()
              
              return render(request,'Commandes/mesCommandes.html',{'commandes':commandes})
       else : 
            form = CommandeForm() #créer formulaire vide 
            commandes=Commande.objects.all()
            return render(request,'Commandes/create_commande.html',{'form':form,'commandes':commandes})

def edit_commande(request, pk):
    commande = get_object_or_404(Commande, pk=pk)
    if request.method == 'POST':
        form = CommandeForm(request.POST, instance=commande)
        if form.is_valid():
            form.save()
            return redirect('ListCommande')
    else:
        form = CommandeForm(instance=commande)
    return render(request, 'Commandes/edit_commande.html', {'form': form})

def delete_commande(request, pk):
    commande = get_object_or_404(Commande, pk=pk)
    if request.method == 'POST':
        commande.delete()
        return redirect('ListCommande')
    return render(request, 'Commandes/delete_commande.html', {'commande': commande})

def detail_commande(request, commande_id):
    commande = get_object_or_404(Commande, id=commande_id)
    context = {'commande': commande}
    return render(request, 'Commandes/detail_commande.html', context)

def ListCommande(request):
        commandes= Commande.objects.all()
        context={'commandes':commandes}
        return render( request,'Commandes/mesCommandes.html',context )


def create_categorie(request):
       if request.method == "POST" :
         form = CategorieForm(request.POST)
         if form.is_valid():
              form.save() 
              categories=Categorie.objects.all()
              
              return render(request,'Categories/mesCategories.html',{'categories':categories})
       else : 
            form = CategorieForm() #créer formulaire vide 
            categories=Categorie.objects.all()
            return render(request,'Categories/create_categorie.html',{'form':form,'categories':categories})

def edit_categorie(request, pk):
    categorie = get_object_or_404(Categorie, pk=pk)
    if request.method == 'POST':
        form = CategorieForm(request.POST, instance=categorie)
        if form.is_valid():
            categorie.save()
            return redirect('ListCategorie')
    else:
        form = CategorieForm(instance=categorie)
        return render(request, 'Categories/edit_categorie.html', {'form': form})

def delete_categorie(request, pk):
    categorie = get_object_or_404(Categorie, pk=pk)
    if request.method == 'POST':
        categorie.delete()
        return redirect('ListCategorie')
    return render(request, 'Categories/delete_categorie.html', {'categorie': categorie})

def detail_categorie(request, categorie_id):
    categorie = get_object_or_404(Categorie, id=categorie_id)
    context = {'categorie': categorie}
    return render(request, 'Categories/detail_categorie.html', context)

def ListCategorie(request):
        categories= Categorie.objects.all()
        context={'categories':categories}
        return render( request,'Categories/mesCategories.html',context )

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Produit
from .forms import AjouterPanierForm


def liste_produits(request):
    produits = Produit.objects.all()
    # Ajouter le code pour trier les produits ici
    context = {'produits': produits}
    return render(request, 'panier/liste_produits.html', context)

def ajouter_au_panier(request, produit_id):
    produit = get_object_or_404(Produit, id=produit_id)
    if request.method == 'POST':
        form = AjouterPanierForm(request.POST)
        if form.is_valid():
            quantite_demandee = form.cleaned_data['quantite']
            if produit.stock >= quantite_demandee:
                panier = request.session.get('panier', {})
                if produit_id in panier:
                    panier[produit_id]['quantite'] += quantite_demandee
                else:
                    panier[produit_id] = {'quantite': quantite_demandee, 'prix': float(produit.prix)}
                request.session['panier'] = panier
                messages.success(request, f"{produit.libellé} a été ajouté au panier.")
                return redirect('liste_produits')
            else:
                messages.error(request, f"Désolé, il n'y a pas assez de stock pour {produit.libellé}.")
    else:
        form = AjouterPanierForm()
    context = {'produit': produit, 'form': form}
    return render(request, 'panier/ajouter_au_panier.html', context)

def contenu_panier(request):
    panier = request.session.get('panier', {})
    contenu = []
    total = 0
    for produit_id, info in panier.items():
        produit = get_object_or_404(Produit, id=produit_id)
        quantite = info['quantite']
        prix_unitaire = info['prix']
        prix_total = quantite * prix_unitaire
        contenu.append({'produit': produit, 'quantite': quantite, 'prix_unitaire': prix_unitaire, 'prix_total': prix_total})
        total += prix_total
    context = {'contenu': contenu, 'total': total}
    return render(request, 'panier/contenu_panier.html', context)

def passer_commande(request):
    panier = request.session.get('panier', {})
    if not panier:
        messages.error(request, "Votre panier est vide.")
        return redirect('contenu_panier')
    for produit_id, info in panier.items():
        produit = get_object_or_404(Produit, id=produit_id)
        quantite_demandee = info['quantite']
        if quantite_demandee > produit.stock:
            messages.error(request, f"Désolé, il n'y a plus assez de stock pour {produit.libellé}.")
            return redirect('contenu_panier')
    for produit_id, info in panier.items():
        produit = get_object_or_404(Produit, id=produit_id)
        quantite_demandee = info['quantite']
        produit.stock -= quantite_demandee
        produit.save()
    request.session['panier'] = {}
    messages.success(request, "Votre commande a été passée.")
    return redirect('liste_produits')


def vider_panier(request):
    request.session['panier'] = {}
    messages.success(request, "Votre panier a été vidé.")
    return redirect('liste_produits')

from django.shortcuts import render
from .models import Panier

def panier_detail(request):
    panier = Panier.objects.filter(utilisateur=request.user)
    total = 0
    for p in panier:
        total += p.total_produit()
    context = {
        'panier': panier,
        'total': total,
    }
    return render(request, 'panier/panier_detail.html', context)



def liste_paniers(request):
    paniers = Panier.objects.all()
    context = {'paniers': paniers}
    return render(request, 'panier/liste_paniers.html', context)



from django.forms.models import inlineformset_factory
from django.shortcuts import get_object_or_404, redirect, render

from .models import Panier, ContenuPanier
from .models import Panier, ContenuPanier
from .forms import PanierForm, ContenuPanierForm,EditPanierForm

from django.forms import inlineformset_factory
from .models import Panier, ContenuPanier

def edit_panier(request, pk):
    panier = get_object_or_404(Panier, pk=pk)
    ContenuPanierFormset = inlineformset_factory(Panier, ContenuPanier, fields=('produit', 'quantite'), extra=1)

    if request.method == 'POST':
        form = EditPanierForm(request.POST, instance=panier)
        formset = ContenuPanierFormset(request.POST, instance=panier)
        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            return redirect('liste_paniers')
    else:
        form = EditPanierForm(instance=panier)
        formset = ContenuPanierFormset(instance=panier)

    context = {'form': form, 'formset': formset, 'panier': panier}
    return render(request, 'panier/edit_panier.html', context)
