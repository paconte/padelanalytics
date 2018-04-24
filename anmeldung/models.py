from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from anmeldung.validators import policy_read_validator
from django_countries.fields import CountryField


SERIE_GERMANY = (('GPS-100', 'GPS-100'), ('GPS-250', 'GPS-250'), ('GPS-500', 'GPS-500'), ('GPS-1000', 'GPS-1000'),
                 ('GPS-1200', 'GPS-1200'), ('GPS-WOMEN', 'GPS-WOMEN'))
CATEGORY_GERMANY = (('Herren A', 'Herren A'), ('Herren B', 'Herren B'), ('Damen', 'Damen'), ('Mixed', 'Mixed'),
                    ('Senioren', 'Senioren'), ('Junioren', 'Junioren'))
PLAYER = (('A', 'A'), ('B', 'B'))


def player_directory_path(instance, filename):
    return 'player_media/' + normalize(
        '{0}-{1}-{2}-{3}'.format(instance.surname, instance.forename, instance.email, filename))


def club_directory_path(instance, filename):
    return 'club_media/' + normalize('{0}-{1}'.format(instance.name, filename))


class Club(models.Model):
    name = models.CharField(max_length=50)
    city = models.CharField(max_length=30)
    province = models.CharField(max_length=30)
    postcode = models.PositiveIntegerField(validators=[MinValueValidator(99), MaxValueValidator(1000000)])
    email = models.EmailField()
    phone = models.CharField(max_length=24)
    address = models.CharField(max_length=120, blank=True)
    indoor_courts = models.PositiveIntegerField()
    outdoor_courts = models.PositiveIntegerField()
    logo = models.ImageField(upload_to=club_directory_path, default='default.jpg')
    cover_photo = models.ImageField(upload_to=club_directory_path, default='pista.jpg')

    def __str__(self):
        return self.name


class Tournament(models.Model):
    creation_date = models.DateTimeField(auto_now_add=True, editable=False)
    club = models.ForeignKey(Club, on_delete=models.DO_NOTHING)
    serie = models.CharField(choices=SERIE_GERMANY, max_length=20, default='GPS-500')
    category = models.CharField(choices=CATEGORY_GERMANY, max_length=20, default='Herren A')
    city = models.CharField(max_length=20)
    date = models.DateField()
    signup = models.BooleanField(default=False)
    finished = models.BooleanField(default=False)

    @property
    def serie_url(self):
        if self.serie == 'GPS-100':
            return 'images/kategorien/gps100.jpg'
        elif self.serie == 'GPS-250':
            return 'images/kategorien/gps250.jpg'
        elif self.serie == 'GPS-500':
            return 'images/kategorien/gps500.jpg'
        elif self.serie == 'GPS-1000':
            return 'images/kategorien/gps1000.jpg'
        elif self.serie == 'GPS-1200':
            return 'images/kategorien/gps1200.jpg'
        elif self.serie == 'GPS-WOMEN':
            return 'images/kategorien/w-gps.jpg'
        else:
            raise TypeError("The serie is not supported.")

    def __str__(self):
        return "  /  ".join([str(self.date), str(self.serie), str(self.city), str(self.category)])

    def turnierliste_key(self):
        return " ".join([str(self.serie), str(self.city), str(self.date)])


class Player(models.Model):
    creation_date = models.DateTimeField(auto_now_add=True, editable=False)
    forename = models.CharField(max_length=24, verbose_name='First Name')
    surname = models.CharField(max_length=24, verbose_name='Last Name')
    surname2 = models.CharField(max_length=24, blank=True)
    email = models.EmailField(verbose_name='Email')
    phone = models.CharField(max_length=64, verbose_name='Phone')
    country = CountryField()
    city = models.CharField(max_length=32, verbose_name='City')
    club = models.ForeignKey(Club, on_delete=models.DO_NOTHING)
    birthplace = models.CharField(max_length=32, verbose_name='Birth place')
    birthdate = models.DateTimeField(verbose_name='Birthday')
    ranking_points = models.PositiveIntegerField(verbose_name='Ranking Points', default=0)
    photo = models.ImageField(upload_to=player_directory_path, default='Cool-Male-Avatars-06.png')
    policy_read = models.BooleanField(default=False, validators=[policy_read_validator])

    def __str__(self):
        return " ".join([str(self.forename), str(self.surname)])

    def abbr(self):
        return " ".join([self.forename[0] + '.', self.surname])


class Registration(models.Model):
    creation_date = models.DateTimeField(auto_now_add=True, editable=False)
    tournament = models.ForeignKey(Tournament, on_delete=models.DO_NOTHING)
    policy_read = models.BooleanField(default=False, validators=[policy_read_validator])
    player_a = models.ForeignKey(Player, related_name="player_a", on_delete=models.DO_NOTHING)
    player_b = models.ForeignKey(Player, related_name="player_b", on_delete=models.DO_NOTHING)

    def __str__(self):
        return " - ".join([str(self.player_a), str(self.player_b)])


def get_clubs():
    return Club.objects.all()


def get_tournament(id):
    return Tournament.objects.get(pk=id)


def get_similar_tournaments(t_id):
    result = dict()
    tournament = get_tournament(t_id)
    similars = Tournament.objects.filter(date=tournament.date, city=tournament.city, club=tournament.club)
    for t in similars:
        if t.id != tournament.id:
            result[t.category] = t.id
    return result


def get_tournaments():
    return Tournament.objects.order_by('date', 'city')


def get_tournament_teams_by_ranking(tournament_id):
    teams = Registration.objects.filter(tournament=tournament_id)
    result = list()
    for team in teams:
        ranking = team.player_a.ranking_points + team.player_b.ranking_points
        result.append((team, ranking))
    return sorted(result, key=lambda x: x[1], reverse=True)


def normalize(filename):
    return "".join([c for c in filename if c.isalpha() or c.isdigit() or c==' ']).rstrip()
