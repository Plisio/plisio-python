from typing import Dict, List, Optional, Union

import plisio


class PlisioModel:
    @classmethod
    def from_response(cls, response_dict: 'plisio.RType'):
        raise NotImplementedError()

    @classmethod
    def list_of_models(cls, response_list: List['plisio.RType']):
        return [
            cls.from_response(response_dict)
            for response_dict in response_list
        ]

    def __repr__(self):
        return '<' + f'{super().__repr__()}: ' + str(self.__dict__) + '>'


class Balance(PlisioModel):
    """
    /balances/{psys_cid}
    Get plisio.CryptoCurrency balance
    """

    def __init__(
            self,
            currency: 'plisio.CryptoCurrency',
            balance: float,
            locked_balance: Optional[float]
    ):
        self.currency = currency
        self.balance = balance
        self.locked_balance = locked_balance

    @classmethod
    def from_response(cls, response_dict: 'plisio.RType') -> 'Balance':
        return cls(
            response_dict.get('psys_cid') and plisio.CryptoCurrency[response_dict['psys_cid']],
            response_dict.get('balance') and float(response_dict['balance']),
            response_dict.get('lockedBalance') and float(response_dict['lockedBalance']),
        )


class Currency(PlisioModel):
    """
    /currencies/{fiat}
    List of supported cryptocurrencies
    """

    def __init__(
            self,
            currency: 'plisio.CryptoCurrency',
            icon: str,
            rate_usd: float,
            price_usd: float,
            precision: int,
            fiat: 'plisio.FiatCurrency',
            fiat_rate: float,
            min_sum_in: float,
            invoice_commission_percentage: int,
    ):
        self.currency = currency
        self.icon = icon
        self.rate_usd = rate_usd
        self.price_usd = price_usd
        self.precision = precision
        self.fiat = fiat
        self.fiat_rate = fiat_rate
        self.min_sum_in = min_sum_in
        self.invoice_commission_percentage = invoice_commission_percentage

    @classmethod
    def from_response(cls, response_dict: 'plisio.RType') -> 'Currency':
        return cls(
            response_dict.get('cid') and plisio.CryptoCurrency[response_dict['cid'].replace('-', '_')],
            response_dict.get('icon') and str(response_dict['icon']),
            response_dict.get('rate_usd') and float(response_dict['rate_usd']),
            response_dict.get('price_usd') and float(response_dict['price_usd']),
            response_dict.get('precision') and int(response_dict['precision']),
            response_dict.get('fiat') and plisio.FiatCurrency[response_dict['fiat']],
            response_dict.get('fiat_rate') and float(response_dict['fiat_rate']),
            response_dict.get('min_sum_in') and float(response_dict['min_sum_in']),
            response_dict.get('invoice_commission_percentage') and int(response_dict['invoice_commission_percentage']),
        )


class Invoice(PlisioModel):
    """
    /invoices/new
    Create new invoice
    """

    def __init__(
            self,
            txn_id: str,
            invoice_url: str,
            amount: Optional[float],
            pending_amount: Optional[float],
            wallet_hash: Optional[str],
            currency: Optional['plisio.CryptoCurrency'],
            source_currency: Optional['plisio.FiatCurrency'],
            source_rate: Optional[float],
            expected_confirmations: Optional[int],
            qr_code: Optional[str],
            verify_hash: Optional[str],
            invoice_commission: Optional[float],
            invoice_sum: Optional[float],
            invoice_total_sum: Optional[float],
    ):
        self.txn_id = txn_id
        self.invoice_url = invoice_url
        self.amount = amount
        self.pending_amount = pending_amount
        self.wallet_hash = wallet_hash
        self.currency = currency
        self.source_currency = source_currency
        self.source_rate = source_rate
        self.expected_confirmations = expected_confirmations
        self.qr_code = qr_code
        self.verify_hash = verify_hash
        self.invoice_commission = invoice_commission
        self.invoice_sum = invoice_sum
        self.invoice_total_sum = invoice_total_sum

    @classmethod
    def from_response(cls, response_dict: 'plisio.RType') -> 'Invoice':
        return cls(
            response_dict.get('txn_id') and str(response_dict['txn_id']),
            response_dict.get('invoice_url') and str(response_dict['invoice_url']),
            response_dict.get('amount') and float(response_dict['amount']),
            response_dict.get('pending_amount') and float(response_dict['pending_amount']),
            response_dict.get('wallet_hash') and str(response_dict['wallet_hash']),
            response_dict.get('currency') and plisio.CryptoCurrency[response_dict.get('currency')],
            response_dict.get('source_currency') and plisio.FiatCurrency[response_dict.get('source_currency')],
            response_dict.get('source_rate') and float(response_dict['source_rate']),
            response_dict.get('expected_confirmations') and int(response_dict['expected_confirmations']),
            response_dict.get('qr_code') and str(response_dict['qr_code']),
            response_dict.get('verify_hash') and str(response_dict['verify_hash']),
            response_dict.get('invoice_commission') and float(response_dict['invoice_commission']),
            response_dict.get('invoice_sum') and float(response_dict['invoice_sum']),
            response_dict.get('invoice_total_sum') and float(response_dict['invoice_total_sum']),
        )


class Plan(PlisioModel):
    """
    Sub-model for FeePlan, WithdrawParams
    """

    def __init__(
            self,
            conf_target: int,
            fee_rate: int,
            dynamic_field: str,
            plan: 'plisio.PlanName',
            unit: str,
            value: float,
    ):
        self.conf_target = conf_target
        self.fee_rate = fee_rate
        self.dynamic_field = dynamic_field
        self.plan = plan
        self.unit = unit
        self.value = value

    @classmethod
    def from_response(cls, response_dict: Dict[str, Union[str, dict]]) -> 'Plan':
        return cls(
            response_dict.get('conf_target') and int(response_dict['conf_target']),
            response_dict.get('feeRate') and int(response_dict['feeRate']),
            response_dict.get('dynamicField'),
            response_dict.get('plan') and plisio.PlanName[response_dict['plan']],
            response_dict.get('unit'),
            response_dict.get('value') and float(response_dict['value']),
        )


class FeePlan(PlisioModel):
    """
    /operations/fee-plan/{psys_cid}
    Get Plisio fee plans
    Sub-model for Commission
    """

    def __init__(
            self,
            currency: 'plisio.CryptoCurrency',
            economy: Optional['Plan'] = None,
            normal: Optional['Plan'] = None,
            priority: Optional['Plan'] = None,
            custom: Optional['Plan'] = None,
    ):
        self.currency = currency
        self.economy = economy
        self.normal = normal
        self.priority = priority
        self.custom = custom

    @classmethod
    def from_response(cls, response_dict: Dict[str, Union[str, dict]]) -> 'FeePlan':
        return cls(
            response_dict.get('psys_cid') and plisio.CryptoCurrency[response_dict['psys_cid']],
            response_dict.get('economy') and Plan.from_response(response_dict['economy']),
            response_dict.get('normal') and Plan.from_response(response_dict['normal']),
            response_dict.get('priority') and Plan.from_response(response_dict['priority']),
            response_dict.get('custom') and Plan.from_response(response_dict['custom']),
        )


class Custom(PlisioModel):
    """
    Sub-model for Commission
    """

    def __init__(
            self,
            min_: int,
            max_: int,
            default: int,
            borders: int,
            unit: str,
    ):
        self.min = min_
        self.max = max_
        self.default = default
        self.borders = borders
        self.unit = unit

    @classmethod
    def from_response(cls, response_dict: Dict[str, Union[str, dict]]) -> 'Custom':
        return cls(
            response_dict.get('min') and int(response_dict['min']),
            response_dict.get('max') and int(response_dict['max']),
            response_dict.get('default') and int(response_dict['default']),
            response_dict.get('borders') and int(response_dict['borders']),
            response_dict.get('unit'),
        )


class Commission(PlisioModel):
    """
    /operations/commission/{psys_cid}
    Estimate cryptocurrency fee and Plisio commission
    """

    def __init__(
            self,
            commission: float,
            fee: float,
            max_amount: float,
            plan: 'plisio.PlanName',
            use_wallet: Optional[int],
            use_wallet_balance: Optional[int],
            plans: 'FeePlan',
            custom: 'Custom',
            errors: Optional[int],
            custom_fee_rate: int
    ):
        self.commission = commission
        self.fee = fee
        self.max_amount = max_amount
        self.plan = plan
        self.use_wallet = use_wallet
        self.use_wallet_balance = use_wallet_balance
        self.plans = plans
        self.custom = custom
        self.errors = errors
        self.custom_fee_rate = custom_fee_rate

    @classmethod
    def from_response(cls, response_dict: Dict[str, Union[str, dict]]) -> 'Commission':
        return cls(
            response_dict.get('commission') and float(response_dict['commission']),
            response_dict.get('fee') and float(response_dict['fee']),
            response_dict.get('maxAmount') and float(response_dict['maxAmount']),
            response_dict.get('plan') and plisio.PlanName[response_dict['plan']],
            response_dict.get('useWallet') and int(response_dict['useWallet']),
            response_dict.get('useWalletBalance') and int(response_dict['useWalletBalance']),
            response_dict.get('plans') and FeePlan.from_response(response_dict['plans']),
            response_dict.get('custom') and Custom.from_response(response_dict['custom']),
            response_dict.get('errors') and int(response_dict['errors']),
            response_dict.get('customFeeRate') and int(response_dict['customFeeRate']),
        )


class WithdrawParams(PlisioModel):
    """
    Sub-model for Withdraw
    """

    def __init__(
            self,
            source_currency: 'plisio.CryptoCurrency',
            source_rate: float,
            usd_rate: Optional[float],
            fee: Optional['Plan'],
    ):
        self.source_currency = source_currency
        self.source_rate = source_rate
        self.usd_rate = usd_rate
        self.fee = fee

    @classmethod
    def from_response(cls, response_dict: 'plisio.RType') -> 'WithdrawParams':
        return cls(
            response_dict.get('source_currency'),
            response_dict.get('source_rate') and float(response_dict['source_rate']),
            response_dict.get('usd_rate') and float(response_dict['usd_rate']),
            response_dict.get('fee') and Plan.from_response(response_dict['fee']),
        )


class Withdraw(PlisioModel):
    """
    /operations/withdraw
    Create a copy of invoice
    """

    def __init__(
            self,
            type_: 'plisio.OperationType',
            status: str,
            currency: 'plisio.CryptoCurrency',
            source_currency: 'plisio.FiatCurrency',
            source_rate: float,
            fee: float,
            wallet_hash: str,
            sendmany: List[Dict[str, float]],
            params: 'WithdrawParams',
            created_at_utc: int,
            amount: float,
            tx_url: str,
            tx_id: List[str],
            id_: str,
    ):
        self.type = type_
        self.status = status
        self.currency = currency
        self.source_currency = source_currency
        self.source_rate = source_rate
        self.fee = fee
        self.wallet_hash = wallet_hash
        self.sendmany = sendmany
        self.params = params
        self.created_at_utc = created_at_utc
        self.amount = amount
        self.tx_url = tx_url
        self.tx_id = tx_id
        self.id = id_

    @classmethod
    def from_response(cls, response_dict: 'plisio.RType') -> 'Withdraw':
        return cls(
            response_dict.get('type') and plisio.OperationType[response_dict['type']],
            response_dict.get('status') and str(response_dict['status']),
            response_dict.get('psys_cid') and plisio.CryptoCurrency[response_dict['psys_cid']],
            response_dict.get('source_currency') and plisio.FiatCurrency[response_dict['source_currency']],
            response_dict.get('source_rate') and float(response_dict['source_rate']),
            response_dict.get('fee') and float(response_dict['fee']),
            response_dict.get('wallet_hash'),
            response_dict.get('sendmany') and [[{k: float(v)} for k, v in sm.items()] for sm in response_dict['sendmany']],
            response_dict.get('params') and WithdrawParams.from_response(response_dict['params']),
            response_dict.get('created_at_utc') and int(response_dict['created_at_utc']),
            response_dict.get('amount') and float(response_dict['amount']),
            response_dict.get('tx_url') and str(response_dict['tx_url']),
            response_dict.get('tx_id'),
            response_dict.get('id'),
        )


class Fee(PlisioModel):
    """
    /operations/fee/{psys_cid}
    Estimate fee
    """

    def __init__(
            self,
            fee: float,
            currency: 'plisio.CryptoCurrency',
            plan: 'plisio.PlanName'
    ):
        self.fee = fee
        self.currency = currency
        self.plan = plan

    @classmethod
    def from_response(cls, response_dict: 'plisio.RType') -> 'Fee':
        return cls(
            response_dict.get('fee') and float(response_dict['fee']),
            response_dict.get('psys_cid') and plisio.CryptoCurrency[response_dict['psys_cid']],
            response_dict.get('plan') and plisio.PlanName[response_dict['plan']],
        )


class OperationTx(PlisioModel):
    """
    Sub-model for Operation
    """

    def __init__(
            self,
            txid: str,
            block: int,
            confirmations: int,
            value: float,
            processed: bool,
            fail_retry: int,
            fee_rate: float,
            fee_rate_unit: str,
            url: str,
            wallet_hash: List[str],
    ):
        self.txid = txid
        self.block = block
        self.confirmations = confirmations
        self.value = value
        self.processed = processed
        self.fail_retry = fail_retry
        self.fee_rate = fee_rate
        self.fee_rate_unit = fee_rate_unit
        self.url = url
        self.wallet_hash = wallet_hash

    @classmethod
    def from_response(cls, response_dict: 'plisio.RType') -> 'OperationTx':
        return cls(
            response_dict.get('txid') and str(response_dict['txid']),
            response_dict.get('block') and int(response_dict['block']),
            response_dict.get('confirmations') and int(response_dict['confirmations']),
            response_dict.get('value') and float(response_dict['value']),
            response_dict.get('processed'),
            response_dict.get('failRetry') and int(response_dict['failRetry']),
            response_dict.get('feeRate') and float(response_dict['feeRate']),
            response_dict.get('feeRateUnit') and response_dict['feeRateUnit'],
            response_dict.get('url'),
            response_dict.get('wallet_hash'),
        )


class OperationParams(PlisioModel):
    """
    Sub-model for Operation
    """

    def __init__(
            self,
            order_number: str,
            order_name: Optional[str],
            source_amount: Optional[float],
            source_currency: 'plisio.CryptoCurrency',
            currency: Optional['plisio.CryptoCurrency'],
            amount: Optional[float],
            source_rate: float,
            email: str,
            usd_rate: Optional[float],
            fee: Optional['Plan'],
    ):
        self.source_currency = source_currency
        self.source_rate = source_rate
        self.usd_rate = usd_rate
        self.fee = fee
        self.order_number = order_number
        self.order_name = order_name
        self.source_amount = source_amount
        self.currency = currency
        self.amount = amount
        self.email = email

    @classmethod
    def from_response(cls, response_dict: 'plisio.RType') -> 'OperationParams':
        return cls(
            response_dict.get('order_number'),
            response_dict.get('order_name'),
            response_dict.get('source_amount') and float(response_dict['source_amount']),
            response_dict.get('source_currency'),
            response_dict.get('currency'),
            response_dict.get('amount') and float(response_dict['amount']),
            response_dict.get('source_rate') and float(response_dict['source_rate']),
            response_dict.get('email'),
            response_dict.get('usd_rate') and float(response_dict['usd_rate']),
            response_dict.get('fee') and Plan.from_response(response_dict['fee']),
        )


class Operation(PlisioModel):
    """
    /operations
    List of all user transactions
    /operations/{id}
    Create new invoice
    """

    def __init__(
            self,
            user_id: int,
            shop_id: str,
            type_: 'plisio.OperationType',
            status: 'plisio.OperationStatus',
            pending_sum: float,
            currency: 'plisio.CryptoCurrency',
            source_currency: 'plisio.FiatCurrency',
            source_rate: float,
            fee: float,
            wallet_hash: str,
            sendmany: List[Dict[str, float]],
            params: 'OperationParams',
            expire_at_utc: int,
            created_at_utc: int,
            amount: float,
            sum_: float,
            commission: float,
            tx_url: str,
            tx_id: List[str],
            id_: str,
            actual_sum: float,
            actual_commission: float,
            actual_fee: float,
            actual_invoice_sum: float,
            tx: List[OperationTx],
            status_code: int,
    ):
        self.user_id = user_id
        self.shop_id = shop_id
        self.type = type_
        self.status = status
        self.pending_sum = pending_sum
        self.currency = currency
        self.source_currency = source_currency
        self.source_rate = source_rate
        self.fee = fee
        self.wallet_hash = wallet_hash
        self.sendmany = sendmany
        self.params = params
        self.expire_at_utc = expire_at_utc
        self.created_at_utc = created_at_utc
        self.amount = amount
        self.sum = sum_
        self.commission = commission
        self.tx_url = tx_url
        self.tx_id = tx_id
        self.id = id_
        self.actual_sum = actual_sum
        self.actual_commission = actual_commission
        self.actual_fee = actual_fee
        self.actual_invoice_sum = actual_invoice_sum
        self.tx = tx
        self.status_code = status_code

    @classmethod
    def from_response(cls, response_dict: 'plisio.RType') -> 'Operation':
        return cls(
            response_dict.get('user_id') and int(response_dict['user_id']),
            response_dict.get('shop_id'),
            response_dict.get('type') and plisio.OperationType[response_dict['type']],
            response_dict.get('status') and plisio.OperationStatus[response_dict['status']],
            response_dict.get('pending_sum') and float(response_dict['pending_sum']),
            response_dict.get('currency') and plisio.CryptoCurrency[response_dict['currency']],
            response_dict.get('source_currency') and plisio.FiatCurrency[response_dict['source_currency']],
            response_dict.get('source_rate') and float(response_dict['source_rate']),
            response_dict.get('fee') and float(response_dict['fee']),
            response_dict.get('wallet_hash'),
            response_dict.get('sendmany') and [[{k: float(v)} for k, v in sm.items()] for sm in response_dict['sendmany']],
            response_dict.get('params') and OperationParams.from_response(response_dict['params']),
            response_dict.get('expire_at_utc') and int(response_dict['expire_at_utc']),
            response_dict.get('created_at_utc') and int(response_dict['created_at_utc']),
            response_dict.get('amount') and float(response_dict['amount']),
            response_dict.get('sum') and float(response_dict['sum']),
            response_dict.get('commission') and float(response_dict['commission']),
            response_dict.get('tx_url'),
            response_dict.get('tx_id'),
            response_dict.get('id'),
            response_dict.get('actual_sum') and float(response_dict['actual_sum']),
            response_dict.get('actual_commission') and float(response_dict['actual_commission']),
            response_dict.get('actual_fee') and float(response_dict['actual_fee']),
            response_dict.get('actual_invoice_sum') and float(response_dict['actual_invoice_sum']),
            response_dict.get('tx') and [OperationTx.from_response(tx) for tx in response_dict['tx']],
            response_dict.get('status_code') and int(response_dict['status_code']),
        )


class Operations(PlisioModel):
    """
    Wrapper for Operation
    """

    def __init__(
            self,
            operations: List['Operation'],
            links: Dict[str, Dict[str, str]],
            meta: Dict[str, int],
    ):
        self.operations = operations
        self.links = links
        self.meta = meta

    @classmethod
    def from_response(cls, response_dict: 'plisio.RType') -> 'Operations':
        return cls(
            response_dict.get('operations') and [Operation.from_response(op) for op in response_dict['operations']],
            response_dict.get('_links'),
            response_dict.get('_meta'),
        )
