import os.path, json, threading
from .requestshelper import RequestsHelper
from .settings import TELEGRAM_API, USERS_LAST_UPDATE
from .log import Log

class Telegram:

    """
    Class to communicate with Telegram API.
    """

    def __init__(self, token, observer):

        """
        Constructor

        Parameters:
            token (string): Telegram API token
            observer (string): Observer object that will process the API response.
        """

        self.token = token

        if os.path.isfile(USERS_LAST_UPDATE):

            try:

                with open(USERS_LAST_UPDATE) as file:
                    self.lastUpdate = json.loads(file.read())

            except:
                Log.message('LAST UPDATE IS EMPTY!')
                self.lastUpdate = {}

        else:
            self.lastUpdate = {}

        self.observer = observer

    def getUpdates(self):

        """
        Represents /getUpdates API method.
        """

        while True:

            r = RequestsHelper.post(TELEGRAM_API + self.token + '/getUpdates', \
                    data={'offset' : self.lastUpdate})

            for item in r['result']:

                if 'update_id' in item and 'message' in item:

                    chatId = str(item['message']['chat']['id'])

                    if chatId not in self.lastUpdate:

                        self.lastUpdate[chatId] = -1

                    if self.lastUpdate[chatId] < item['update_id']:

                        self.lastUpdate[chatId] = item['update_id']

                        with open(USERS_LAST_UPDATE, 'w') as f:
                            f.write(json.dumps(self.lastUpdate))

                        message = item['message']

                        t = threading.Thread(target=self.observer.notify, args=(message,))

                        t.start()

    def sendMessage(self, chatId, origin, message):

        """
        Represents /sendMessage API method.

        Parameters:
            chatId (int): Chat ID number.
            origin (string): The message ID which sent the request.
            message (string): Message content to send.
        """

        r = RequestsHelper.post(TELEGRAM_API + self.token + '/sendMessage', \
                data={'chat_id' : chatId, 'reply_to_message_id': origin, 'text' : message})

        if not r['ok']:
            Log.message('Service lost. Problem during message sending.')
            raise Exception('Service lost.') # TODO: Use custom exception.

    def sendDocument(self, chatId, origin, document):

        """
        Represents /sendDocument API method.

        Parameters:
            chatId (int): Chat ID number.
            origin (string): The message ID which sent the request.
            document (file): File content to send.
        """

        r = RequestsHelper.post(TELEGRAM_API + self.token + '/sendDocument', \
                data={'chat_id' : chatId, 'reply_to_message_id': origin}, files={'document' : document})

        if not r['ok']:
            Log.message('Service lost. Problem during document sending.')
            raise Exception('Service lost.')


