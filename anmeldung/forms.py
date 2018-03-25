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
        exclude = ['creation_date', 'ranking_points', 'photo']
        widgets = {
            'email': forms.EmailInput(attrs={'placeholder': 'Mail-Adresse'}),
            'surname': forms.TextInput(attrs={'placeholder': 'Familienname'}),
            'surname2': forms.TextInput(attrs={'placeholder': 'Familienname 2'}),
            'forename': forms.TextInput(attrs={'placeholder': 'Vorname'}),
            'phone': forms.TextInput(attrs={'placeholder': 'Telefonnummer'}),
            'city': forms.TextInput(attrs={'placeholder': 'Wohnort'}),
            'club': forms.Select(choices=Club.objects.all(), attrs={'placeholder': 'Verein'}),
            'birthplace': forms.TextInput(attrs={'placeholder': 'Geburtsort'}),
            'birthdate': forms.TextInput(attrs={'placeholder': 'Geburtsdatum'}),
            'country': forms.Select(attrs={'placeholder': 'Land'}),
            'policy_read': forms.CheckboxInput(attrs={'placeholder': 'Accept'})
        }
