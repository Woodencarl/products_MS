from django.apps import AppConfig
from requests import post
from productsMS import constants

ACCESS_TOKEN_OFFERS_API = ''


class CatalogConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'catalog'

    def ready(self):
        print('Getting access token for offers API...')
        try:
            r = post(url=constants.API_OFFERS_URL + "/auth")
            if r.status_code.__str__() != '201':
                raise Exception("Problem connecting to Offers API.")
            else:
                global OFFER_API_HEADER
                global ACCESS_TOKEN_OFFERS_API
                ACCESS_TOKEN_OFFERS_API = r.json()['access_token']
                OFFER_API_HEADER = {'Bearer': ACCESS_TOKEN_OFFERS_API}
                print("Access_token gained.")
        except Exception:
            print(Exception)
