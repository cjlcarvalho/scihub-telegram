import requests
from lxml import html
from .settings import SCIHUB_URLS_FILE
from .exceptions import ScihubUnavailable

class ScihubScraper:

    def __init__(self):

        self.scihubUrl = ''

    def connect(self):

        with open(SCIHUB_URLS_FILE, 'r') as f:

            urls = map(lambda x: x[:-1] , f.readlines())

            for url in urls:

                print('[LOG] Trying to connect to ' + url + ' ...')

                try:

                    r = requests.get(url)

                    if r.status_code != 200:

                        print('[LOG] Couldn\'t connect to ' + url)

                    else:

                        print('[LOG] Connected to ' + url)

                        self.scihubUrl = url

                        break
                except:

                    print('[LOG] Error during connection establishment with ' + url)

        if self.scihubUrl == '':

            raise ScihubUnavailable('Couldn\'t connect with Sci-Hub using urls contained in ' + SCIHUB_URLS_FILE + ' file.')

    def searchFile(self, param):

        if self.scihubUrl == '':

            raise ScihubUnavailable('Couldn\'t connect to Sci-Hub.')

        r = requests.get(self.scihubUrl + '/' + param, stream=True)

        if r.headers['Content-Type'] != 'application/pdf':

            if not r.content:

                return None

            tree = html.fromstring(r.content)

            link = tree.xpath('//*[@id=\'pdf\']/@src')

            if link:

                print('[LOG] Trying to download file from ' + link[0])

                r = requests.get(link[0] if link[0].startswith('http') else 'http:' + link[0], stream=True)

            else:

                return None

        withoutBar = param.replace('/', '-')

        self._downloadDocument(r, withoutBar)

        return open(withoutBar + '.pdf', 'rb')

    def _downloadDocument(self, req, name):

        with open(name + '.pdf', 'wb') as f:
            for chunk in req.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)
