from scihubbot import ScihubBot
from settings import TOKEN

if __name__ == '__main__':

    bot = ScihubBot(TOKEN)

    bot.listen()
