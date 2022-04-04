from typing import Type, Dict, Optional, Union, List, Any

import aiohttp
import requests

import plisio


class _PlisioUrl:
    balance = 'balances'
    currencies = 'currencies'
    invoice = 'invoices/new'
    commission = 'operations/commission'
    withdraw = 'operations/withdraw'
    fee = 'operations/fee'
    fee_plan = 'operations/fee-plan'
    operations = 'operations'


class _PlisioRequest:
    def __init__(
            self,
            url: str,
            data: Dict[str, Any],
            response_class: Type['plisio.PlisioModel'],
            method: str = 'get',
    ):
        self.url = url
        self.data = data
        self.__response_class = response_class
        self.method = method

        self.__processed = False
        self.__response_status = None
        self.__response = None

    def set_response(self, status_code: int, response_dict: 'plisio.RType'):
        if self.__processed:
            raise plisio.RequestAlreadyProcessed()
        self.__processed = True
        self.__response_status = status_code
        self.__handle_processed_request(response_dict)

    def __handle_processed_request(self, response_dict: 'plisio.RType') -> 'plisio.ModelType':
        if self.response_status in [200, 201]:
            if self.__response_class is not None:
                data: 'plisio.RType' = response_dict['data']
                if isinstance(data, list):
                    self.__response = self.__response_class.list_of_models(data)
                else:
                    self.__response = self.__response_class.from_response(data)
        else:
            self.__handle_exception(response_dict)

    def __handle_exception(self, response_dict: 'plisio.RType'):
        message = response_dict.get('message')
        if self.response_status == 400:
            raise plisio.BadRequestError(message)
        if self.response_status == 401:
            raise plisio.UnauthorizedError(message)
        if self.response_status == 403:
            raise plisio.ForbiddenError(message)
        if self.response_status == 404:
            raise plisio.NotFoundError(message)
        if self.response_status == 405:
            raise plisio.MethodNotAllowedError(message)
        if self.response_status == 406:
            raise plisio.NotAcceptableError(message)
        if self.response_status == 415:
            raise plisio.UnsupportedMediaTypeError(message)
        if self.response_status == 422:
            raise plisio.UnprocessableEntityTypeError(message)
        if self.response_status == 429:
            raise plisio.RateLimitReachedError(message)
        if self.response_status == 500:
            raise plisio.InternalServerError(message)
        if self.response_status == 503:
            raise plisio.ServiceUnavailableError(message)
        raise plisio.PlisioError(message)

    @property
    def response_status(self) -> int:
        if self.__processed:
            return self.__response_status
        raise plisio.RequestNotProcessed()

    @property
    def response(self) -> 'plisio.ModelType':
        if self.__processed:
            return self.__response
        raise plisio.RequestNotProcessed()


class _BaseClient:
    _url = _PlisioUrl
    __api_url = 'https://plisio.net/api/v1/'

    def __init__(self, api_key: str):
        self.__api_key = api_key

    @staticmethod
    def __prepare_data(data: Dict[str, Any]):
        for key in list(data):
            if data[key] is None:
                del data[key]
            elif isinstance(data[key], float):
                data[key] = "{:.8f}".format(data[key]).rstrip('0')
            elif isinstance(data[key], bool):
                if data[key]:
                    data[key] = '1'
                else:
                    del data[key]

    def __create_request(
            self,
            uri: str,
            data: Dict[str, Any],
            response_class: Type['plisio.PlisioModel'],
            method: str = 'get',
    ) -> '_PlisioRequest':
        url = self.__api_url + uri
        self.__prepare_data(data)
        data['api_key'] = self.__api_key
        return _PlisioRequest(url, data, response_class, method)

    def _get_balance_request(self, **kwargs) -> '_PlisioRequest':
        return self.__create_request(
            self._url.balance + '/' + kwargs['currency'].name,
            {},
            plisio.Balance
        )

    def _get_currencies_request(self, **kwargs) -> '_PlisioRequest':
        url_ = '/' + kwargs['fiat_currency'].name if kwargs.get('fiat_currency') else ''
        return self.__create_request(
            self._url.currencies + url_,
            {},
            plisio.Currency
        )

    def _invoice_request(self, **kwargs) -> '_PlisioRequest':
        return self.__create_request(
            self._url.invoice,
            {
                'currency': kwargs['currency'].name,
                'order_name': kwargs['order_name'],
                'order_number': kwargs['order_number'],
                'amount': kwargs['amount'],
                'source_currency': kwargs['source_currency'] and kwargs['source_currency'].name,
                'source_amount': kwargs['source_amount'],
                'allowed_psys_cids': kwargs['allowed_currencies'] and ','.join(
                    [c.name for c in kwargs['allowed_currencies']]
                ),
                'description': kwargs['description'],
                'callback_url': kwargs['callback_url'],
                'email': kwargs['email'],
                'language': kwargs['language'],
                'plugin': kwargs['plugin'],
                'version': kwargs['version'],
                'redirect_to_invoice': kwargs['redirect_to_invoice'],
                'expire_min': kwargs['expire_min'],
            },
            plisio.Invoice
        )

    def _get_commission_request(self, **kwargs) -> '_PlisioRequest':
        return self.__create_request(
            self._url.commission + '/' + kwargs['crypto_currency'].name,
            {
                'addresses': kwargs['addresses'] and ','.join(kwargs['addresses']),
                'amounts':
                    ','.join(map(lambda s: "{:.8f}".format(s), kwargs['amounts']))
                    if isinstance(kwargs['amounts'], list)
                    else kwargs['amounts'] and "{:.8f}".format(kwargs['amounts']),
                'type': kwargs['type_'] and kwargs['type_'].name,
                'feePlan': kwargs['fee_plan'] and kwargs['fee_plan'].name,
                'customFeeRate': kwargs['custom_fee_rate'],
            },
            plisio.Commission
        )

    def _withdraw_request(self, **kwargs) -> '_PlisioRequest':
        return self.__create_request(
            self._url.withdraw,
            {
                'psys_cid': kwargs['crypto_currency'].name,
                'to': ','.join(kwargs['to']) if isinstance(kwargs['to'], list) else kwargs['to'],
                'amount':
                    ','.join(map(lambda s: "{:.8f}".format(s), kwargs['amount']))
                    if isinstance(kwargs['amount'], list)
                    else "{:.8f}".format(kwargs['amount']),
                'type': kwargs['type_'] and kwargs['type_'].name,
                'feePlan': kwargs['fee_plan'] and kwargs['fee_plan'].name,
                'feeRate': kwargs['fee_rate'],
            },
            plisio.Withdraw
        )

    def _get_fee_request(self, **kwargs) -> '_PlisioRequest':
        return self.__create_request(
            self._url.fee + '/' + kwargs['currency'].name,
            {
                'addresses':
                    ','.join(kwargs['addresses']) if isinstance(kwargs['addresses'], list) else kwargs['addresses'],
                'amounts':
                    ','.join(map(lambda s: "{:.8f}".format(s), kwargs['amounts']))
                    if isinstance(kwargs['amounts'], list)
                    else "{:.8f}".format(kwargs['amounts']),
                'feePlan': kwargs['fee_plan'] and kwargs['fee_plan'].name,
            },
            plisio.Fee
        )

    def _get_fee_plan_request(self, **kwargs) -> '_PlisioRequest':
        return self.__create_request(
            self._url.fee_plan + '/' + kwargs['currency'].name,
            {},
            plisio.FeePlan
        )

    def _get_operations_request(self, **kwargs) -> '_PlisioRequest':
        return self.__create_request(
            self._url.operations,
            {
                'page': kwargs['page'],
                'limit': kwargs['limit'],
                'shop_id': kwargs['shop_id'],
                'type': kwargs['type_'] and plisio.OperationType[kwargs['type_']],
                'status': kwargs['status'] and plisio.OperationStatus[kwargs['status']],
                'currency': kwargs['currency'] and plisio.CryptoCurrency[kwargs['currency']],
                'search': kwargs['search'],
            },
            plisio.Operations
        )

    def _get_operation_request(self, **kwargs) -> '_PlisioRequest':
        return self.__create_request(
            self._url.operations + '/' + kwargs['id_'],
            {},
            plisio.Operation
        )


class PlisioClient(_BaseClient):
    @staticmethod
    def _send_request(request: '_PlisioRequest') -> 'plisio.ModelType':
        try:
            _req = requests.request(
                request.method,
                request.url,
                params=request.data,
            )
            status = _req.status_code
            if _req.history:
                data = {'status': 'redirect', 'data': {'invoice_url': _req.url}}
            else:
                data = _req.json()
        except requests.exceptions.RequestException as re:
            raise plisio.UnknownPlisioAPIError() from re
        else:
            request.set_response(status, data)
            return request.response

    def get_balance(self, currency: 'plisio.CryptoCurrency') -> 'plisio.Balance':
        """
        /balances/{psys_cid}
        Get cryptocurrency balance
        """
        request = self._get_balance_request(currency=currency)
        return self._send_request(request)

    def get_currencies(
            self,
            fiat_currency: Optional['plisio.FiatCurrency'] = None,
    ) -> List['plisio.Currency']:
        """
        /currencies/{fiat}
        List of supported cryptocurrencies
        """
        request = self._get_currencies_request(fiat_currency=fiat_currency)
        return self._send_request(request)

    def invoice(
            self,
            currency: 'plisio.CryptoCurrency',
            order_name: str,
            order_number: int,
            amount: float,
            source_currency: Optional['plisio.FiatCurrency'] = None,
            source_amount: Optional[float] = None,
            allowed_currencies: Optional[List['plisio.CryptoCurrency']] = None,
            description: Optional[str] = None,
            callback_url: Optional[str] = None,
            email: Optional[str] = None,
            language: Optional[str] = 'en_US',
            plugin: Optional[str] = None,
            version: Optional[str] = None,
            redirect_to_invoice: Optional[bool] = None,
            expire_min: Optional[int] = None,
    ) -> List['plisio.Invoice']:
        """
        /invoices/new
        Create new invoice
        """
        request = self._invoice_request(
            currency=currency,
            order_name=order_name,
            order_number=order_number,
            amount=amount,
            source_currency=source_currency,
            source_amount=source_amount,
            allowed_currencies=allowed_currencies,
            description=description,
            callback_url=callback_url,
            email=email,
            language=language,
            plugin=plugin,
            version=version,
            redirect_to_invoice=redirect_to_invoice,
            expire_min=expire_min,
        )
        return self._send_request(request)

    def get_commission(
            self,
            crypto_currency: 'plisio.CryptoCurrency',
            addresses: Optional[Union[str, List[str]]] = None,
            amounts: Optional[Union[float, List[float]]] = None,
            type_: Optional['plisio.OperationType'] = None,
            fee_plan: Optional['plisio.PlanName'] = None,
            custom_fee_rate: Optional[int] = None,
    ) -> 'plisio.Commission':
        """
        /operations/commission/{psys_cid}
        Estimate cryptocurrency fee and Plisio commission
        """
        request = self._get_commission_request(
            crypto_currency=crypto_currency,
            addresses=addresses,
            amounts=amounts,
            type_=type_,
            fee_plan=fee_plan,
            custom_fee_rate=custom_fee_rate,
        )
        return self._send_request(request)

    def withdraw(
            self,
            crypto_currency: 'plisio.CryptoCurrency',
            to: Union[str, List[str]],
            amount: Union[float, List[float]],
            type_: Optional['plisio.OperationType'] = None,
            fee_plan: Optional['plisio.PlanName'] = None,
            fee_rate: Optional[float] = None,
    ) -> 'plisio.Withdraw':
        """
        /operations/withdraw
        Withdrawal operation
        """
        request = self._withdraw_request(
            crypto_currency=crypto_currency,
            to=to,
            amount=amount,
            type_=type_,
            fee_plan=fee_plan,
            fee_rate=fee_rate,
        )
        return self._send_request(request)

    def get_fee(
            self,
            currency: 'plisio.CryptoCurrency',
            addresses: Union[str, List[str]],
            amounts: Union[float, List[float]],
            fee_plan: Optional['plisio.PlanName'] = None,
    ) -> 'plisio.Fee':
        """
        /operations/fee/{psys_cid}
        Estimate fee
        """
        request = self._get_fee_request(
            currency=currency,
            addresses=addresses,
            amounts=amounts,
            fee_plan=fee_plan,
        )
        return self._send_request(request)

    def get_fee_plan(self, currency: 'plisio.CryptoCurrency') -> 'plisio.FeePlan':
        """
        /operations/fee-plan/{psys_cid}
        Get Plisio fee plans
        """
        request = self._get_fee_plan_request(
            currency=currency,
        )
        return self._send_request(request)

    def get_operations(
            self,
            page: Optional[int] = None,
            limit: Optional[int] = None,
            shop_id: Optional[str] = None,
            type_: Optional['plisio.OperationType'] = None,
            status: Optional['plisio.OperationStatus'] = None,
            currency: Optional['plisio.CryptoCurrency'] = None,
            search: Optional[str] = None,
    ) -> 'plisio.Operations':
        """
        /operations
        List of all user transactions
        """
        request = self._get_operations_request(
            page=page,
            limit=limit,
            shop_id=shop_id,
            type_=type_,
            status=status,
            currency=currency,
            search=search,
        )
        return self._send_request(request)

    def get_operation(self, id_: str) -> 'plisio.Operation':
        """
        /operations/{id}
        Transaction details
        """
        request = self._get_operation_request(
            id_=id_,
        )
        return self._send_request(request)


class PlisioAioClient(_BaseClient):
    @staticmethod
    async def _send_request(request: '_PlisioRequest'):
        try:
            async with aiohttp.ClientSession() as session:
                async with session.request(
                        request.method,
                        request.url,
                        params=request.data,
                ) as _req:
                    status = _req.status
                    if _req.history:
                        data = {'status': 'redirect', 'data': {'invoice_url': _req.url}}
                    else:
                        data = await _req.json()
        except aiohttp.ClientError as ce:
            raise plisio.UnknownPlisioAPIError() from ce
        else:
            request.set_response(status, data)
            return request.response

    async def get_balance(
            self,
            currency: 'plisio.CryptoCurrency',
    ) -> 'plisio.Balance':
        """
        /balances/{psys_cid}
        Async method to get cryptocurrency balance
        """
        request = self._get_balance_request(
            currency=currency,
        )
        return await self._send_request(request)

    async def get_currencies(
            self,
            fiat_currency: Optional['plisio.FiatCurrency'] = None,
    ) -> List['plisio.Currency']:
        """
        /currencies/{fiat}
        List of supported cryptocurrencies
        """
        request = self._get_currencies_request(fiat_currency=fiat_currency)
        return await self._send_request(request)

    async def invoice(
            self,
            currency: 'plisio.CryptoCurrency',
            order_name: str,
            order_number: int,
            amount: float,
            source_currency: Optional['plisio.FiatCurrency'] = None,
            source_amount: Optional[float] = None,
            allowed_currencies: Optional[List['plisio.CryptoCurrency']] = None,
            description: Optional[str] = None,
            callback_url: Optional[str] = None,
            email: Optional[str] = None,
            language: Optional[str] = 'en_US',
            plugin: Optional[str] = None,
            version: Optional[str] = None,
            redirect_to_invoice: Optional[bool] = None,
            expire_min: Optional[int] = None,
    ) -> List['plisio.Invoice']:
        """
        /invoices/new
        Async method to create new invoice
        """
        request = self._invoice_request(
            currency=currency,
            order_name=order_name,
            order_number=order_number,
            amount=amount,
            source_currency=source_currency,
            source_amount=source_amount,
            allowed_currencies=allowed_currencies,
            description=description,
            callback_url=callback_url,
            email=email,
            language=language,
            plugin=plugin,
            version=version,
            redirect_to_invoice=redirect_to_invoice,
            expire_min=expire_min,
        )
        return await self._send_request(request)

    async def get_commission(
            self,
            crypto_currency: 'plisio.CryptoCurrency',
            addresses: Optional[Union[str, List[str]]] = None,
            amounts: Optional[Union[float, List[float]]] = None,
            type_: Optional['plisio.OperationType'] = None,
            fee_plan: Optional['plisio.PlanName'] = None,
            custom_fee_rate: Optional[int] = None,
    ) -> 'plisio.Commission':
        """
        /operations/commission/{psys_cid}
        Async method to estimate cryptocurrency fee and Plisio commission
        """
        request = self._get_commission_request(
            crypto_currency=crypto_currency,
            addresses=addresses,
            amounts=amounts,
            type_=type_,
            fee_plan=fee_plan,
            custom_fee_rate=custom_fee_rate,
        )
        return await self._send_request(request)

    async def withdraw(
            self,
            crypto_currency: 'plisio.CryptoCurrency',
            to: Union[str, List[str]],
            amount: Union[float, List[float]],
            fee_plan: Optional['plisio.PlanName'] = None,
            fee_rate: Optional[float] = None,
            type_: Optional['plisio.OperationType'] = None,
    ) -> 'plisio.Withdraw':
        """
        /operations/withdraw
        Async method to withdrawal operation
        """
        request = self._withdraw_request(
            crypto_currency=crypto_currency,
            to=to,
            amount=amount,
            fee_plan=fee_plan,
            fee_rate=fee_rate,
            type_=type_,
        )
        return await self._send_request(request)

    async def get_fee(
            self,
            currency: 'plisio.CryptoCurrency',
            addresses: Union[str, List[str]],
            amounts: Union[float, List[float]],
            fee_plan: Optional['plisio.PlanName'] = None,
    ) -> 'plisio.Fee':
        """
        /operations/fee/{psys_cid}
        Async method to estimate fee
        """
        request = self._get_fee_request(
            currency=currency,
            addresses=addresses,
            amounts=amounts,
            fee_plan=fee_plan,
        )
        return await self._send_request(request)

    async def get_fee_plan(self, currency: 'plisio.CryptoCurrency') -> 'plisio.FeePlan':
        """
        /operations/fee-plan/{psys_cid}
        Async method to get Plisio fee plans
        """
        request = self._get_fee_plan_request(
            currency=currency,
        )
        return await self._send_request(request)

    async def get_operations(
            self,
            page: Optional[int] = None,
            limit: Optional[int] = None,
            shop_id: Optional[str] = None,
            type_: Optional['plisio.OperationType'] = None,
            status: Optional['plisio.OperationStatus'] = None,
            currency: Optional['plisio.CryptoCurrency'] = None,
            search: Optional[str] = None,
    ) -> List['plisio.Operation']:
        """
        /operations
        Async method to list of all user transactions
        """
        request = self._get_operations_request(
            page=page,
            limit=limit,
            shop_id=shop_id,
            type_=type_,
            status=status,
            currency=currency,
            search=search,
        )
        return await self._send_request(request)

    async def get_operation(self, id_: str) -> 'plisio.Operation':
        """
        /operations/{id}
        Async method to transaction details
        """
        request = self._get_operation_request(
            id_=id_,
        )
        return await self._send_request(request)
