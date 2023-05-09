from django.urls import path
from django.contrib import admin
from django.urls import path,include
from .import views
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from .views import CategoryAPIView
 
from magasin.views import ProduitAPIView

from rest_framework import routers
from magasin.views import ProductViewset, CategoryAPIView
router = routers.SimpleRouter()
router.register('produit', ProductViewset, basename='produit')

urlpatterns = [
    path('api/produits/', ProduitAPIView.as_view()),
    path('api/', include(router.urls)),
    path('api/category/', CategoryAPIView.as_view()),
     path('api-auth/', include('rest_framework.urls')),
    path('products/', views.index, name='index'),
    path('', views.indexA, name='indexA'),
    path('fournisseurs/', views.ListFournisseur, name='fournisseurs'),
    path('Catalogue/', views.Catalogue, name='Catalogue'),
    path('nouvFournisseur/',views.nouveauFournisseur,name='nouvFournisseur'),
    path('register/',views.register, name = 'register'), 
    path('change_password/', views.ChangePasswordView.as_view(), name='change_password'),

    path('editFournisseur/<int:fk>/', views.edit_Fournisseur, name='edit_Fournisseur'),
    path('deleteFournisseur/<int:fk>/', views.delete_Fournisseur, name='delete_Fournisseur'),
    path('Fournisseur/<int:for_id>/', views.detail_Fournisseur, name='detail_Fournisseur'),

    path('editProduct/<int:pk>/', views.edit_product, name='edit_product'),
    path('deleteProduct/<int:pk>/', views.delete_product, name='delete_product'),
    path('Product/<int:product_id>/', views.detail_product, name='detail_product'),

    path('ListCommande/', views.ListCommande, name='ListCommande'),
    path('create_commande/',views.create_commande,name='create_commande'),
     path('editCommande/<int:pk>/', views.edit_commande, name='edit_commande'),
    path('deleteCommande/<int:pk>/', views.delete_commande, name='delete_commande'),
    path('Commande/<int:commande_id>/', views.detail_commande, name='detail_commande'),

    path('ListCategorie/', views.ListCategorie, name='ListCategorie'),
    path('create_categorie/',views.create_categorie,name='create_categorie'),
    path('editCategorie/<int:pk>/', views.edit_categorie, name='edit_categorie'),
    path('deleteCategorie/<int:pk>/', views.delete_categorie, name='delete_categorie'),
    path('Categorie/<int:categorie_id>/', views.detail_categorie, name='detail_categorie'),
  
    path('liste/', views.liste_produits, name='liste_produits'),
    path('ajouter/<int:produit_id>/', views.ajouter_au_panier, name='ajouter_au_panier'),
    path('contenu/', views.contenu_panier, name='contenu_panier'),
    path('passer_commande/', views.passer_commande, name='passer_commande'),
    path('vider_panier/', views.vider_panier, name='vider_panier'),
    path('panier_detail/', views.panier_detail, name='panier_detail'),
    path('paniers/', views.liste_paniers, name='liste_paniers'),
    path('panier/<int:pk>/', views.edit_panier, name='edit_panier'),
   
   
   ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)