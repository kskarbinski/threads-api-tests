http_exceptions = dict()


def add_exception(cls):
    def wrapper():
        http_exceptions[cls.status_code] = cls
    wrapper()
    return cls


def from_status_code(status_code, msg):
    exception_cls = http_exceptions.get(status_code) or HttpException
    return exception_cls(msg=msg)


class HttpException(Exception):
    status_code = "Unknown"

    def __init__(self, msg=""):
        self.msg = msg

    def __str__(self):
        return "{status_code} {msg}".format(status_code=self.status_code, msg=self.msg)


@add_exception
class BadRequest(HttpException):
    status_code = 400


@add_exception
class Unauthorized(HttpException):
    status_code = 401


@add_exception
class Forbidden(HttpException):
    status_code = 403


@add_exception
class NotFound(HttpException):
    status_code = 404


@add_exception
class Conflict(HttpException):
    status_code = 409


@add_exception
class UnprocessableEntity(HttpException):
    status_code = 422


@add_exception
class InternalServerError(HttpException):
    status_code = 500


del add_exception
