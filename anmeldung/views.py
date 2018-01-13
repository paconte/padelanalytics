from django.shortcuts import render
from anmeldung.forms import RegistrationForm


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


