class Error(BaseException):
    pass


class FunctionSourceException(Error):
    def __init__(self):
        self.message = 'Functions %s call from multimple source (%s, %s)'


class UnknownFunctionException(Error):
    def __init__(self):
        self.message = 'Call unknown functions %s'
