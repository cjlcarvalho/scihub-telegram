
class Log:

    mode = 'stdout'
    out = ''

    @classmethod
    def message(cls, msg):

        m = '[LOG] ' + msg

        if cls.mode == 'stdout':

            print(m)

        elif cls.mode == 'file':

            with open(cls.out, 'a') as f:

                f.write(m + '\n')
