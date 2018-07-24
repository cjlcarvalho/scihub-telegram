
class Log:

    """
    Log class. It contains the log mode (stdout/file) and the output file (if it is by file mode).
    """

    mode = 'stdout'
    out = ''

    @classmethod
    def message(cls, msg):

        """
        Static method to Log a message.

        Parameters:
            msg (string): Message content.
        """

        m = '[LOG] ' + msg

        if cls.mode == 'stdout':

            print(m)

        elif cls.mode == 'file':

            with open(cls.out, 'a') as f:

                f.write(m + '\n')

