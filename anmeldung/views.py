from django.shortcuts import render
from anmeldung.forms import FullRegistrationForm


def index(request):
    return render(request, 'landing.html')


def anmeldung(request):
    if request.method == 'POST':
        # registration_form = RegistrationForm(request.POST)
        registration_form = FullRegistrationForm(request.POST)
        if registration_form.is_valid():
            registration_form.save()
            return render(request, 'turnierliste.html')
        else:
            print('Form is INvalid :(')
            print(registration_form.errors)
            return render(request, 'anmeldung.html', {'form': registration_form})
    else:
        # return render(request, 'anmeldung.html', {'form': RegistrationForm()})
        return render(request, 'anmeldung.html', {'form': FullRegistrationForm()})


def turnierliste(request):
    return render(request, 'turnierliste.html')


