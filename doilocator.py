import requests
from settings import CROSSREF_TITLE_SEARCH

class DOILocator:

    def search(self, paper):

        r = requests.get(CROSSREF_TITLE_SEARCH,
                params={'query.title' : paper})

        if r.json()['status'] == 'ok':

            if 'message' in r.json():

                message = r.json()['message']

                if len(message['items']) > 0 and message['items'][0]['title'][0] == paper:
                    return message['items'][0]['DOI']

        return None
