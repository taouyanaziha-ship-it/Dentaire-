from django import forms
from .models import Patient, Dentiste, Rendezvous,Recu

class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ['nom', 'prenom', 'email', 'telephone', 'date_naissance']

        widgets = {
            'nom': forms.TextInput(attrs={
                'class': 'form-control mb-3',
                'placeholder': 'Entrer le nom'
            }),

            'prenom': forms.TextInput(attrs={
                'class': 'form-control mb-3',
                'placeholder': 'Entrer le prénom'
            }),

            'email': forms.EmailInput(attrs={
                'class': 'form-control mb-3',
                'placeholder': 'exemple@gmail.com'
            }),

            'telephone': forms.TextInput(attrs={
                'class': 'form-control mb-3',
                'placeholder': 'Entrer le téléphone'
            }),

            'date_naissance': forms.DateInput(attrs={
                'class': 'form-control mb-3',
                'type': 'date'
            }),
        }
class DentisteForm(forms.ModelForm):
    class Meta:
        model = Dentiste
        fields = ['nom', 'specialite', 'telephone', 'email']
        widgets = {
            'nom': forms.TextInput(attrs={
                'class': 'form-control mb-3',
                'placeholder': 'Entrer le nom'
            }),
            'specialite': forms.TextInput(attrs={
                'class': 'form-control mb-3',
                'placeholder': 'Entrer la spécialité'
            }),
            'telephone': forms.TextInput(attrs={
                'class': 'form-control mb-3',
                'placeholder': 'Entrer le téléphone'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control mb-3',
                'placeholder': 'exemple@gmail.com'
            }),
        }
class RendezvousForm(forms.ModelForm):
    class Meta:
        model = Rendezvous
        fields = ['patient', 'dentiste', 'date', 'heure', 'motif', 'statut']
        widgets = {
            'patient': forms.Select(attrs={
                'class': 'form-control mb-3',
            }),
            'dentiste': forms.Select(attrs={
                'class': 'form-control mb-3',
            }),
            'date': forms.DateInput(attrs={
                'class': 'form-control mb-3',
                'type': 'date'
            }),
            'heure': forms.TimeInput(attrs={
                'class': 'form-control mb-3',
                'type': 'time'
            }),
            'motif': forms.Textarea(attrs={
                'class': 'form-control mb-3',
                'rows': 3
            }),
            'statut': forms.TextInput(attrs={
                'class': 'form-control mb-3',
            }),
        }
class RecuForm(forms.ModelForm):
    class Meta:
        model  = Recu
        fields = ['montant', 'mode_paiement']
        widgets = {
            'montant':       forms.NumberInput(attrs={'class': 'form-control mb-3'}),
            'mode_paiement': forms.Select(attrs={'class': 'form-control mb-3'}),
        }