import datetime
import pytz
from django.core.exceptions import ValidationError

DATE_FORMAT = "%d/%m/%Y"
TIME_ZONE = pytz.timezone('Europe/Berlin')


def convert_date(value):
    return datetime.datetime.strptime(value, DATE_FORMAT)


def birthdate_validator(value):
    birthdate = convert_date(value)
    result = birthdate - timedelta(years=5)
    print(result)


def policy_read_validator(value):
    if not value:
        raise ValidationError('Policy not accepted. Obey!')

