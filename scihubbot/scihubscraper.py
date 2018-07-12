import requests
from lxml import html
from .settings import SCIHUB_URL

class ScihubScraper:

    def searchFile(self, param):

        r = requests.get(SCIHUB_URL + param, stream=True)

        if r.headers['Content-Type'] != 'application/pdf':

            if not r.content:
                return None

            tree = html.fromstring(r.content)

            link = tree.xpath('//div[@id=\'main_content\']//iframe[@id=\'pdf\']/@src')

            if link:

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
