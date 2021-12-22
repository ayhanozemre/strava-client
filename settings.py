import os

DOMAIN = 'https://www.strava.com'

API_ENDPOINT = os.path.join(DOMAIN, 'api/v3/')

SECRET_KEY = os.getenv("STRAVA_SECRET_KEY")

# bouds city : istanbul
DEFAULT_CITY_BOUNDS = '40.791286,28.383179,41.486291,29.690552'
