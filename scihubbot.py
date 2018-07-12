from telegram import Telegram
from scihubscraper import ScihubScraper
from doilocator import DOILocator
from settings import TOKEN

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

        if text.strip() == '/help':

            print('[LOG] Help command asked.')
            self.telegram.sendMessage(chatId, helpMessage)

        elif text.startswith('/download '):

            print('[LOG] Searching for ' + text[10:])
            doc = self.scihub.searchFile(text[10:])

            if doc is None:
                self.telegram.sendMessage(chatId, 'Couldn\'t find this file! :(')
            else:
                self.telegram.sendDocument(chatId , doc)

        elif text.startswith('/byname '):

            print('[LOG] Searching by name: ' + text[8:])
            doi = self.doilocator.search(text[8:])

            if doi is None:
                self.telegram.sendMessage(chatId, 'Couldn\'t find file DOI. :(')
            else:
                doc = self.scihub.searchFile(doi)

                if doc is None:
                    self.telegram.sendMessage(chatId, 'Couldn\'t find this file by its DOI! :(')
                else:
                    self.telegram.sendDocument(chatId, doc)

        else:
            print('[LOG] Unknown command: ' + text)
            self.telegram.sendMessage(chatId, 'Unknown command!')
