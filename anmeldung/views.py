from django.shortcuts import render, redirect

from anmeldung.forms import RegistrationForm, get_new_player_form
from anmeldung.models import get_padel_tournament
from anmeldung.models import get_padel_tournaments
from anmeldung.models import get_tournament_teams_by_ranking
from anmeldung.models import get_clubs
from anmeldung.models import get_similar_tournaments

from tournaments.models import get_tournament_games
from tournaments.models import get_padel_tournament_teams

from tournaments.service import Fixtures


def index(request):
    return render(request, 'landing.html')


def tournament_signup(request, id=None):
    if request.method == 'POST':
        registration_form = RegistrationForm(request.POST)
        if registration_form.is_valid():
            registration_form.save()
            return redirect('tournament', registration_form.cleaned_data['tournament'].id)
        else:
            print('Form is INvalid :(')
            print(registration_form.errors)
            return render(request, 'tournament_signup.html', {'form': registration_form})
    else:
        if id:
            form = RegistrationForm(initial={'tournament': id})
        else:
            form = RegistrationForm()
        return render(request, 'tournament_signup.html', {'form': form})


def turnierliste(request):
    tournaments = get_padel_tournaments()
    print (tournaments)
    return render(request, 'turnierliste.html', {'tournaments': tournaments})


def tournament(request, id):
    # partidos, equipos_de_verdad, equipos_anmeldeados,
    # num_de_pools, num_de_goldsilver_en_ko, num_de_ko_runde
    tournament = get_padel_tournament(id)
    similar_tournaments = get_similar_tournaments(id)
    signed_up_teams = get_tournament_teams_by_ranking(id)

    all_games = get_tournament_games(tournament.tournament_ptr)
    real_teams = get_padel_tournament_teams(tournament.tournament_ptr)
    fixtures = Fixtures(all_games)
    pool_games = fixtures.sorted_pools
    ko_games = fixtures.get_phased_finals({})

    return render(
        request,
        'tournament.html',
        {
            'tournament': tournament,
            'similar_tournaments': similar_tournaments,
            'signed_up_teams': signed_up_teams,
            'real_teams': real_teams,
            'pool_tables': pool_games,
            'ko_games': ko_games
        })


def clubs(request):
    clubs = get_clubs()
    return render(request, 'clubs.html', {'clubs': clubs})


def new_player(request):
    new_player_form = get_new_player_form()
    print(new_player_form, str(new_player_form), new_player_form.forms)
    if request.method == 'POST':
        # new_player_form = NewPlayerForm(request.POST)
        new_player_form = new_player_form(request.POST)
        if new_player_form.is_valid():
            new_player_form.save()
            return render(request, 'new_player_success.html')
        else:
            print(new_player_form.errors)
            return render(request, 'new_player.html', {'formset': new_player_form})
    else:
        return render(request, 'new_player.html', {'formset': new_player_form})


def ranking(request):
    return render(request, 'ranking.html')


def cardplayer(request):
    return render(request, 'card-player.html')
