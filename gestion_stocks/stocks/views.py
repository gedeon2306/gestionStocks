from django.shortcuts import render, redirect
from django.contrib import messages
from django.forms import modelformset_factory
from django.contrib.auth.hashers import make_password, check_password
from .forms import *
from .models import *
from django.shortcuts import get_object_or_404
from django.utils.timezone import localtime
import os
from collections import defaultdict
from datetime import datetime
from django.db.models import Sum

# Inscription et Connexion
def index(request):
    form_inscription = InscriptionForm()
    form_connexion = ConnexionForm()

    if request.method == "POST":
        if "register" in request.POST:
            form_inscription = InscriptionForm(request.POST)
            if form_inscription.is_valid():
                user = form_inscription.save(commit=False)
                user.password = make_password(form_inscription.cleaned_data["password"])
                user.save()
                user.role = 'Administrateur'
                user.valide = True
                user.save()
                messages.success(request, "Votre compte a été créé avec succès !")
                return redirect("index")
            else:
                for field, errors in form_inscription.errors.items():
                    for error in errors:
                        messages.error(request, f"{field}: {error}")
                return redirect("index")
            
        elif "login" in request.POST:
            form_connexion = ConnexionForm(request.POST)
            if form_connexion.is_valid():
                username = form_connexion.cleaned_data["username"]
                password = form_connexion.cleaned_data["password"]
                
                try:
                    user = User.objects.get(username=username)
                    if check_password(password, user.password):
                        request.session["user_id"] = user.id
                        request.session["user_prenom"] = user.prenom
                        request.session["user_nom"] = user.nom
                        request.session["user_role"] = user.role
                        request.session["user_valide"] = user.valide
                        request.session["user_actif"] = user.actif

                        if request.session["user_actif"] == False:
                            del request.session["user_id"]
                            del request.session["user_prenom"]
                            del request.session["user_nom"]
                            del request.session["user_role"]
                            del request.session["user_valide"]
                            del request.session["user_actif"]
                            messages.error(request, "Votre compte est désactivé, Connexion échouée")
                            return redirect("index")

                        message = "Connexion réussie, Bienvenue {} {}".format(user.prenom, user.nom)
                        messages.success(request, message)
                        return redirect("dashboard")
                    else:
                        messages.error(request, "Nom d'utilisateur ou mot de passe incorrect")
                except User.DoesNotExist:
                    messages.error(request, "Nom d'utilisateur ou mot de passe incorrect")

    users = User.objects.all()
    if len(users)==0:
        return render(request, "stocks/insCon/inscription.html", {"form_inscription": form_inscription})
    else:
        return render(request, "stocks/insCon/connexion.html", {"form_connexion": form_connexion})

# Accueil / Tableau de bord
def dashboard(request):
    if "user_id" not in request.session:
        messages.error(request, "Veuillez vous connecter pour accéder a cette page")
        return redirect("index")
    
    produits = Produit.objects.all()
    stock = 0
    for produit in produits:
        stock+=produit.quantite_disponible

    entrees = Entree.objects.all()
    achat = 0
    for entree in entrees:
        achat+=entree.prixTotal

    sorties = Sortie.objects.all()
    vente = 0
    for sortie in sorties:
        vente+=sortie.prixTotal
    
    context = {
        'user' : get_object_or_404(User, id=request.session["user_id"]),
        'utilisateurs' : User.objects.all(),
        'stock' : stock,
        'achat' : achat,
        'vente' : vente,
    }

    return render(request, "stocks/dashboard.html", context)

# Statistiques
def entreeParMois():
    """
    Récupère le nombre d'entrées pour chaque mois en traitant les données en Python.

    Returns:
        dict: Un dictionnaire où les clés sont les mois (au format YYYY-MM)
              et les valeurs sont le nombre d'entrées pour ce mois.
    """
    entries = Entree.objects.all().order_by('date')
    monthly_counts = defaultdict(int)
    for entry in entries:
        month_year = entry.date.strftime('%Y-%m')
        monthly_counts[month_year] += 1
    return dict(monthly_counts)

def sortieParMois():
    """
    Récupère le nombre d'entrées pour chaque mois en traitant les données en Python.

    Returns:
        dict: Un dictionnaire où les clés sont les mois (au format YYYY-MM)
              et les valeurs sont le nombre d'entrées pour ce mois.
    """
    sorties = Sortie.objects.all().order_by('date')
    monthly_counts = defaultdict(int)
    for sortie in sorties:
        if sortie.motif != "Destructions(Produits périmés)":
            month_year = sortie.date.strftime('%Y-%m')
            monthly_counts[month_year] += 1
    return dict(monthly_counts)

def produitDetruitParMois():
    """
    Récupère le nombre d'entrées pour chaque mois en traitant les données en Python.

    Returns:
        dict: Un dictionnaire où les clés sont les mois (au format YYYY-MM)
              et les valeurs sont le nombre d'entrées pour ce mois.
    """
    sorties = Sortie.objects.all().order_by('date')
    monthly_counts = defaultdict(int)
    for sortie in sorties:
        if sortie.motif == "Destructions(Produits périmés)":
            month_year = sortie.date.strftime('%Y-%m')
            monthly_counts[month_year] += 1
    return dict(monthly_counts)

def prixEntreeParMois():
    """
    Récupère le prix total des entrées pour chaque mois en traitant les données en Python.

    Returns:
        dict: Un dictionnaire où les clés sont les mois (au formatYYYY-MM)
              et les valeurs sont le prix total des entrées pour ce mois.
    """
    entries = Entree.objects.all().order_by('date')
    monthly_prices = defaultdict(float)
    for entry in entries:
        month_year = entry.date.strftime('%Y-%m')
        monthly_prices[month_year] += float(entry.prixTotal)
    return dict(monthly_prices)

def prixSortieParMois():
    """
    Récupère le prix total des entrées pour chaque mois en traitant les données en Python.

    Returns:
        dict: Un dictionnaire où les clés sont les mois (au formatYYYY-MM)
              et les valeurs sont le prix total des entrées pour ce mois.
    """
    sorties = Sortie.objects.all().order_by('date')
    monthly_prices = defaultdict(float)
    for sortie in sorties:
        if sortie.motif != "Destructions(Produits périmés)":
            month_year = sortie.date.strftime('%Y-%m')
            monthly_prices[month_year] += float(sortie.prixTotal)
    return dict(monthly_prices)

def prixDestructionParMois():
    """
    Récupère le prix total des entrées pour chaque mois en traitant les données en Python.

    Returns:
        dict: Un dictionnaire où les clés sont les mois (au formatYYYY-MM)
              et les valeurs sont le prix total des entrées pour ce mois.
    """
    sorties = Sortie.objects.all().order_by('date')
    monthly_prices = defaultdict(float)
    for sortie in sorties:
        if sortie.motif == "Destructions(Produits périmés)":
            month_year = sortie.date.strftime('%Y-%m')
            monthly_prices[month_year] += float(sortie.prixTotal)
    return dict(monthly_prices)

def stats(request):
    if "user_id" not in request.session:
        messages.error(request, "Veuillez vous connecter pour accéder a cette page")
        return redirect("index")
    
    admin = 0
    gest = 0
    consu = 0
    actif = 0
    noActif = 0
    utilisateurs = User.objects.all()

    for utilisateur in utilisateurs:
        if utilisateur.role == 'Administrateur':
            admin += 1
        elif utilisateur.role == 'Gestionnaire de stock':
            gest+=1
        else:
            consu+=1
        
        if utilisateur.actif == True:
            actif +=1
        else:
            noActif +=1


    monthly_entry_data = entreeParMois()
    monthly_price_data = prixEntreeParMois()

    monthly_sortie_data = sortieParMois()
    monthly_priceSortie_data = prixSortieParMois()

    produitDetruit = produitDetruitParMois()
    prixDestruction = prixDestructionParMois()

    months_entry = list(monthly_entry_data.keys())
    counts_entry = list(monthly_entry_data.values())
    prices_entry = [monthly_price_data.get(month, 0) for month in months_entry] # Assurer l'alignement des mois

    months_sortie = list(monthly_sortie_data.keys())
    counts_sortie = list(monthly_sortie_data.values())
    prices_sortie = [monthly_priceSortie_data.get(month, 0) for month in months_sortie] # Assurer l'alignement des mois
    
    months_destruction = list(produitDetruit.keys())
    counts_destruction = list(produitDetruit.values())
    prices_destruction = [prixDestruction.get(month, 0) for month in months_sortie] # Assurer l'alignement des mois

    context = {
        'months_entry': months_entry,
        'entry_counts': counts_entry,
        'prices_entry': prices_entry,

        'months_sortie': months_sortie,
        'sortie_counts': counts_sortie,
        'prices_sortie': prices_sortie,

        'months_destruction': months_destruction,
        'destruction_counts': counts_destruction,
        'prices_destruction': prices_destruction,

        'user' : get_object_or_404(User, id=request.session["user_id"]),
        'admin':admin,
        'gest':gest,
        'consu':consu,
        'actif':actif,
        'noActif':noActif,
    }

    return render(request, "stocks/stats.html", context)

# Gestion des Utilisateurs
def listeUtilisateurs(request):
    if "user_id" not in request.session:
        messages.error(request, "Veuillez vous connecter pour accéder a cette page")
        return redirect("index")
    
    if request.session["user_role"] != 'Administrateur':
        messages.error(request, "Accès non autorisé")
        return redirect(request.META.get('HTTP_REFERER', 'dashboard'))
    
    user=get_object_or_404(User, id=request.session["user_id"])
    users = User.objects.all()
    return render(request, "stocks/utilisateurs/users.html", {"user": user, "users":users})

def addUser(request):
    if "user_id" not in request.session:
        messages.error(request, "Veuillez vous connecter pour accéder a cette page")
        return redirect("index")
    
    if request.session["user_role"] != 'Administrateur':
        messages.error(request, "Accès non autorisé")
        return redirect(request.META.get('HTTP_REFERER', 'dashboard'))

    form_addUser = CreateUserForm()

    if request.method == "POST":
        form_addUser = CreateUserForm(request.POST)
        if form_addUser.is_valid():
            user = form_addUser.save(commit=False)
            user.password = make_password(form_addUser.cleaned_data["password"])
            user.save()
            messages.success(request, "Utilisateur créé avec succès !")
            return redirect("listeUtilisateurs")
        else:
            for field, errors in form_addUser.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
            return redirect("addUser")
    
    user=get_object_or_404(User, id=request.session["user_id"])
    return render(request, "stocks/utilisateurs/add-user.html", {"form_addUser":form_addUser, "user":user})

def showUser(request, id):
    if "user_id" not in request.session:
        messages.error(request, "Veuillez vous connecter pour accéder a cette page")
        return redirect("index")
    
    if request.session["user_role"] != 'Administrateur':
        messages.error(request, "Accès non autorisé")
        return redirect(request.META.get('HTTP_REFERER', 'dashboard'))
    
    utilisateur=get_object_or_404(User, id=id)
    user=get_object_or_404(User, id=request.session["user_id"])
    return render(request, "stocks/utilisateurs/view-user.html", {'user':user, 'utilisateur':utilisateur})

def updateUser(request, id):
    if "user_id" not in request.session:
        messages.error(request, "Veuillez vous connecter pour accéder a cette page")
        return redirect("index")
    
    if request.session["user_role"] != 'Administrateur':
        messages.error(request, "Accès non autorisé")
        return redirect(request.META.get('HTTP_REFERER', 'dashboard'))

    utilisateur = get_object_or_404(User, id=id)
    form_updateUser = UpdateUserForm(instance=utilisateur)

    if request.method == "POST":
        form_updateUser = UpdateUserForm(request.POST, instance=utilisateur)
        if form_updateUser.is_valid():
            user = form_updateUser.save(commit=True)
            messages.success(request, "Utilisateur modifier avec succès !")
            return redirect("listeUtilisateurs")
        else:
            for field, errors in form_updateUser.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
            return redirect("updateUser")
    
    user=get_object_or_404(User, id=request.session["user_id"])
    return render(request, "stocks/utilisateurs/edit-user.html", {"form_updateUser":form_updateUser, "user":user})

def deleteUser(request, id):
    if "user_id" not in request.session:
        messages.error(request, "Veuillez vous connecter pour accéder a cette page")
        return redirect("index")
    
    if request.session["user_role"] != 'Administrateur':
        messages.error(request, "Accès non autorisé")
        return redirect(request.META.get('HTTP_REFERER', 'dashboard'))
    
    user = get_object_or_404(User, id=id)
    user.delete()
    messages.info(request, "Utilisateur supprimé avec succès !")
    return redirect("listeUtilisateurs")

def actif(request, id, action):
    if "user_id" not in request.session:
        messages.error(request, "Veuillez vous connecter pour accéder a cette page")
        return redirect("index")
    
    if request.session["user_role"] != 'Administrateur':
        messages.error(request, "Accès non autorisé")
        return redirect(request.META.get('HTTP_REFERER', 'dashboard'))
    
    if action == "activer":
        user=get_object_or_404(User, id=id)
        user.actif = True
        user.save()
        messages.success(request, "Compte activé")
        return redirect(request.META.get('HTTP_REFERER', 'listeUtilisateurs'))
    else:
        user=get_object_or_404(User, id=id)
        user.actif = False
        user.save()
        messages.success(request, "Compte désactivé")
        return redirect(request.META.get('HTTP_REFERER', 'listeUtilisateurs'))

# Gestion des Fournisseurs
def listeFournisseurs(request):
    if "user_id" not in request.session:
        messages.error(request, "Veuillez vous connecter pour accéder a cette page")
        return redirect("index")
    
    user=get_object_or_404(User, id=request.session["user_id"])
    fournisseurs = Fournisseur.objects.all()
    return render(request, "stocks/fournisseurs/fournisseurs.html", {"user": user, "fournisseurs":fournisseurs})

def addFournisseur(request):
    if "user_id" not in request.session:
        messages.error(request, "Veuillez vous connecter pour accéder a cette page")
        return redirect("index")
    
    if request.session["user_role"] == 'Consultant':
        messages.error(request, "Accès non autorisé")
        return redirect(request.META.get('HTTP_REFERER', 'dashboard'))

    form_addFournisseur = FournisseurForm()

    if request.method == "POST":
        form_addFournisseur = FournisseurForm(request.POST)
        if form_addFournisseur.is_valid():
            form_addFournisseur.save(commit=True)
            messages.success(request, "Fournisseur créé avec succès")
            return redirect("listeFournisseurs")
        else:
            for field, errors in form_addFournisseur.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
            return redirect("addFournisseur")
    
    user=get_object_or_404(User, id=request.session["user_id"])
    return render(request, "stocks/fournisseurs/add-fournisseur.html", {"form_addFournisseur":form_addFournisseur, "user":user})

def showFournisseur(request, id):
    if "user_id" not in request.session:
        messages.error(request, "Veuillez vous connecter pour accéder a cette page")
        return redirect("index")
    
    fournisseur=get_object_or_404(Fournisseur, id=id)
    entrees = fournisseur.produits.all()
    produits = Produit.objects.filter(entree__in=entrees)
    user=get_object_or_404(User, id=request.session["user_id"])
    return render(request, "stocks/fournisseurs/view-fournisseur.html", {'user':user, 'fournisseur':fournisseur, 'produits': produits})

def updateFournisseur(request, id):
    if "user_id" not in request.session:
        messages.error(request, "Veuillez vous connecter pour accéder a cette page")
        return redirect("index")
    
    if request.session["user_role"] == 'Consultant':
        messages.error(request, "Accès non autorisé")
        return redirect(request.META.get('HTTP_REFERER', 'dashboard'))

    fournisseur = get_object_or_404(Fournisseur,id=id)
    form_updateFournisseur = FournisseurForm(instance=fournisseur)

    if request.method == "POST":
        form_updateFournisseur = FournisseurForm(request.POST, instance=fournisseur)
        if form_updateFournisseur.is_valid():
            form_updateFournisseur.save(commit=True)
            messages.success(request, "Fournisseur modifier avec succès")
            return redirect("listeFournisseurs")
        else:
            for field, errors in form_updateFournisseur.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
            return redirect("updateFournisseur")
    
    user=get_object_or_404(User, id=request.session["user_id"])
    return render(request, "stocks/fournisseurs/edit-fournisseur.html", {"form_updateFournisseur":form_updateFournisseur, "user":user})

def deleteFournisseur(request, id):
    if "user_id" not in request.session:
        messages.error(request, "Veuillez vous connecter pour accéder a cette page")
        return redirect("index")
    
    if request.session["user_role"] == 'Consultant':
        messages.warning(request, "Accès non autorisé")
        return redirect(request.META.get('HTTP_REFERER', 'dashboard'))
    
    fournisseur = get_object_or_404(Fournisseur, id=id)
    fournisseur.delete()
    messages.info(request, "Fournisseur supprimé avec succès !")
    return redirect("listeFournisseurs")

# Gestion des produits
def listeProduits(request):
    if "user_id" not in request.session:
        messages.error(request, "Veuillez vous connecter pour accéder a cette page")
        return redirect("index")
    
    user=get_object_or_404(User, id=request.session["user_id"])
    produits = Produit.objects.all()
    return render(request, "stocks/produits/produits.html", {"user": user, "produits":produits})

def showProduit(request, id):
    if "user_id" not in request.session:
        messages.error(request, "Veuillez vous connecter pour accéder a cette page")
        return redirect("index")
    
    produit=get_object_or_404(Produit, id=id)
    user=get_object_or_404(User, id=request.session["user_id"])
    return render(request, "stocks/produits/view-produit.html", {'user':user, 'produit':produit})

def updateProduit(request, id):
    if "user_id" not in request.session:
        messages.error(request, "Veuillez vous connecter pour accéder a cette page")
        return redirect("index")
    
    if request.session["user_role"] == 'Consultant':
        messages.error(request, "Accès non autorisé")
        return redirect(request.META.get('HTTP_REFERER', 'dashboard'))

    produit = get_object_or_404(Produit,id=id)
    form_updateProduit = UpdateProduitForm(instance=produit)

    if request.method == "POST":
        form_updateProduit = UpdateProduitForm(request.POST, instance=produit)
        if form_updateProduit.is_valid():
            produit = form_updateProduit.save(commit=False)
            produit.prix_total = produit.quantite_fournie * produit.prix_achat_unitaire
            produit.save()

            produits = Produit.objects.filter(entree_id = produit.entree_id)
            entree = Entree.objects.get(pk = produit.entree_id)
            prix_total = 0

            for prod in produits:
                prix_total += prod.prix_total
            
            entree.prixTotal = prix_total
            entree.save()

            messages.success(request, "Produit modifier avec succès")
            return redirect("listeProduits")
        else:
            for field, errors in form_updateProduit.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
            return redirect("updateProduit")
    
    user=get_object_or_404(User, id=request.session["user_id"])
    return render(request, "stocks/produits/edit-produit.html", {"form_updateProduit":form_updateProduit, "user":user})

def deleteProduit(request, id):
    if "user_id" not in request.session:
        messages.error(request, "Veuillez vous connecter pour accéder a cette page")
        return redirect("index")
    
    if request.session["user_role"] == 'Consultant':
        messages.warning(request, "Accès non autorisé")
        return redirect(request.META.get('HTTP_REFERER', 'dashboard'))
    
    produit = get_object_or_404(Produit, id=id)
    produit.delete()

    produits = Produit.objects.filter(entree_id = produit.entree_id)
    entree = Entree.objects.get(pk = produit.entree_id)
    prix_total = 0

    for prod in produits:
        prix_total += prod.prix_total
    
    entree.prixTotal = prix_total
    entree.save()

    messages.info(request, "Produit supprimé avec succès !")
    return redirect(request.META.get('HTTP_REFERER', 'listeProduits'))

# Gestion des entrées
def listeEntrees(request):
    if "user_id" not in request.session:
        messages.error(request, "Veuillez vous connecter pour accéder a cette page")
        return redirect("index")
    
    user=get_object_or_404(User, id=request.session["user_id"])
    entrees = Entree.objects.all()
    return render(request, "stocks/entrees/entrees.html", {"user": user, "entrees":entrees})

def addEntree(request):
    if "user_id" not in request.session:
        messages.error(request, "Veuillez vous connecter pour accéder a cette page")
        return redirect("index")
    
    if request.session["user_role"] == 'Consultant':
        messages.warning(request, "Accès non autorisé")
        return redirect(request.META.get('HTTP_REFERER', 'dashboard'))

    ProduitFormSet = modelformset_factory(Produit, form=ProduitForm, extra=1, can_delete=True)

    if request.method == "POST":
        form_addEntree = EntreeForm(request.POST)
        formset = ProduitFormSet(request.POST)

        if form_addEntree.is_valid() and formset.is_valid():
            entree = form_addEntree.save(commit=False)
            entree.user = get_object_or_404(User, id=request.session["user_id"])
            entree.prixTotal = 0 
            entree.date = localtime(entree.date)
            entree.save()

            # Traitement des produits
            for form in formset:
                if form.cleaned_data and not form.cleaned_data.get('DELETE', False):
                    produit = form.save(commit=False)
                    produit.entree = entree  # Associer au bon "Entree"
                    produit.quantite_disponible = produit.quantite_fournie  # Maj quantité
                    produit.prix_total = produit.quantite_fournie * produit.prix_achat_unitaire
                    
                    # Mise à jour du prix total de l'entrée
                    entree.prixTotal += produit.prix_total

                    produit.save()

            # Sauvegarde du prix total mis à jour
            entree.save()
            messages.success(request, "Entrée enregistré avec succès")
            return redirect('listeEntrees')
        else:
            for field, errors in form_addEntree.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")

            for form in formset:
                for field, errors in form.errors.items():
                    for error in errors:
                        messages.error(request, f"{field}: {error}")

            return redirect("addEntree")

    else:
        form_addEntree = EntreeForm()
        formset = ProduitFormSet(queryset=Produit.objects.none())  # Formset vide au départ
        user = get_object_or_404(User, id=request.session["user_id"])

    return render(request, 'stocks/entrees/add-entree.html', {
        'form_addEntree': form_addEntree,
        'formset': formset,
        'user':user
    })

def showProduitsEntrees(request, id):
    if "user_id" not in request.session:
        messages.error(request, "Veuillez vous connecter pour accéder a cette page")
        return redirect("index")
    
    entree = get_object_or_404(Entree, id=id) 
    produits=Produit.objects.filter(entree_id=id)
    user=get_object_or_404(User, id=request.session["user_id"])
    return render(request, "stocks/entrees/produitsEntrees.html", {'user':user, 'produits':produits, 'entree':entree})

def deleteEntree(request, id):
    if "user_id" not in request.session:
        messages.error(request, "Veuillez vous connecter pour accéder a cette page")
        return redirect("index")
    
    if request.session["user_role"] == 'Consultant':
        messages.warning(request, "Accès non autorisé")
        return redirect(request.META.get('HTTP_REFERER', 'dashboard'))
    
    entree = get_object_or_404(Entree, id=id)
    entree.delete()

    messages.info(request, "Entrée supprimée avec succès !")
    return redirect("listeEntrees")

# Gestion des sorties
def listeSorties(request):
    if "user_id" not in request.session:
        messages.error(request, "Veuillez vous connecter pour accéder a cette page")
        return redirect("index")
    
    user=get_object_or_404(User, id=request.session["user_id"])
    sorties = Sortie.objects.all()
    return render(request, "stocks/sorties/sorties.html", {"user": user, "sorties":sorties})

def addSortie(request):
    if "user_id" not in request.session:
        messages.error(request, "Veuillez vous connecter pour accéder a cette page")
        return redirect("index")
    
    if request.session["user_role"] == 'Consultant':
        messages.warning(request, "Accès non autorisé")
        return redirect(request.META.get('HTTP_REFERER', 'dashboard'))

    ProduitFormSet = modelformset_factory(ProduitSortie, form=ProduitSortieForm, extra=1, can_delete=True)

    if request.method == "POST":
        form_addSortie = SortieForm(request.POST)
        formset = ProduitFormSet(request.POST)

        if form_addSortie.is_valid() and formset.is_valid():
            sortie = form_addSortie.save(commit=False)
            sortie.user = get_object_or_404(User, id=request.session["user_id"])
            sortie.prixTotal = 0 
            sortie.date = localtime(sortie.date)
            sortie.save()

            # Traitement des produits
            for form in formset:
                if form.cleaned_data and not form.cleaned_data.get('DELETE', False):
                    produit = form.save(commit=False)
                    # breakpoint()
                    prod = form.cleaned_data['nom']
                    if prod.quantite_disponible >= produit.quantite_sortie:
                        produit.nom = prod.nom
                        produit.reference = prod.reference
                        produit.prix_vente = prod.prix_vente
                        produit.prixTotal = prod.prix_vente * produit.quantite_sortie
                        prod.quantite_disponible -= produit.quantite_sortie
                        prod.save()
                    else:
                        sortie.delete()
                        messages.error(request, "Stock insuffisant")
                        return redirect('addSortie')
                    produit.sortie = sortie  # Associer à la bonne "sortie"
                    
                    # Mise à jour du prix total de l'entrée
                    sortie.prixTotal += produit.prixTotal

                    produit.save()

            # Sauvegarde du prix total mis à jour
            sortie.save()
            messages.success(request, "Sortie effectuée avec succès")
            return redirect('listeSorties')
        else:
            for field, errors in form_addSortie.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")

            for form in formset:
                for field, errors in form.errors.items():
                    for error in errors:
                        messages.error(request, f"{field}: {error}")

            return redirect("addSortie")

    else:
        form_addSortie = SortieForm()
        formset = ProduitFormSet(queryset=ProduitSortie.objects.none())  # Formset vide au départ
        user = get_object_or_404(User, id=request.session["user_id"])

    return render(request, 'stocks/sorties/add-sortie.html', {
        'form_addSortie': form_addSortie,
        'formset': formset,
        'user':user
    })

def showProduitsSorties(request, id):
    if "user_id" not in request.session:
        messages.error(request, "Veuillez vous connecter pour accéder a cette page")
        return redirect("index")
    
    sortie = get_object_or_404(Sortie, id=id) 
    produits=ProduitSortie.objects.filter(sortie_id=id)
    user=get_object_or_404(User, id=request.session["user_id"])
    return render(request, "stocks/sorties/produitsSorties.html", {'user':user, 'produits':produits, 'sortie':sortie})

def deleteSortie(request, id):
    if "user_id" not in request.session:
        messages.error(request, "Veuillez vous connecter pour accéder a cette page")
        return redirect("index")
    
    if request.session["user_role"] == 'Consultant':
        messages.warning(request, "Accès non autorisé")
        return redirect(request.META.get('HTTP_REFERER', 'dashboard'))
    
    sortie = get_object_or_404(Sortie, id=id)
    sortie.delete()

    messages.info(request, "Sortie supprimée avec succès !")
    return redirect("listeSorties")

# Modifier le profile
def updateProfile(request):
    if "user_id" not in request.session:
        messages.error(request, "Veuillez vous connecter pour accéder à cette page")
        return redirect("index")
    
    user=get_object_or_404(User, id=request.session["user_id"])
    form_modifier_user = UpdateUserProfileForm(instance=user)
    
    if request.method == "POST":
        user = User.objects.get(id=request.session["user_id"])
        form_modifier_user = UpdateUserProfileForm(request.POST, request.FILES, instance=user)
        
        if form_modifier_user.is_valid():
            user = form_modifier_user.save(commit=False)
            
            # Gestion du mot de passe
            current_password = form_modifier_user.cleaned_data.get("current_password")
            new_password = form_modifier_user.cleaned_data.get("new_password")
            
            if new_password:
                if not check_password(current_password, user.password):
                    messages.error(request, "Le mot de passe actuel est incorrect")
                    return redirect("updateProfile")
                user.password = make_password(new_password)
            
            # Gestion de la photo de profil
            if "photo_profil" in request.FILES:
                # Supprimer l'ancienne photo si elle existe
                if user.photo_profil:
                    if os.path.exists(user.photo_profil.path):
                        os.remove(user.photo_profil.path)
                
                user.photo_profil = request.FILES["photo_profil"]
            
            user.save()
            messages.success(request, "Profil modifié avec succès !")
            
            # Si le mot de passe a été changé, déconnecter l'utilisateur
            if new_password:
                del request.session["user_id"]
                del request.session["user_prenom"]
                del request.session["user_nom"]
                del request.session["user_role"]
                del request.session["user_valide"]
                del request.session["user_actif"]
                return redirect("index")
            
            return redirect("updateProfile")
        else:
            for field, errors in form_modifier_user.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
            return redirect("updateProfile")
            
    return render(request, "stocks/edit-profile.html", {"user": user, "form_updateProfile": form_modifier_user})

# Déconnexion
def logout(request):
    if "user_id" in request.session:
        del request.session["user_id"]
        del request.session["user_prenom"]
        del request.session["user_nom"]
        del request.session["user_role"]
        del request.session["user_valide"]
        del request.session["user_actif"]
        messages.success(request, "Vous avez été déconnecté avec succès")
    return redirect("index")








