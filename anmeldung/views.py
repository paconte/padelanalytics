from django.shortcuts import render
from anmeldung.forms import FullRegistrationForm
from anmeldung.models import get_tournaments


def index(request):
    return render(request, 'landing.html')


def anmeldung(request):
    if request.method == 'POST':
        registration_form = FullRegistrationForm(request.POST)
        if registration_form.is_valid():
            registration_form.save()
            return render(request, 'turnierliste.html')
        else:
            print('Form is INvalid :(')
            print(registration_form.errors)
            return render(request, 'anmeldung.html', {'form': registration_form})
    else:
        return render(request, 'anmeldung.html', {'form': FullRegistrationForm()})


def turnierliste(request):
    tournaments = get_tournaments()
    print(tournaments)
    return render(request, 'turnierliste.html', {'tournaments': tournaments})


def tournament(request, id):
    print(id)
    return render(request, 'tournament.html')


