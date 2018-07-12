import requests, os.path, sys
from settings import TELEGRAM_API, LOG_FILE

class Telegram:

    def __init__(self, token, observer):
        self.token = token

        if os.path.isfile(LOG_FILE):

            try:
                self.lastUpdate = int(open(LOG_FILE).read().strip())
            except:
                self.lastUpdate = -1

        else:
            self.lastUpdate = -1

        self.observer = observer

    def getUpdates(self):

        try:

            while True:

                r = requests.post(TELEGRAM_API + self.token + '/getUpdates', \
                        data={'offset' : self.lastUpdate})

                for item in r.json()['result']:

                    if 'update_id' in item and 'message' in item:

                        if self.lastUpdate < item['update_id']:

                            self.lastUpdate = item['update_id']

                            message = item['message']

                            self.observer.notify(message)

        except KeyboardInterrupt:

            with open(LOG_FILE, 'w') as f:
                f.write(str(self.lastUpdate))

            sys.exit()

    def sendMessage(self, chatId, message):

        r = requests.post(TELEGRAM_API + self.token + '/sendMessage', \
                data={'chat_id' : chatId, 'text' : message})

        if not r.json()['ok']:
            print('[LOG] Service lost. Problem during message sending.')
            raise Exception('Service lost.')

    def sendDocument(self, chatId, document):

        r = requests.post(TELEGRAM_API + self.token + '/sendDocument', \
                data={'chat_id' : chatId}, files={'document' : document})

        if not r.json()['ok']:
            print('[LOG] Service lost. Problem during document sending.')
            raise Exception('Service lost.')
