from django.db import models
from anmeldung.validators import policy_read_validator


SERIE_GERMANY = (('GPS-100', 'GPS-100'), ('GPS-250', 'GPS-250'), ('GPS-500', 'GPS-500'), ('GPS-1000', 'GPS-1000'), ('GPS-1200', 'GPS-1200'))
CATEGORY_GERMANY = (('Herren A', 'Herren A'), ('Herren B', 'Herren B'), ('Damen', 'Damen'), ('Mixed', 'Mixed'), ('Senioren', 'Senioren'), ('Junioren', 'Junioren'))
PLAYER = (('A', 'A'), ('B', 'B'))


class Tournament(models.Model):
    creation_date = models.DateTimeField(auto_now_add=True, editable=False)
    serie = models.CharField(choices=SERIE_GERMANY, max_length=20, default='GPS-500')
    category = models.CharField(choices=CATEGORY_GERMANY, max_length=20, default='Herren A')
    city = models.CharField(max_length=20)
    date = models.DateField()

    def __str__(self):
        return " ".join([str(self.serie), str(self.city), str(self.category), str(self.date)])


class Player(models.Model):
    creation_date = models.DateTimeField(auto_now_add=True, editable=False)
    forename = models.CharField(max_length=24, verbose_name='First Name')
    surname = models.CharField(max_length=24, verbose_name='Last Name')
    email = models.EmailField(verbose_name='Email')
    phone = models.CharField(max_length=64, verbose_name='Phone')
    city = models.CharField(max_length=32, verbose_name='City')
    club = models.CharField(max_length=32, verbose_name='Club')
    birthplace = models.CharField(max_length=32, verbose_name='Birth place')
    birthdate = models.DateTimeField(verbose_name='Birthday')
    ranking_points = models.PositiveIntegerField(verbose_name='Ranking Points')

    def __str__(self):
        return " ".join([str(self.forename), str(self.surname)])


class Registration(models.Model):
    creation_date = models.DateTimeField(auto_now_add=True, editable=False)
    tournament = models.ForeignKey(Tournament, on_delete=models.DO_NOTHING)
    policy_read = models.BooleanField(default=True, validators=[policy_read_validator])
    player_a = models.ForeignKey(Player, related_name="player_a", on_delete=models.DO_NOTHING)
    player_b = models.ForeignKey(Player, related_name="player_b", on_delete=models.DO_NOTHING)

    def __str__(self):
        return " - ".join([str(self.player_a), str(self.player_b)])




