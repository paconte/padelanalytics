import logging

from django.shortcuts import render
from django.shortcuts import redirect

from anmeldung.forms import RegistrationForm
from anmeldung.forms import get_new_player_form

from anmeldung.models import get_padel_tournament
from anmeldung.models import get_padel_tournaments
from anmeldung.models import get_tournament_teams_by_ranking
from anmeldung.models import get_clubs
from anmeldung.models import get_similar_tournaments
from anmeldung.models import get_all_registrations

from tournaments.models import Person
from tournaments.models import get_tournament_games
from tournaments.models import get_padel_tournament_teams

from tournaments.service import Fixtures

# Get an instance of a logger
logger = logging.getLogger(__name__)


def index(request):
    return render(request, 'landing.html')


def tournament_signup(request, id=None):
    if request.method == 'POST':
        registration_form = RegistrationForm(request.POST)
        if registration_form.is_valid():
            player_a = registration_form.cleaned_data['player_a']
            player_b = registration_form.cleaned_data['player_b']

            # check player is not twice in the team
            if player_a.id == player_b.id:
                registration_form.add_error('player_b', 'A team must have two different players.')
                return render(request, 'tournament_signup.html', {'form': registration_form})

            # check no player is twice in a tournament
            player_signed_up = None
            registrations = get_all_registrations(registration_form.cleaned_data['tournament'])
            for reg in registrations:
                if player_a.id == reg.player_a.id or player_a.id == reg.player_b.id:
                    registration_form.add_error('player_a', 'Player already signed up in the tournament.')
                    player_signed_up = True
                    break
                elif player_b.id == reg.player_a.id or player_b.id == reg.player_b.id:
                    registration_form.add_error('player_b', 'Player already signed up in the tournament.')
                    player_signed_up = True
                    break
            if player_signed_up:
                return render(request, 'tournament_signup.html', {'form': registration_form})

            # all checks are good
            registration_form.save()
            return redirect('tournament', registration_form.cleaned_data['tournament'].id)
        # form is invalid
        else:
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
    if request.method == 'POST':
        new_player_form = new_player_form(request.POST)
        if new_player_form.is_valid():
            # get or create the person
            person, created = Person.objects.get_or_create(
                first_name=new_player_form.cleaned_data[0]['first_name'],
                last_name=new_player_form.cleaned_data[0]['last_name'],
                born=new_player_form.cleaned_data[0]['born'],
                nationality=None,
                gender=new_player_form.cleaned_data[0]['gender']
            )
            # logging
            if created:
                logger.info("While creating a new PadelPerson a new Person has been created: %s", person)
            # saving the new PadelPerson
            padel_person = new_player_form.save(commit=False)[0]
            padel_person.person_ptr = person
            padel_person.save()
            return render(request, 'new_player_success.html')
        else:
            return render(request, 'new_player.html', {'formset': new_player_form})
    else:
        return render(request, 'new_player.html', {'formset': new_player_form})


def ranking(request):
    return render(request, 'ranking.html')


def cardplayer(request):
    return render(request, 'card-player.html')
