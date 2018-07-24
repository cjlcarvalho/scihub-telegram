import requests, os
from .exceptions import DownloadError
from .log import Log

class RequestsHelper:

    """
    Request API wrapper.
    """

    @classmethod
    def get(cls, url, params={}, stream=False):

        """
        Get method.

        Parameters:
            url (string): String representing the request URL
            params (dict): Request parameters
            stream (bool): Set streaming flag

        Returns:
            Response dictionary.
        """

        r = requests.get(url, params=params, stream=stream)

        response = { 'status_code' : r.status_code, \
                     'headers' : r.headers, \
                     'content' : r.content }

        try:
            response['json'] = r.json()
        except ValueError:
            pass

        return response

    @classmethod
    def post(cls, url, data={}, files={}):

        """
        Post method.

        Parameters:
            url (string): String representing the request URL
            params (dict): Request parameters
            stream (bool): Set streaming flag

        Returns:
            Response json
        """

        r = requests.post(url, data=data, files=files)

        return r.json()

    @classmethod
    def downloadDocument(cls, url, dest):

        """
        Method to download some document/file.
        Raises download error when it can't download the file.

        Parameters:
            url (string): File URL.
            dest (string): File output path.
        """

        r = requests.get(url, stream=True)

        with open(dest, 'wb') as f:

            for chunk in r.iter_content(chunk_size=1024):

                if chunk:

                    f.write(chunk)

        if os.path.getsize(dest) <= 1024:

            raise DownloadError();


