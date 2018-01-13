from django.shortcuts import render
from django import forms
from anmeldung.models import Registration, CATEGORY_GERMANY


class RegistrationForm(forms.ModelForm):
    category = forms.ChoiceField(choices=CATEGORY_GERMANY, widget=forms.RadioSelect)

    class Meta:
        model = Registration
        fields = '__all__'
        widgets = {
            'player': forms.TextInput(attrs={'placeholder': 'Hast du bereits ein GPS - Turnier gespielt? Such dich!'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Mail-Adresse'}),
            'surname': forms.TextInput(attrs={'placeholder': 'Familienname'}),
            'forename': forms.TextInput(attrs={'placeholder': 'Vorname'}),
            'phone': forms.TextInput(attrs={'placeholder': 'Telefonnummer'}),
            'city': forms.TextInput(attrs={'placeholder': 'Wohnort'}),
            'club': forms.TextInput(attrs={'placeholder': 'Verein'}),
            'birthplace': forms.TextInput(attrs={'placeholder': 'Geburtsort'}),
            'ranking_points': forms.TextInput(attrs={'placeholder': 'Trag deine Punkte ein'}),
            'birthdate': forms.TextInput(attrs={'placeholder': 'TT/MM/JJJJ'}),
        }


def index(request):
    return render(request, 'landing.html')


def anmeldung(request):
    if request.method == 'POST':
        registration_form = RegistrationForm(request.POST)
        if registration_form.is_valid():
            return render(request, 'turnierliste.html')
        else:
            return render(request, 'anmeldung.html', {'form': registration_form})
    else:
        return render(request, 'anmeldung.html', {'form': RegistrationForm()})


def turnierliste(request):
    return render(request, 'turnierliste.html')


