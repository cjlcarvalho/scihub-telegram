from .requestshelper import RequestsHelper
from .settings import CROSSREF_TITLE_SEARCH

class DOILocator:
    """
    Helper to search for the paper DOI.
    """

    def search(self, paper):

        """
        Method to search for the paper DOI.

        Parameters:
            paper (string): Paper's name.

        Returns:
            Object: Representing the DOI as string (if found) or None (if not found).
        """

        paper = paper.strip()

        r = RequestsHelper.get(CROSSREF_TITLE_SEARCH,
                params={'query.title' : paper})

        if r['json']['status'] == 'ok':

            if 'message' in r['json']:

                message = r['json']['message']

                for item in message['items']:

                    if item['title'][0] == paper:

                        return item['DOI']

        return None


