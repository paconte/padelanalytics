from django.db import models
from anmeldung.validators import birthdate_validator, policy_read_validator


SERIE_GERMANY = (('GPS-100', 'GPS-100'), ('GPS-250', 'GPS-250'), ('GPS-500', 'GPS-500'), ('GPS-1000', 'GPS-1000'), ('GPS-1200', 'GPS-1200'))
CATEGORY_GERMANY = (('Herren A', 'Herren A'), ('Herren B', 'Herren B'), ('Damen', 'Damen'), ('Mixed', 'Mixed'), ('Senioren', 'Senioren'), ('Junioren', 'Junioren'))
PLAYER = (('A', 'A'), ('B', 'B'))


class Tournament(models.Model):
    category = models.CharField(choices=SERIE_GERMANY, max_length=20)
    city = models.CharField(max_length=20)
    date = models.DateTimeField()

    def __str__(self):
        return " ".join([str(self.date) + str(self.category) + str(self.city)])


class Registration(models.Model):
    # tournament_name = models.ForeignKey(Tournament)
    # category = models.CharField(choices=CATEGORY_GERMANY, max_length=32)
    # player = models.CharField(choices=PLAYER, max_length=32)
    forename = models.CharField(max_length=24, verbose_name='First Name')
    surname = models.CharField(max_length=24, verbose_name='Last Name')
    email = models.EmailField(verbose_name='Email')
    phone = models.CharField(max_length=64, verbose_name='Phone')
    city = models.CharField(max_length=32, verbose_name='City')
    club = models.CharField(max_length=32, verbose_name='Club')
    birthplace = models.CharField(max_length=32, verbose_name='Birthday')
    birthdate = models.DateTimeField()
    ranking_points = models.PositiveIntegerField(verbose_name='Ranking Points')
    policy_read = models.BooleanField(default=True, validators=[policy_read_validator])



