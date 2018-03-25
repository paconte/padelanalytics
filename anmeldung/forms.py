from django import forms
from anmeldung.models import Club, Player, Registration


class RegistrationForm(forms.ModelForm):
    class Meta:
        model = Registration
        fields = '__all__'
        exclude = ['creation_date']


class NewPlayerForm(forms.ModelForm):
    class Meta:
        model = Player
        exclude = ['creation_date', 'surname2', 'country', 'ranking_points', 'photo']
        widgets = {
            'email': forms.EmailInput(attrs={'placeholder': 'Mail-Adresse'}),
            'surname': forms.TextInput(attrs={'placeholder': 'Familienname'}),
            'forename': forms.TextInput(attrs={'placeholder': 'Vorname'}),
            'phone': forms.TextInput(attrs={'placeholder': 'Telefonnummer'}),
            'city': forms.TextInput(attrs={'placeholder': 'Wohnort'}),
            'club': forms.Select(choices=Club.objects.all(), attrs={'placeholder': 'Verein'}),
            'birthplace': forms.TextInput(attrs={'placeholder': 'Geburtsort'}),
            'birthdate': forms.TextInput(attrs={'placeholder': 'Geburtsdatum'}),
            'policy_read': forms.CheckboxInput(attrs={'placeholder': 'Muerte con pinchos'})
        }
