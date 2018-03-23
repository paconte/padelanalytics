from django.shortcuts import render, redirect
from anmeldung.forms import FullRegistrationForm
from anmeldung.models import get_tournament, get_tournaments, get_tournament_teams_by_ranking, get_clubs, \
    get_similar_tournaments


def index(request):
    return render(request, 'landing.html')


def tournament_signup(request, id=None):
    if request.method == 'POST':
        registration_form = FullRegistrationForm(request.POST)
        if registration_form.is_valid():
            registration_form.save()
            return redirect('tournament', registration_form.cleaned_data['tournament_name'].id)
        else:
            print('Form is INvalid :(')
            print(registration_form.errors)
            return render(request, 'anmeldung.html', {'form': registration_form})
    else:
        if id:
            form = FullRegistrationForm(initial={'tournament_name': id})
        else:
            form = FullRegistrationForm()
        return render(request, 'anmeldung.html', {'form': form})


def turnierliste(request):
    tournaments = get_tournaments()
    return render(request, 'turnierliste.html', {'tournaments': tournaments})


def tournament(request, id):
    teams = get_tournament_teams_by_ranking(id)
    tournament = get_tournament(id)
    similar_tournaments = get_similar_tournaments(id)
    print(tournament, similar_tournaments)
    return render(request, 'tournament.html',
                  {'tournament': tournament, 'teams': teams, 'similar_tournaments': similar_tournaments})


def clubs(request):
    clubs = get_clubs()
    return render(request, 'clubs.html', {'clubs': clubs})

