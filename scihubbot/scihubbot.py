import sys
from .telegram import Telegram
from .scihubscraper import ScihubScraper
from .doilocator import DOILocator
from .exceptions import ScihubUnavailable, CaptchaError
from .settings import TOKEN
from .log import Log

HELPMESSAGE = 'List of commands:\n\n' + \
              '- download - Inform URL, PMID/DOI or search string.\n' + \
              '- byname - Inform paper name to search.\n'

class ScihubBot:
    """
    Sci-Hub bot class.
    """

    def __init__(self):

        self.telegram = Telegram(TOKEN, self)

        self.scihub = ScihubScraper()

        self.doilocator = DOILocator()

    def start(self):

        """
        Method to start your bot.
        """

        Log.message('Bot started...')

        try:

            self.scihub.connect()

            self.telegram.getUpdates()

        except KeyboardInterrupt:

            Log.message('Bye.')

            sys.exit()

        except ScihubUnavailable:

            Log.message('Sci-Hub Website unavailable.')

            sys.exit()

        except Exception as e:

            Log.message('Error occurred. Message: ' + e.message)

    def notify(self, message):

        """
        Notify method.
        It should be called by the bot's subject, informing the message.

        Parameters:
            message (dict): Dictionary containing the message information.
        """

        text = message['text']

        chatId = message['chat']['id']

        msgId = message['message_id']

        if text.strip() == '/help' or text.strip() == '/start':

            Log.message('Help command asked.')

            self.telegram.sendMessage(chatId, msgId, HELPMESSAGE)

        elif text.startswith('/download '):

            Log.message('Searching for ' + text[10:])

            try:

                doc = self.scihub.searchFile(str(text[10:]))

                if doc is None:

                    self.telegram.sendMessage(chatId, msgId, 'Couldn\'t find this file! :(')

                else:

                    self.telegram.sendDocument(chatId, msgId, doc)

            except CaptchaError:

                Log.message('Captcha was found.')

        elif text.startswith('/byname '):

            Log.message('Searching by name: ' + text[8:])

            doi = self.doilocator.search(text[8:])

            if doi is None:

                self.telegram.sendMessage(chatId, msgId, 'Couldn\'t find file DOI. :(')

            else:

                try:

                    doc = self.scihub.searchFile(doi)

                    if doc is None:

                        self.telegram.sendMessage(chatId, msgId, 'Couldn\'t find this file by its DOI! :(')

                    else:

                        self.telegram.sendDocument(chatId, msgId, doc)

                except CaptchaError:

                    Log.message('Captcha was found.')

        else:

            Log.message('Unknown command: ' + text)

            self.telegram.sendMessage(chatId, msgId, 'Unknown command! Send /help to know how to download your papers.')


