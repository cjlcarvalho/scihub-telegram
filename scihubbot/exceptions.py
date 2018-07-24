
class ScihubUnavailable(Exception):

    """
    An Exception to deal with Sci-Hub website unavailability.
    """

    pass

class CaptchaError(Exception):

    """
    An Exception to be thrown when captcha was found.
    """

    pass

class DownloadError(Exception):

    """
    An Exception to be thrown when download errors happen.
    """

    pass

