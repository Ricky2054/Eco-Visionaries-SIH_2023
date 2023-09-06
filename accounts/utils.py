from django.db import models

from django.core.validators import EmailValidator
from django.core.exceptions import ValidationError

from django.conf import settings


import uuid
import datetime
import pytz
import re


special_char_regex = re.compile('[@_!#$%^&*()<>?/\|}{~:]')

# Get the timezone object for the timezone specified in settings.py
tz = pytz.timezone(settings.TIME_ZONE)

# Get the current time in the timezone
current_time = datetime.datetime.now(tz)


#base/abstract model for other models
class BaseModel(models.Model):
    id = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        abstract = True


#func to check is a str contains special chars
def check_str_special(string):
    if special_char_regex.search(string):
        return True
    else:
        return False
    

#func to validate email
def validate_email(email):
    validator = EmailValidator()

    try:
        validator(email)
    except ValidationError:
        return False

    return True




