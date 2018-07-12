import requests, os.path, sys, json
from settings import TELEGRAM_API, LOG_FILE

class Telegram:

    def __init__(self, token, observer):
        self.token = token

        if os.path.isfile(LOG_FILE):

            try:

                with open(LOG_FILE) as file:
                    self.lastUpdate = json.loads(file.read())

            except:
                self.lastUpdate = {}

        else:
            self.lastUpdate = {}

        self.observer = observer

    def getUpdates(self):

        try:

            while True:

                r = requests.post(TELEGRAM_API + self.token + '/getUpdates', \
                        data={'offset' : self.lastUpdate})

                for item in r.json()['result']:

                    if 'update_id' in item and 'message' in item:

                        chatId = str(item['message']['chat']['id'])

                        if chatId not in self.lastUpdate:

                            self.lastUpdate[chatId] = -1

                        if self.lastUpdate[chatId] < item['update_id']:

                            self.lastUpdate[chatId] = item['update_id']

                            message = item['message']

                            self.observer.notify(message)

        except KeyboardInterrupt:

            with open(LOG_FILE, 'w') as f:
                f.write(json.dumps(self.lastUpdate))

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
