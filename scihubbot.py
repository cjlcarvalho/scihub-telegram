import requests, base64
from lxml import html
from settings import TELEGRAM_API, SCIHUB_URL

class ScihubBot:

    def __init__(self, token):
        self.token = token

        self.lastUpdate = -1

    def listen(self):

        while True:

            r = requests.post(TELEGRAM_API + self.token + '/getUpdates', \
                              data={'offset' : self.lastUpdate})

            for item in r.json()['result']:

                if 'update_id' in item and 'message' in item:

                    if self.lastUpdate < item['update_id']:

                        self.lastUpdate = item['update_id']

                        message = item['message']['text']

                        if message.strip() == '/help':

                            self.sendHelp(item['message']['chat']['id'])

                        elif message.startswith('/download '):

                            self.search(item['message']['chat']['id'], message[10:])

                        else:

                            self.sendMessage(item['message']['chat']['id'], 'Unknown command.')


    def sendHelp(self, chatId):

        message = 'List of commands:\n\n - download - Inform URL, PMID/DOI or search string to receive your file.'

        self.sendMessage(chatId, message)

    def sendMessage(self, chatId, message):

        r = requests.post(TELEGRAM_API + self.token + '/sendMessage', \
                data={'chat_id' : chatId, 'text' : message})

        if not r.json()['ok']:
            raise Exception('[LOG] Service lost. Problem during message sending.')

    def sendDocument(self, chatId, document):

        sendMessage(chatId, 'Here is your file (' + document.name + '):')

        r = requests.post(TELEGRAM_API + self.token + '/sendDocument', \
                data={'chat_id' : chatId, files={'document' : document})

        if not r.json()['ok']:
            raise Exception('[LOG] Service lost. Problem during document upload.')

    def search(self, chatId, param):

        print('[LOG] (' + str(chatId) + ') Searching for file: ' + param)

        r = requests.get(SCIHUB_URL + param, stream=True)

        withoutBar = param.replace('/', '-')

        if r.headers['Content-Type'] != 'application/pdf':

            tree = html.fromstring(r.content)

            link = tree.xpath('//div[@id=\'main_content\']//iframe[@id=\'pdf\']/@src')

            if link:

                reqDoc = requests.get(link[0] if link[0].startswith('http') else 'http:' + link[0], stream=True)

                self._downloadDocument(reqDoc, withoutBar)

                self.sendDocument(chatId, open(withoutBar + '.pdf', 'rb'))

            else:

                self.sendMessage(chatId, 'Couldn\'t find this file! :(')

        else:
            self._downloadDocument(r, withoutBar)

            self.sendDocument(chatId, open(withoutBar + '.pdf', 'rb'))

    def _downloadDocument(self, req, name):

        with open(name + '.pdf', 'wb') as f:
            for chunk in req.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)
