import argparse, sys
from scihubbot.scihubbot import ScihubBot
from scihubbot.log import Log

parser = argparse.ArgumentParser()
parser.add_argument("-l", "--log", help="select log type [stdout/file]")
parser.add_argument("-o", "--out", help="log output file location")
#parser.add_argument("-u", "--urls=", help="scihub custom urls file")

args = parser.parse_args()

if args.log is not None:
    if args.log == 'stdout' or args.log == 'file':
        Log.mode = args.log

        if Log.mode == 'file':
            if args.out is not None:
                Log.out = args.out
            else:
                print("Inform output file location...")
                sys.exit(0)

if __name__ == '__main__':

    ScihubBot().start()
