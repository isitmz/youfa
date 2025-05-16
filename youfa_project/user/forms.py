from django import forms
from .models import UserProfile

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        # Includi solo i campi che l'utente può modificare o che devono essere visualizzati
        fields = ['nome', 'cognome', 'data_nascita', 'telefono', 'notifiche_attive']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'cognome': forms.TextInput(attrs={'class': 'form-control'}),
            'data_nascita': forms.DateInput(
                attrs={'class': 'form-control', 'type': 'date'},
                format='%Y-%m-%d' # Importante per il corretto rendering del valore iniziale
            ),
            'telefono': forms.TextInput(attrs={'class': 'form-control', 'type': 'tel'}),
            'notifiche_attive': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        labels = {
            'notifiche_attive': 'Attiva notifiche',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Disabilita i campi che non devono essere modificabili dall'utente
        # Django aggiungerà l'attributo 'disabled' all'HTML generato
        self.fields['nome'].disabled = True
        self.fields['cognome'].disabled = True
        self.fields['data_nascita'].disabled = True

        # L'attributo 'required' sugli input sarà gestito automaticamente da Django
        # in base alla definizione del campo nel modello/form.
        # Se un campo è obbligatorio, Django aggiungerà 'required' all'input.

    def clean_telefono(self):
        telefono = self.cleaned_data.get('telefono')
        if telefono: # Controlla solo se il campo telefono ha un valore            
            min_length = 7
            max_length = 15
            if not (min_length <= len(telefono) <= max_length):
                raise forms.ValidationError(f"Il numero di telefono deve essere compreso tra {min_length} e {max_length} caratteri.")
        return telefono