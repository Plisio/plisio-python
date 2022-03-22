from typing import Optional


class PlisioError(Exception):
    reason = 'An error has occurred when contacting to Plisio API'

    def __init__(self, message: Optional[str] = None):
        if message is None:
            message = self.reason
        super().__init__(message)


class RequestNotProcessed(PlisioError):
    reason = 'The request to Plisio API has not yet been processed'


class RequestAlreadyProcessed(PlisioError):
    reason = 'The request to Plisio API has already been processed'


class UnknownPlisioAPIError(PlisioError):
    pass


class BadRequestError(PlisioError):
    """
    400 Bad Request.
    INVALID_REQUEST.
    Request is not well-formed, syntactically incorrect, or violates schema.
    """
    reason = 'Request is not well-formed, syntactically incorrect, or violates schema.'


class UnauthorizedError(PlisioError):
    """
    401 Unauthorized.
    AUTHENTICATION_FAILURE.
    Authentication failed due to invalid authentication credentials.
    """
    reason = 'Authentication failed due to invalid authentication credentials.'


class ForbiddenError(PlisioError):
    """
    403 Forbidden.
    NOT_AUTHORIZED.
    Authorization failed due to insufficient permissions.
    """
    reason = 'Authorization failed due to insufficient permissions.'


class NotFoundError(PlisioError):
    """
    404 Not Found.
    RESOURCE_NOT_FOUND.
    The specified resource does not exist.
    """
    reason = 'The specified resource does not exist.'


class MethodNotAllowedError(PlisioError):
    """
    405 Method Not Allowed.
    METHOD_NOT_SUPPORTED.
    The server does not implement the requested HTTP method.
    """
    reason = 'The server does not implement the requested HTTP method.'


class NotAcceptableError(PlisioError):
    """
    406 Not Acceptable.
    MEDIA_TYPE_NOT_ACCEPTABLE.
    The server does not implement the media type that would be acceptable to the client.
    """
    reason = 'The server does not implement the media type that would be ' \
             'acceptable to the client.'


class UnsupportedMediaTypeError(PlisioError):
    """
    415 Unsupported Media Type.
    UNSUPPORTED_MEDIA_TYPE.
    The server does not support the request payload’s media type.
    """
    reason = 'The server does not support the request payload’s media type.'


class UnprocessableEntityTypeError(PlisioError):
    """
    422 Unprocessable Entity.
    UNPROCESSABLE_ENTITY.
    The API cannot complete the requested action, or the request action is
    semantically incorrect or fails business validation.
    """
    reason = 'The API cannot complete the requested action, or the request ' \
             'action is semantically incorrect or fails business validation.'


class RateLimitReachedError(PlisioError):
    """
    429 Rate Limit Reached.
    RATE_LIMIT_REACHED.
    Too many requests. Blocked due to rate limiting.
    """
    reason = 'Too many requests. Blocked due to rate limiting.'


class InternalServerError(PlisioError):
    """
    500 Internal Server Error.
    INTERNAL_SERVER_ERROR.
    An internal server error has occurred.
    """
    reason = 'An internal server error has occurred.'


class ServiceUnavailableError(PlisioError):
    """
    503 Service Unavailable.
    SERVICE_UNAVAILABLE.
    Service Unavailable.
    """
    reason = 'Service Unavailable.'
