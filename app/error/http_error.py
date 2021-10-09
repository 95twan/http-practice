class HttpError(Exception):
    def __init__(self, msg, status_code, status_msg):
        super().__init__(msg)
        self.status_code = status_code
        self.status_msg = status_msg
