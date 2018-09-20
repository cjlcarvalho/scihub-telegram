from lxml import html
from .requestshelper import RequestsHelper
from .settings import URLS
from .exceptions import ScihubUnavailable, CaptchaError
from .log import Log

class ScihubScraper:

    """
    Class to scrap Sci-Hub website.
    """

    def __init__(self):

        self.scihubUrl = ''

    def connect(self):

        """
        This method will try to connect with Sci-Hub using the predefined URLs.

        Raises a ScihubUnavailable exception when it's unable to connect.
        """

        for url in URLS:

            Log.message('Trying to connect to ' + url + ' ...')

            try:

                r = RequestsHelper.get(url)

                if r['status_code'] != 200:

                    Log.message('Couldn\'t connect to ' + url)

                else:

                    Log.message('Connected to ' + url)

                    self.scihubUrl = url

            except:

                Log.message('Error during connection establishment with ' + url)

        if self.scihubUrl == '':

            raise ScihubUnavailable()

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

        url = self.scihubUrl + '/' + param

        r = RequestsHelper.get(url, stream=True)

        if r['headers']['Content-Type'] != 'application/pdf':

            if not r['content']:

                return None

            tree = html.fromstring(r['content'])

            if tree.xpath('//*[@id="captcha"]'):

                raise CaptchaError()

            link = tree.xpath('//*[@id=\'pdf\']/@src')

            if link:

                Log.message('Downloading file from ' + link[0])

                url = link[0] if link[0].startswith('http') else 'http:' + link[0]

            else:

                return None

        withoutBar = param.replace('/', '-')

        try:

            RequestsHelper.downloadDocument(url, withoutBar + '.pdf')

        except DownloadError:

            Log.message('Short file. It is possible that you got some error while downloading.')

        return open(withoutBar + '.pdf', 'rb')

