from typing import Union, List, Dict
from .plisio_enums import CryptoCurrency, FiatCurrency, OperationStatus, OperationType, PlanName

from .plisio_exceptions import (
    PlisioError,
    RequestNotProcessed,
    RequestAlreadyProcessed,
    UnknownPlisioAPIError,
    BadRequestError,
    UnauthorizedError,
    ForbiddenError,
    NotFoundError,
    MethodNotAllowedError,
    NotAcceptableError,
    UnsupportedMediaTypeError,
    UnprocessableEntityTypeError,
    RateLimitReachedError,
    InternalServerError,
    ServiceUnavailableError,
)

from .plisio_models import (
    PlisioModel,
    Balance,
    Currency,
    Invoice,
    Commission,
    Withdraw,
    Fee,
    Plan,
    FeePlan,
    Operation,
    Operations,
)

from .plisio_client import PlisioClient, PlisioAioClient

RType = Union[List['RType'], Dict[str, 'RType']]

ModelType = Union[
    'plisio.PlisioModel',
    'plisio.Balance',
    'plisio.Currency',
    'plisio.Invoice',
    'plisio.Commission',
    'plisio.Withdraw',
    'plisio.Fee',
    'plisio.Plan',
    'plisio.FeePlan',
    'plisio.Operation',
    'plisio.Operations',
]
