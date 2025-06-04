from django.urls import path
from . import views

urlpatterns = [
    # Inscription / Connexion
    path('', views.index, name='index'),
    
    # Tbleau de bord
    path('dashboard/', views.dashboard, name='dashboard'),

    # Statistiques
    path('Statistique/', views.stats, name='stats'),

    # Gestion des utilisateur
    path('ListeDesUtilisateur', views.listeUtilisateurs, name='listeUtilisateurs'),
    path('AjouterUtilisateur', views.addUser, name='addUser'),
    path('DetailUtilisateur/<int:id>/', views.showUser, name='showUser'),
    path('ModifierUtilisateur/<int:id>/', views.updateUser, name='updateUser'),
    path('SuprimerUtilisateur/<int:id>/', views.deleteUser, name='deleteUser'),
    path('actif/<int:id>/<str:action>/', views.actif, name='actif'),

    # Gestion des fournisseurs
    path('ListeDesFournisseurs', views.listeFournisseurs, name='listeFournisseurs'),
    path('AjouterFournisseur', views.addFournisseur, name='addFournisseur'),
    path('DetailFournisseur/<int:id>', views.showFournisseur, name='showFournisseur'),
    path('ModifierFournisseur/<int:id>/', views.updateFournisseur, name='updateFournisseur'),
    path('SuprimerFournisseur/<int:id>/', views.deleteFournisseur, name='deleteFournisseur'),

    # Gestion des produits
    path('ListeDesProduits', views.listeProduits, name='listeProduits'),
    path('DetailProduit/<int:id>', views.showProduit, name='showProduit'),
    path('ModifierProduit/<int:id>/', views.updateProduit, name='updateProduit'),
    path('SuprimerProduit/<int:id>/', views.deleteProduit, name='deleteProduit'),

    # Gestion des entrées
    path('ListeDesEntrees', views.listeEntrees, name='listeEntrees'),
    path('listeDesProduitsEntrees/<int:id>', views.showProduitsEntrees, name='showProduitsEntrees'),
    path('AjouterEntree', views.addEntree, name='addEntree'),
    path('SuprimerEntree/<int:id>/', views.deleteEntree, name='deleteEntree'),

    # Gestion des entrées
    path('ListeDesSorties', views.listeSorties, name='listeSorties'),
    path('ListeDesProduitsSorties/<int:id>', views.showProduitsSorties, name='showProduitsSorties'),
    path('AjouterSortie', views.addSortie, name='addSortie'),
    path('SuprimerSortie/<int:id>/', views.deleteSortie, name='deleteSortie'),

    # Gestion du profile
    path('ModifierProfile', views.updateProfile, name='updateProfile'),

    # Déconnexion
    path('logout/', views.logout, name='logout'),
]