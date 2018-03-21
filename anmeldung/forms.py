from django import forms
from django.core.exceptions import ValidationError
from django.db import DataError
from anmeldung.models import CATEGORY_GERMANY, Club, Tournament, Player, Registration
from anmeldung.validators import policy_read_validator, DATE_FORMAT, convert_date


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


class FullRegistrationForm(forms.Form):
    tournament_name = forms.ModelChoiceField(queryset=Tournament.objects.filter(signup=True))

    policy_read = forms.BooleanField(initial=True, validators=[policy_read_validator])
    # playerA = forms.ModelChoiceField(queryset=Player.objects.all())
    # playerB = forms.ModelChoiceField(queryset=Player.objects.all())

    # first player
    forename_a = forms.CharField(
        max_length=24,
        widget=forms.TextInput(attrs={'placeholder': 'Vorname'})
    )
    surname_a = forms.CharField(
        max_length=24,
        widget=forms.TextInput(attrs={'placeholder': 'Familienname'})
    )
    email_a = forms.EmailField(
        widget=forms.EmailInput(attrs={'placeholder': 'Mail-Adresse'})
    )
    phone_a = forms.CharField(
        max_length=64,
        widget=forms.TextInput(attrs={'placeholder': 'Telefonnummer'})
    )
    city_a = forms.CharField(
        max_length=32,
        widget=forms.TextInput(attrs={'placeholder': 'Wohnort'})
    )
    club_a = forms.ModelChoiceField(queryset=Club.objects.all())
    birthplace_a = forms.CharField(
        max_length=32,
        widget=forms.TextInput(attrs={'placeholder': 'Geburtsort'})
    )
    birthdate_a = forms.DateField(
        input_formats=[DATE_FORMAT],
        widget=forms.TextInput(attrs={'placeholder': 'TT/MM/JJJJ'})
    )
    ranking_points_a = forms.IntegerField(
        widget=forms.TextInput(attrs={'placeholder': 'Trag deine Punkte ein'})
    )
    # second player
    forename_b = forms.CharField(
        max_length=24,
        widget=forms.TextInput(attrs={'placeholder': 'Vorname'})
    )
    surname_b = forms.CharField(
        max_length=24,
        widget=forms.TextInput(attrs={'placeholder': 'Familienname'})
    )
    email_b = forms.EmailField(
        widget=forms.EmailInput(attrs={'placeholder': 'Mail-Adresse'})
    )
    phone_b = forms.CharField(
        max_length=64,
        widget=forms.TextInput(attrs={'placeholder': 'Telefonnummer'})
    )
    city_b = forms.CharField(
        max_length=32,
        widget=forms.TextInput(attrs={'placeholder': 'Wohnort'})
    )
    club_b = forms.ModelChoiceField(queryset=Club.objects.all())
    birthplace_b = forms.CharField(
        max_length=32,
        widget=forms.TextInput(attrs={'placeholder': 'Geburtsort'})
    )
    birthdate_b = forms.DateField(
        input_formats=[DATE_FORMAT],
        widget=forms.TextInput(attrs={'placeholder': 'TT/MM/JJJJ'})
    )
    ranking_points_b = forms.IntegerField(
        widget=forms.TextInput(attrs={'placeholder': 'Trag deine Punkte ein'})
    )

    def save(self):
        if self.is_valid():
            print(self.data)
            player_a = Player.objects.create(
                forename=self.data['forename_a'],
                surname=self.data['surname_a'],
                email=self.data['email_a'],
                city=self.data['city_a'],
                club=self._get_club_a(),
                birthplace=self.data['birthplace_a'],
                birthdate=convert_date(self.data['birthdate_a']),
                ranking_points=self._clean_ranking_points_a()
            )
            try:
                player_b = Player.objects.create(
                    forename=self.data['forename_b'],
                    surname=self.data['surname_b'],
                    email=self.data['email_b'],
                    city=self.data['city_b'],
                    club=self._get_club_b(),
                    birthplace=self.data['birthplace_b'],
                    birthdate=convert_date(self.data['birthdate_b']),
                    ranking_points=self._clean_ranking_points_b()
                )
            except Exception:
                player_a.delete()
                raise DataError("Player Model has data errors.")

            try:
                return Registration.objects.create(
                    tournament=self._get_tournament(),
                    policy_read=self._get_terms(),
                    player_a=player_a,
                    player_b=player_b
                )

            except Exception:
                player_a.delete()
                player_b.delete()
                raise DataError("Registration Model has data errors.")
        else:
            raise ValidationError("FullRegistrationForm is not valid.")

    def _clean_ranking_points_a(self):
        if self.is_valid():
            result = int(self.data['ranking_points_a'])
            if result < 0:
                result = 0
        else:
            raise ValidationError("FullRegistrationForm is not valid.")
        return result

    def _clean_ranking_points_b(self):
        if self.is_valid():
            result = int(self.data['ranking_points_b'])
            if result < 0:
                result = 0
        else:
            raise ValidationError("FullRegistrationForm is not valid.")
        return result

    def _get_tournament(self):
        if self.is_valid():
            return Tournament.objects.get(pk=self.data['tournament_name'])
        raise ValidationError("FullRegistrationForm is not valid.")

    def _get_terms(self):
        if self.is_valid():
            result = False
            if self.data['policy_read'] == 'on':
                result = True
            return result
        raise ValidationError("FullRegistrationForm is not valid.")

    def _get_club_a(self):
        if self.is_valid():
            return Club.objects.get(pk=self.data['club_a'])
        raise ValidationError("FullRegistrationForm is not valid.")

    def _get_club_b(self):
        if self.is_valid():
            return Club.objects.get(pk=self.data['club_b'])
        raise ValidationError("FullRegistrationForm is not valid.")
