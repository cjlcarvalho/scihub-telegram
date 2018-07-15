from .telegram import Telegram
from .scihubscraper import ScihubScraper
from .doilocator import DOILocator
from .settings import TOKEN

helpMessage = 'List of commands:\n\n' + \
              '- download - Inform URL, PMID/DOI or search string.\n' + \
              '- byname - Inform paper name to search.\n'

class ScihubBot:

    def __init__(self):

        self.telegram = Telegram(TOKEN, self)

        self.scihub = ScihubScraper()

        self.doilocator = DOILocator()

    def start(self):

        print('[LOG] Bot started...')

        self.telegram.getUpdates()

    def notify(self, message):

        text = message['text']

        chatId = message['chat']['id']

        msgId = message['message_id']

        if text.strip() == '/help' or text.strip() == '/start':

            print('[LOG] Help command asked.')
            self.telegram.sendMessage(chatId, msgId, helpMessage)

        elif text.startswith('/download '):

            print('[LOG] Searching for ' + text[10:])
            doc = self.scihub.searchFile(str(text[10:]))

            if doc is None:
                self.telegram.sendMessage(chatId, msgId, 'Couldn\'t find this file! :(')
            else:
                self.telegram.sendDocument(chatId, msgId, doc)

        elif text.startswith('/byname '):

            print('[LOG] Searching by name: ' + text[8:])
            doi = self.doilocator.search(text[8:])

            if doi is None:
                self.telegram.sendMessage(chatId, msgId, 'Couldn\'t find file DOI. :(')
            else:
                doc = self.scihub.searchFile(doi)

                if doc is None:
                    self.telegram.sendMessage(chatId, msgId, 'Couldn\'t find this file by its DOI! :(')
                else:
                    self.telegram.sendDocument(chatId, msgId, doc)

        else:
            print('[LOG] Unknown command: ' + text)
            self.telegram.sendMessage(chatId, msgId, 'Unknown command! Send /help to know how to download your papers.')
