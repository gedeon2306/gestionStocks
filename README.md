## G-Stocks – Application de gestion de stocks

G-Stocks est une application web développée avec **Django** pour gérer le stock de produits alimentaires d’une structure (magasin, entrepôt, restaurant, etc.).  
Elle permet de suivre les **entrées**, **sorties**, **fournisseurs**, **produits**, les **utilisateurs** et de visualiser des **statistiques** complètes.

### Fonctionnalités principales

- **Authentification & sécurité**
  - Inscription du tout premier utilisateur (initialisation) puis formulaire de connexion.
  - Authentification par nom d’utilisateur / mot de passe (hashés).
  - Gestion de session personnalisée (stockage de l’ID et des infos de l’utilisateur en session).
  - Déconnexion sécurisée.

- **Rôles & gestion des utilisateurs**
  - Rôles disponibles : **Administrateur**, **Gestionnaire de stock**, **Consultant**.
  - L’utilisateur créé lors de l’inscription initiale devient automatiquement **Administrateur** et est validé.
  - Liste des utilisateurs avec leurs informations.
  - Création, modification et suppression d’utilisateurs.
  - Activation / désactivation de comptes (un utilisateur désactivé ne peut pas se connecter).
  - Gestion fine des droits :
    - Seul l’**Administrateur** gère les utilisateurs (CRUD, activation, désactivation).
    - Le **Consultant** a un accès **lecture seule** sur les données métier (pas de création / modification / suppression).

- **Gestion du profil utilisateur**
  - Modification des informations personnelles (prénom, nom, email, téléphone, username).
  - Changement de mot de passe avec vérification de l’ancien mot de passe.
  - Mise à jour de la photo de profil avec suppression automatique de l’ancienne image.

- **Gestion des fournisseurs**
  - Liste complète des fournisseurs.
  - Création, modification et suppression d’un fournisseur.
  - Visualisation du détail d’un fournisseur, de ses entrées et des produits associés.
  - Accès d’édition réservé aux rôles autorisés (pas de modification pour le Consultant).

- **Gestion des produits**
  - Modèle produit complet :
    - Nom, référence unique, catégorie.
    - Quantité fournie / disponible.
    - Unité de mesure (kg, litre, unité).
    - Prix d’achat unitaire, prix de vente, prix total.
    - Date de péremption.
  - Liste des produits en stock.
  - Détail d’un produit.
  - Modification et suppression d’un produit (avec recalcul du prix total d’entrée).
  - Mise à jour automatique du stock disponible lors des sorties.

- **Gestion des entrées de stock**
  - Création d’une entrée associée à un **fournisseur** et à un **utilisateur**.
  - Ajout de **plusieurs produits** dans une même entrée via un formset dynamique.
  - Calcul automatique du **prix total par produit** et du **prix total de l’entrée**.
  - Liste des entrées enregistrées.
  - Détail des produits d’une entrée.
  - Suppression d’une entrée.

- **Gestion des sorties de stock**
  - Typologie des sorties : **Vente**, **Utilisations internes**, **Destructions (produits périmés)**, **Transferts entre entrepôts**.
  - Création d’une sortie associée à un **utilisateur**.
  - Ajout de **plusieurs produits sortants** via un formset.
  - Contrôle de la quantité : impossibilité de sortir plus que la quantité disponible (message d’erreur “Stock insuffisant”).
  - Mise à jour automatique de la **quantité disponible** des produits.
  - Calcul automatique du prix total par produit sorti et du **prix total de la sortie**.
  - Liste des sorties et détail des produits d’une sortie.

- **Tableau de bord (Dashboard)**
  - Accès réservé aux utilisateurs connectés.
  - Indicateurs clés :
    - Nombre total d’utilisateurs.
    - Nombre total de produits en stock (somme des quantités disponibles).
    - Montant cumulé des **achats** (somme des prix des entrées).
    - Montant cumulé des **ventes** (somme des prix des sorties).
    - Nombre de **produits bientôt expirés** (périmant dans les 30 prochains jours).
  - Vue d’accueil moderne avec cartes d’indicateurs.

- **Statistiques détaillées**
  - Statistiques par mois :
    - Nombre d’entrées par mois.
    - Nombre de sorties (hors destructions) par mois.
    - Nombre de destructions (produits périmés) par mois.
    - Montant total des entrées par mois.
    - Montant total des sorties (hors destructions) par mois.
    - Montant total des destructions par mois.
  - Répartition des utilisateurs :
    - Nombre d’Administrateurs, Gestionnaires de stock, Consultants.
    - Nombre de comptes actifs / inactifs.

### Stack technique

- **Backend** : Django 5.1 (Python)
- **Base de données** : SQLite (par défaut, configurable vers MySQL)
- **Front** : Templates Django (`stocks/templates/...`) + CSS/JS statiques
- **Langue & fuseau horaire** : Français (`fr-FR`), Afrique/Brazzaville

### Prérequis

- **Python 3.11+** (recommandé, compatible Django 5.1)
- Pip installé (`pip`)
- Optionnel : environnement virtuel (`venv`)

### Installation du projet en local

1. **Cloner le dépôt**
   - `git clone https://github.com/gedeon2306/gestionStocks`
   - `cd gestionStocks`

2. **Créer et activer un environnement virtuel (recommandé)**
   - Sous Windows PowerShell :
     - `python -m venv .env`
     - `.env\Scripts\Activate`

3. **Installer les dépendances**
   - `pip install -r gestion_stocks/requirements.txt`

4. **Appliquer les migrations**
   - `cd gestion_stocks`
   - `python manage.py migrate`

5. **Lancer le serveur de développement**
   - `python manage.py runserver`
   - Accéder à l’application sur `http://127.0.0.1:8000/`

### Utilisation de l’application

- **Inscription initiale**  
  - Si aucun utilisateur n’existe, la page d’accueil affiche le formulaire d’inscription.  
  - Le premier compte créé est automatiquement un **Administrateur** valide et actif.

- **Connexion**
  - Une fois au moins un utilisateur créé, la page d’accueil passe au formulaire de connexion.
  - Saisir le nom d’utilisateur et le mot de passe pour accéder au **dashboard**.

- **Navigation principale**
  - `/` : page d’inscription / connexion.
  - `/dashboard/` : tableau de bord.
  - `/Statistique/` : page des statistiques.
  - `/ListeDesUtilisateur`, `/ListeDesFournisseurs`, `/ListeDesProduits`, `/ListeDesEntrees`, `/ListeDesSorties` : vues de gestion métier.

### Structure fonctionnelle principale

- Application Django : `stocks`
  - `models.py` : modèles `User`, `Fournisseur`, `Entree`, `Produit`, `Sortie`, `ProduitSortie`.
  - `forms.py` : formulaires d’inscription, connexion, gestion utilisateurs, fournisseurs, produits, entrées et sorties.
  - `views.py` : logique métier (authentification, dashboard, statistiques, CRUD complet).
  - `urls.py` : routes de l’application métier.
  - `templates/stocks/...` : interfaces utilisateur (inscription/connexion, dashboard, listes, formulaires, stats, profil, etc.).

### Améliorations possibles

- Ajout d’une gestion avancée des permissions basée sur le système de permissions Django natif.
+- Export des données (CSV/Excel/PDF) pour les entrées, sorties et statistiques.
 - Intégration d’un système de notifications (email, alertes visuelles) pour les stocks faibles ou produits expirés.
