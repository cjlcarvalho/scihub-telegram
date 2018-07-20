import requests, os
from .log import Log

class RequestsHelper:

    @classmethod
    def get(cls, url, params={}, stream=False):

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

        r = requests.post(url, data=data, files=files)

        return r.json()

    @classmethod
    def downloadDocument(cls, url, dest):

        r = requests.get(url, stream=True)

        with open(dest, 'wb') as f:

            for chunk in r.iter_content(chunk_size=1024):

                if chunk:

                    f.write(chunk)

        if os.path.getsize(dest) <= 1024:

            Log.message('Short file. It is possible that you got some error while downloading.')


