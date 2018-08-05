from django import forms

from anmeldung.models import Club
from anmeldung.models import PadelPerson
from anmeldung.models import Registration
from tournaments.models import Person


class RegistrationForm(forms.ModelForm):
    class Meta:
        model = Registration
        fields = '__all__'
        exclude = ['creation_date']


def get_new_player_form(request):
    NewPlayerInlineFormSet = get_new_player_form()
    return NewPlayerInlineFormSet(request)


def get_new_player_form():
    NewPlayerInlineFormSet = forms.inlineformset_factory(
        Person,
        PadelPerson,
        exclude=['ranking_points', 'photo'],
        widgets={
            'email': forms.EmailInput(attrs={'placeholder': 'Mail-Adresse'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Familienname'}),
            'last_name2': forms.TextInput(attrs={'placeholder': 'Familienname 2'}),
            'first_name': forms.TextInput(attrs={'placeholder': 'Vorname'}),
            'gender': forms.Select(choices=Person.GENDER_CHOICES, attrs={'placeholder': 'Geschlecht'}),
            'phone': forms.TextInput(attrs={'placeholder': 'Telefonnummer'}),
            'city': forms.TextInput(attrs={'placeholder': 'Wohnort'}),
            'club': forms.Select(choices=Club.objects.all(), attrs={'placeholder': 'Verein'}),
            'birthplace': forms.TextInput(attrs={'placeholder': 'Geburtsort'}),
            'born': forms.TextInput(attrs={'placeholder': 'Geburtsdatum'}),
            'country': forms.Select(attrs={'placeholder': 'Land'}),
            'policy_read': forms.CheckboxInput(attrs={'placeholder': 'Accept'})}
    )
    return NewPlayerInlineFormSet