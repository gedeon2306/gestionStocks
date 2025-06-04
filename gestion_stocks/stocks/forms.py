from django import forms
from .models import *

class InscriptionForm(forms.ModelForm):
    password = forms.CharField(label='Mot de passe', widget=forms.PasswordInput(
        attrs={
            'required': True,
            'id':'password'
        }
    ))
    confirm_password = forms.CharField(label='Confirmer le mot de passe', widget=forms.PasswordInput(
        attrs={
            'required': True,
            'id':'confirm-password'
        }
    ))

    class Meta:
        model = User
        fields = ['prenom', 'nom', 'email', 'username', 'telephone']
        widgets = {
            'prenom': forms.TextInput(attrs={
                'required': True,
                'id':'firstname'
            }),
            'nom': forms.TextInput(attrs={
                'required': True,
                'id':'lastname'
            }),
            'email': forms.EmailInput(attrs={
                'required': True,
                'id':'email'
            }),
            'username': forms.TextInput(attrs={
                'required': True,
                'id':'username'
            }),
            'telephone': forms.TextInput(attrs={
                'required': True,
                'id':'telephone'
            }),
        }

    def clean_confirm_password(self):
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')
        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError('Les mots de passe ne correspondent pas')
        return confirm_password

class ConnexionForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(
        attrs={
            'required': True,
            'id': 'username'
        }
    ))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'required': True,
            'id': 'password'
        }
    )) 

class CreateUserForm(forms.ModelForm):
    
    password = forms.CharField(label='Mot de passe', widget=forms.PasswordInput(
        attrs={
            'required': True,
            'id':'password'
        }
    ))
    confirm_password = forms.CharField(label='Confirmer le mot de passe', widget=forms.PasswordInput(
        attrs={
            'required': True,
            'id':'confirm-password'
        }
    ))

    class Meta:
        model = User
        fields = ['prenom', 'nom', 'email', 'username', 'telephone', 'role']
        widgets = {
            'prenom': forms.TextInput(attrs={
                'required': True,
                'id':'firstname'
            }),
            'nom': forms.TextInput(attrs={
                'required': True,
                'id':'lastname'
            }),
            'email': forms.EmailInput(attrs={
                'required': True,
                'id':'email',
                'placeholder': 'exemple1234@exemple.com'
            }),
            'username': forms.TextInput(attrs={
                'required': True,
                'id':'username'
            }),
            'telephone': forms.TextInput(attrs={
                'required': True,
                'id':'telephone'
            }),
            'role': forms.Select(attrs={
                'required': True,
                'id':'role',
            }),
        }

    def clean_confirm_password(self):
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')
        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError('Les mots de passe ne correspondent pas')
        return confirm_password

class UpdateUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['prenom', 'nom', 'email', 'telephone', 'role']
        widgets = {
            'prenom': forms.TextInput(attrs={
                'required': True,
                'id':'firstname'
            }),
            'nom': forms.TextInput(attrs={
                'required': True,
                'id':'lastname'
            }),
            'email': forms.EmailInput(attrs={
                'required': True,
                'id':'email',
                'placeholder': 'exemple1234@exemple.com'
            }),
            'telephone': forms.TextInput(attrs={
                'required': True,
                'id':'telephone'
            }),
            'role': forms.Select(attrs={
                'required': True,
                'id':'role',
            }),
        }

    def clean_confirm_password(self):
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')
        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError('Les mots de passe ne correspondent pas')
        return confirm_password

class FournisseurForm(forms.ModelForm):

    class Meta:
        model = Fournisseur
        fields = ['nom', 'contact', 'adresse']
        widgets = {
            'nom': forms.TextInput(attrs={
                'required': True,
                'id':'nom'
            }),
            'contact': forms.TextInput(attrs={
                'required': True,
                'id':'telephone'
            }),
            'adresse': forms.TextInput(attrs={
                'required': True,
                'id':'adresse',
                'placeholder':'57, Rue de la boisson'
            }),
        }

class UpdateProduitForm(forms.ModelForm):

    class Meta:
        model = Produit
        fields = ['nom', 'reference', 'categorie', 'unite_mesure', 'prix_achat_unitaire', 'prix_vente', 'date_peremption',]
        widgets = {
            'nom': forms.TextInput(attrs={
                'required': True,
                'id':'nom'
            }),
            'reference': forms.TextInput(attrs={
                'required': True,
                'id':'reference'
            }),
            'categorie': forms.TextInput(attrs={
                'required': True,
                'id':'categorie'
            }),
            'unite_mesure': forms.Select(attrs={
                'required': True,
                'id':'unite_mesure'
            }),
            'prix_achat_unitaire': forms.TextInput(attrs={
                'required': True,
                'id':'prix_achat_unitaire'
            }),
            'prix_vente': forms.TextInput(attrs={
                'required': True,
                'id':'prix_vente'
            }),
            'date_peremption': forms.TextInput(attrs={
                'required': True,
                'id':'date_peremption',
                'type': 'date'
            }),
        }

class UpdateUserProfileForm(forms.ModelForm):
    current_password = forms.CharField(
        label='Mot de passe actuel',
        widget=forms.PasswordInput(attrs={
            'id': 'current-password',
        }),
        required=False
    )
    new_password = forms.CharField(
        label='Nouveau mot de passe',
        widget=forms.PasswordInput(attrs={
            'id': 'new-password',
        }),
        required=False
    )
    confirm_password = forms.CharField(
        label='Confirmer le mot de passe',
        widget=forms.PasswordInput(attrs={
            'id': 'confirm-password',
        }),
        required=False
    )
    photo_profil = forms.ImageField(
        label='Photo de profil',
        required=False,
        widget=forms.FileInput(attrs={
            'id': 'profile-photo',
            'accept': 'image/*',
            'hidden': True
        })
    )

    class Meta:
        model = User
        fields = ['prenom', 'nom', 'email', 'telephone', 'username', 'photo_profil']
        widgets = {
            'prenom': forms.TextInput(attrs={
                'id': 'prenom',
                'required': True
            }),
            'nom': forms.TextInput(attrs={
                'id': 'nom',
                'required': True
            }),
            'email': forms.EmailInput(attrs={
                'id': 'email',
                'required': True
            }),
            'telephone': forms.TextInput(attrs={
                'id': 'telephone',
                'required': True
            }),
            'username': forms.TextInput(attrs={
                'id': 'username',
                'required': True
            })
        }

    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get('new_password')
        confirm_password = cleaned_data.get('confirm_password')
        
        if new_password and not cleaned_data.get('current_password'):
            raise forms.ValidationError('Le mot de passe actuel est requis pour changer le mot de passe')
            
        if new_password and confirm_password and new_password != confirm_password:
            raise forms.ValidationError('Les nouveaux mots de passe ne correspondent pas')
            
        return cleaned_data

class EntreeForm(forms.ModelForm):
    class Meta:
        model = Entree 
        fields = ['fournisseur']

class ProduitForm(forms.ModelForm):
    class Meta:
        model = Produit
        fields = ['nom', 'reference', 'categorie', 'quantite_fournie', 'unite_mesure', 'prix_achat_unitaire', 'prix_vente', 'date_peremption',]
        widgets = {
            'nom': forms.TextInput(attrs={
                'required': True,
                'id':'nom',
                'class':'form'
            }),
            'reference': forms.TextInput(attrs={
                'required': True,
                'id':'reference',
                'class':'form'
            }),
            'categorie': forms.TextInput(attrs={
                'required': True,
                'id':'categorie',
                'class':'form'
            }),
            'quantite_fournie': forms.TextInput(attrs={
                'required': True,
                'id':'quantite_fournie',
                'type': 'number',
                'min': '1',
                'class':'form'
            }),
            'unite_mesure': forms.Select(attrs={
                'required': True,
                'id':'unite_mesure',
                'class':'form'
            }),
            'prix_achat_unitaire': forms.TextInput(attrs={
                'required': True,
                'id':'prix_achat_unitaire',
                'type': 'number',
                'min': '1',
                'class':'form'
            }),
            'prix_vente': forms.TextInput(attrs={
                'required': True,
                'id':'prix_vente',
                'type': 'number',
                'min': '1',
                'class':'form'
            }),
            'date_peremption': forms.DateInput(attrs={
                'required': True,
                'id':'date_peremption',
                'type': 'date',
                'class':'form'
            }),
        }
    def clean_quantite_fournie(self):
        quantite = self.cleaned_data.get('quantite_fournie')
        if quantite is not None and quantite <= 1:
            raise forms.ValidationError("La quantité fournie doit être supérieure ou égale à 0.")
        return quantite

class SortieForm(forms.ModelForm):
    class Meta:
        model = Sortie
        fields = ['motif']
        widgets = {
            'motif': forms.Select(attrs={
                'required': True,
                'id':'motif',
            })
        }

class ProduitSortieForm(forms.ModelForm):
    nom = forms.ModelChoiceField(
        queryset=Produit.objects.all(),
        label="",
        widget=forms.Select(attrs={
            'required': True,
            'id':'nom',
            'class':'form'
        }),
        # empty_label="Choisissez un niveau"
    ) 
    class Meta:
        model = ProduitSortie
        fields = ['nom', 'quantite_sortie']
        widgets = {
            'quantite_sortie': forms.TextInput(attrs={
                'required': True,
                'id':'quantite_fournie',
                'type': 'number',
                'min': '1',
                'class':'form'
            })
        }
    def clean_quantite_fournie(self):
        quantite = self.cleaned_data.get('quantite_fournie')
        if quantite is not None and quantite <= 1:
            raise forms.ValidationError("La quantité fournie doit être supérieure ou égale à 0.")
        return quantite




