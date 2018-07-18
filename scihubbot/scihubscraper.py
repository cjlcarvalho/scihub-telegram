import requests
from lxml import html
from .settings import SCIHUB_URLS_FILE
from .exceptions import ScihubUnavailable
from .log import Log

class ScihubScraper:

    """
        Class to scrap Sci-Hub website.
    """

    def __init__(self):

        self.scihubUrl = ''

    def connect(self):

        """
            This method will try to connect with Sci-Hub using the predefined URLs available at SCIHUB_URLS_FILE.

            Raises a ScihubUnavailable exception when it's unable to connect.
        """

        with open(SCIHUB_URLS_FILE, 'r') as f:

            urls = map(lambda x: x[:-1] , f.readlines())

            for url in urls:

                Log.message('Trying to connect to ' + url + ' ...')

                try:

                    r = requests.get(url)

                    if r.status_code != 200:

                        Log.message('Couldn\'t connect to ' + url)

                    else:

                        Log.message('Connected to ' + url)

                        self.scihubUrl = url

                        break
                except:

                    Log.message('Error during connection establishment with ' + url)

        if self.scihubUrl == '':

            raise ScihubUnavailable('Couldn\'t connect with Sci-Hub using urls contained in ' + SCIHUB_URLS_FILE + ' file.')

    def searchFile(self, param):

        """
            Search file on Sci-Hub according to the parameter (i.e. DOI, URL or search string).

            Parameters:
            param (string): Sci-Hub search parameter.

            Returns:
            file: PDF containing the text of the desired paper. It will return None in the cases where it's not found.

        """

        if self.scihubUrl == '':

            raise ScihubUnavailable('Couldn\'t connect to Sci-Hub.')

        r = requests.get(self.scihubUrl + '/' + param, stream=True)

        if r.headers['Content-Type'] != 'application/pdf':

            if not r.content:

                return None

            tree = html.fromstring(r.content)

            link = tree.xpath('//*[@id=\'pdf\']/@src')

            if link:

                Log.message('Trying to download file from ' + link[0])

                r = requests.get(link[0] if link[0].startswith('http') else 'http:' + link[0], stream=True)

            else:

                return None

        withoutBar = param.replace('/', '-')

        self._downloadDocument(r, withoutBar)

        return open(withoutBar + '.pdf', 'rb')

    def _downloadDocument(self, req, name):

        """
            Method to download a document according to its name and request.

            Parameters:
            req (request): Request made.
            name (string): The name of the file.

        """


        with open(name + '.pdf', 'wb') as f:
            for chunk in req.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)


