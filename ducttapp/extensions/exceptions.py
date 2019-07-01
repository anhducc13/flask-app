from werkzeug.exceptions import HTTPException as BaseHTTPException

class HTTPException(BaseHTTPException):
    def __init__(self, code=400, message=None, errors=None):
        super().__init__(description=message, response=None)
        self.code = code
        self.errors = errors


class BadRequestException(HTTPException):
    def __init__(self, message='Bad Request', errors=None):
        super().__init__(code=400, message=message, errors=errors)


class NotFoundException(HTTPException):
    def __init__(self, message='Resource Not Found', errors=None):
        super().__init__(code=404, message=message, errors=errors)


class UnAuthorizedException(HTTPException):
    def __init__(self, message='UnAuthorized', errors=None):
        super().__init__(code=401, message=message, errors=errors)


class ForbiddenException(HTTPException):
    def __init__(self, message='Permission Denied', errors=None):
        super().__init__(code=403, message=message, errors=errors)
