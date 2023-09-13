from django.db import models

from django.core.validators import EmailValidator
from django.core.exceptions import ValidationError

from django.conf import settings

from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.core.cache import cache


import uuid
import datetime
import pytz
import re


CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)

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


#func to convert unix time to Asia/kolkata time
def unix_time_to_kolkata_datetime(unix_timestamp):
    # Define the Asia/Kolkata time zone
    kolkata_tz = pytz.timezone('Asia/Kolkata')

    # Convert Unix timestamp to a datetime object in UTC
    utc_datetime = datetime.datetime.utcfromtimestamp(unix_timestamp)

    # Set the UTC time zone to the datetime object
    utc_datetime = utc_datetime.replace(tzinfo=pytz.utc)

    # Convert UTC datetime to Kolkata time zone
    kolkata_datetime = utc_datetime.astimezone(kolkata_tz).strftime('%Y-%m-%d %H:%M:%S')

    return kolkata_datetime


#func to convert to unix time
def datetime_to_unix_time(dt):
    #i/p: datetime obj - datetime(2023, 9, 6, 12, 0, 0)

    # Convert a datetime object to a Unix timestamp
    unix_timestamp = int(dt.timestamp())
    return unix_timestamp


#func to extract date from date-time str
def extract_date(datetime_string):
    # Parse the datetime string
    datetime_obj = datetime.datetime.strptime(datetime_string, '%Y-%m-%d %H:%M:%S')

    # Extract only the date
    date_only = datetime_obj.date()

    # Convert the date to a string if needed
    date_string = date_only.strftime('%Y-%m-%d')

    return date_string


#func to format date in given format
def format_date(date, format='%d-%m-%Y'):

    try:
        # Attempt to parse the date string
        # If parsing is successful, it contains both date and time
        datetime_obj = datetime.datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
    except ValueError:
        try:
            # Attempt to parse the date string as date only
            # If parsing is successful, it contains date only
            datetime_obj = datetime.datetime.strptime(date, '%Y-%m-%d')
            
        except ValueError:
            # If both parsing attempts fail, the format is invalid
            return date


    return datetime_obj.strftime(format)




#func to check weather key was cached
def cache_get(key):
    '''
    this will return the cached data if its present in cache, None otherwise
    '''

    return cache.get(key)


#func to set cache
def cache_set(key, value, ttl_sec=CACHE_TTL):
    '''
    this will cache the value with key
    '''
    
    cache.set(key, value, timeout=ttl_sec)


#func to delete cache
def cache_delete(key):
    '''
    this will delete cache data with key
    '''
    
    cache.delete(key)


#func to delete cache with given prefix
def cache_delete_many(key_with_prefix):
    '''
    this will delete cache data with key prefix key_with_prefix
    '''
    
    cache.delete_many(keys=key_with_prefix)



#func to get or create cache data
def cache_get_or_create(key, value="", ttl_sec=CACHE_TTL):
    '''
    this will return the cache data with key if present else it will cache the data with key and value. Return type: cached data, Bool. Bool indicating if data is cached now
    '''
    
    cached_data = cache_get(key)
    #check if cached data exists
    if cached_data:
        return cached_data, False
    
    #set the cache 
    cache_set(key, value, ttl_sec)

    #get and return the cache
    return cache_get(key), True



