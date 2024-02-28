# Python SDK for Plisio API

Current project is a **Python SDK for [Plisio API](https://plisio.net/documentation)**.
To use it, you should be registered on Plisio
The account can be created [here](https://plisio.net/account/signup "Sign up"))
You will receive a personal secret key, that is used for all calls to API.

![Supported Versions](https://img.shields.io/badge/python-3.6%20%7C%203.7%20%7C%203.8%20%7C%203.9%20%7C%203.10-yellowgreen)


##  Install

To download Plisio SDK, either fork this GitHub repo or simply use PyPI via pip:
```sh
$ pip install plisio
```

## Usage


### Initialize the connection

To be able to send the requests, create an instance of class
<code>PlisioClient</code>.

```python
import plisio
...

client = plisio.PlisioClient(api_key='your_secret_key')
```

### Balance

Plisio supports 9 cryptocurrencies(https://plisio.net/documentation/appendices/supported-cryptocurrencies).
To view, for example the Ethereum (ETH) balance:
Send the request by <code>client</code> and process the response
with the help of an appropriate model.

```python
# Sending request and getting processed response
balance = client.get_balance(plisio.CryptoCurrency.ETH)
```

### Currencies

To view current exchange rate for the supported cryptocurrencies to
[the definite fiat currency](https://plisio.net/documentation/appendices/supported-fiat-currencies),
send a request to API by the method <code>get_currency</code>
with the selected fiat currency.

Example: getting the rate of *Australian Dollar (AUD)*.
If no fiat currency is selected, the rate of
*United States Dollar (USD)* is used by default. **The response** is a list of models
that consist rates of exchanges.

```python
currencies = client.get_currencies(plisio.FiatCurrency.AUD)
```

### Creating a new invoice

The request has to receive the following **required** parameters:
+ <code>currency</code> - the name of cryptocurrency;
+ <code>order_name</code> - merchant internal order name;
+ <code>order_number</code> - merchant internal order number.

**Additional** parameters:
+ <code>amount</code> - any cryptocurrency float value. If a fiat currency is to be converted,
skip this field and use the next two fields instead;
+ <code>source_currency</code> - the name of the fiat currency;
+ <code>source_amount</code> - any float value;
+ <code>allowed_psys_cids</code> - comma-separated list of cryptocurrencies that are
  allowed for a payment. Also, you will be able to select one of them. Example: *'BTC,ETH,TZEC'*;
+ <code>description</code> - merchant invoice description;
+ <code>callback_url</code> - merchant full URL to get invoice updates.
  The *POST* request will be sent to this URL. If this parameter isn't set,
  a callback will be sent to the URL that can be set under profile in API settings, in the 'Status URL' field; **Add ?json=true to this url to get data in JSON and validate it client.validate_callback**
+ <code>email</code> - an auto-fill invoice email.
  You will be asked to enter an email to which a notification will be sent;
+ <code>language</code> - en_US (supports English only);
+ <code>plugin</code> - Plisio's internal field to determine integration plugin;
+ <code>version</code> - Plisio's internal field to determine integration plugin version.
+ <code>redirect_to_invoice</code> - Instead of JSON response user will be redirected to the Plisio's invoice page (is not working for a white-label shop).
+ <code>expire_min</code> - Interval in minutes when invoice will be expired.

The response is a model that can fill differently depending on
whether you have [**While Label**](https://plisio.net/white-label) or not.
In the first case, only two fields are returned:
<code>txn_id</code> is a Plisio's intertnal ID and
<code>invoice_url</code> is an invoice URL. And in the second case,
 extra fields are added to them:
+ <code>amount</code> - invoice amount in the selected cryptocurrency;
+ <code>pending_amount</code> - the remaining amount to be paid in
  the selected cryptocurrency;
+ <code>wallet_hash</code> - invoice hash;
+ <code>psys_cid</code> - cryptocurrencies ID;
+ <code>currency</code> - cryptocurrencies code;
+ <code>source_currency</code> - fiat currency;
+ <code>source_rate</code> - exchange rate from the <code>psys_cid</code>
  to the <code>source_currency</code> at the moment of transfer;
+ <code>expected_confirmations</code> - the number of expected confirmations
  to mark the invoice as completed;
+ <code>qr_code</code> - QR code image in base64 format;
+ <code>verify_hash</code> - hash to verify the *POST*
  data signed with your *API_KEY*;
+ <code>invoice_commission</code> - Plisio commission;
+ <code>invoice_sum</code> - *shop pays commission*: invoice amount -
  <code>invoice_commission</code>, *client pays commission*: invoice amount;
+ <code>invoice_total_sum</code> - *shop pays commission*: invoice amount,
  *client pays commission*: <code>invoice_commission</code> + <code>invoice_sum</code>.

Create a few *Python* examples, where use:
+ required fields only;
+ all the fields besides the <code>amount</code>;
+ all the fields besides the <code>source_currency</code> and the <code>source_amount</code>.
```python
# Example: using required fields only
first_invoice = plisio.invoice(plisio.CryptoCurrency.BTC, 'order1', 20230903182401, 0.00001)

# Example: using cryptocurrency
second_invoice = plisio.invoice(
    plisio.CryptoCurrency.TRX,
    'order2',
    20230903182402,
    amount=100,
    email='test@plisio.net'
)

# Example: using fiat currency
third_invoice = plisio.invoice(
    plisio.CryptoCurrency.TRX,
    'order3',
    20230903182403,
    source_currency=plisio.FiatCurrency.USD,
    source_rate=10.2,
    allowed_currencies=[plisio.CryptoCurrency.TRX,plisio.CryptoCurrency.USDT_TRX]
)
```

### Validate callback data

To validate invoice's callback data use next code:

<code>PlisioClient</code>.

```python
import plisio
...

client = plisio.PlisioClient(api_key='your_secret_key')
isValid = client.validate_callback(request.body)
```

*If you have some issues with it - verify that you've added **json=true** to yours callback_url*

### Commission

To estimate the cryptocurrency fee and Plisio commission,
call method <code>get_commission</code>. It takes
one required parameter (<code>crypto_currency</code>, the name of the cryptocurrency) and five additional parameters:
+ <code>addresses</code> - wallet address or comma separated addresses when estimating fee for mass withdrawal;
+ <code>amounts</code> - amount or comma separated amount that will be send in case of mass withdraw;
+ <code>type_</code> - operation type, such as:
    + *cash_out*;
    + *mass_cash_out*;
+ <code>fee_plan</code> - the name of [fee plan](https://plisio.net/documentation/endpoints/fee-plans);
+ <code>custom_fee_rate</code> - custom fee plan value.

Method returns the model <code>Commission</code>, which has fields:
+ <code>commission</code> - Plisio commission value;
+ <code>fee</code> - cryptocurrency fee value;
+ <code>max_amount</code> - maximum allowed amount to withdrawal;
+ <code>plan</code> - Plisio's cryptocurrency fee estimation plan,
the <code>PlanName</code> enum;
+ <code>use_wallet</code> - pay fee from wallet;
+ <code>use_wallet_balance</code> - balance of wallet that will be used to pay fee;
+ <code>plans</code> - the model <code>FeePlan</code>;
+ <code>custom</code> - the model <code>Custom</code>;
+ <code>errors</code> - the number of errors;
+ <code>custom_fee_rate</code> - custom fee plan value.

Example: a request using *Ethereum (ETH)*:

```python
commission = plisio.get_commission(
    plisio.CryptoCurrency.ETH
)
```

#### Custom

There are **5** fields:

+ <code>min_</code> - minimal custom fee plan value;
+ <code>max_</code> - maximum custom fee plan value;
+ <code>default</code> - estimated fee parameter to confirm the transaction in
the "conf_target" blocks;
+ <code>borders</code> - rate of the supported plan;
+ <code>unit</code> - fee unit.

### Withdrawal

To withdraw, call the <code>withdraw</code> method and
apply the following parameters:
+ <code>crypto_currency</code> - a name of cryptocurrency;
+ <code>to</code> - hash or multiple comma separated hashes pooled for the *mass_cash_out*;
+ <code>amount</code> - any comma separated float values for the *mass_cash_out*
  in the order that hashes are in <code>to</code> parameter;
+ <code>fee_plan</code> - a name of the one of
  [fee plans](https://plisio.net/documentation/endpoints/fee-plans);
+ <code>fee_rate</code> (expected param, unavailable) - custom feeRate. conf_target (blocks) for BTC like
cryptocurrencies or gasPrice in GWAI for ETH based cryptocurrencies;
+ <code>type_</code> - operation type, likes in <code>get_commission</code> method
  (it's an optional parameter).

After that you are getting model <code>Withdraw</code> with fields:
+ <code>type_</code> - operation type, given in the request;
+ <code>status</code> - specifies whether the operation was completed or not (*completed*, *error*);
+ <code>currency</code> - name of the cryptocurrency;
+ <code>source_currency</code> - name of the fiat currency (only USD available);
+ <code>source_rate</code> - exchange rate from the <code>currency</code> to
  the <code>source_currency</code> at the moment of transfer;
+ <code>fee</code> - transaction fee stated in the transfer;
+ <code>wallet_hash</code> - destination hash (if <code>type_</code> is the *cash_out*);
+ <code>sendmany</code> - dictionary of hashes and values (if <code>type</code> is the *mass_cash_out*);
+ <code>params</code> - a model <code>WithdrawParams</code>;
+ <code>created_at_utc</code> - timestamp in the UTC timezone; it may need to be divided by 1000;
+ <code>amount</code> - transfer amount in cryptocurrency
+ <code>tx_url</code> - link to the cryptocurrency block explorer;
+ <code>tx_id</code> - link of transaction ids;
+ <code>id</code> - internal Plisio operation ID.

```python
withdraw = plisio.withdraw(
    crypto_currency = plisio.CryptoCurrency.LTC,
    to = 'wallet_address',
    amount = float(0.01),
    type_ = plisio.OperationType.cash_out
)
```

### Fee estimation

To estimate fee, apply to <code>get_fee</code> the following parameters:
+ <code>crypto_currency</code> - name of the cryptocurrency;
+ <code>addresses</code> - wallet address or comma separated addresses
  when estimating fee for a mass withdrawal;
+ <code>amounts</code> - amount or comma separated amount
  that will be sent in case of a mass withdraw;
+ <code>fee_plan</code> - a name of the one of
  [fee plans](https://plisio.net/documentation/endpoints/fee-plans)
  (it is not required).

The response model has three fields:
+ <code>fee</code> - transaction fee;
+ <code>currency</code> - name of the cryptocurrency;
+ <code>plan</code> - name of fee plan.

```python
fee = plisio.get_fee(
    plisio.CryptoCurrency.ETH,
    'wallet_address',
    'amount',
    'normal',
)
```

### Fee plan

Returns the model with [fee plans](https://plisio.net/documentation/endpoints/fee-plans)
by selected <code>cryptocurrency</code>. Also this model has additional fields
according to the fee plan.

```python
fee = plisio.get_fee_plan(
    plisio.CryptoCurrency.ETH
)
```

### Operations

To view transactions, call:
1) <code>get_operation</code> to view a specific transaction by <code>id</code>;
2) <code>get_operations</code> to view all transactions.

In the first case, it returns a model <code>Operation</code>
for the required operation's id.
In the second case - model <code>Operations</code>,
which consists of operations list, links for current, first and last pages
and metadata about all your operations. The second case has several
optional variables:
+ <code>page</code> - page number;
+ <code>limit</code> - number of elements on the page;
+ <code>shop_id</code> - filter operation by shop;
+ <code>type_</code> - transaction type;
+ <code>status</code> - transaction status;
+ <code>currency</code> - name of the cryptocurrency;
+ <code>search</code> - text search by the transaction id (txid),
invoice's order number or customer email from invoice.

#### Operation

The <code>Operation</code> model has the next fields:
+ <code>user_id</code> - Profile ID;
+ <code>shop_id</code> - Shop ID;
+ <code>type_</code> - model <code>OperationType</code>
consisted **4** types: *cash_in*, *cash_out*, *mass_cash_out*, *invoice*;
+ <code>status</code> - model <code>OperationStatus</code>, described with **6**
statuses: *pending*, *completed*, *error*, *new*, *expired*, *mismatch*, *cancelled*;
+ <code>pending_sum</code> - unconfirmed amount (mempool);
+ <code>currency</code> - name of the cryptocurrency;
+ <code>source_currency</code> - fiat currency;
+ <code>source_rate</code> - exchange rate from the "cryptocurrency";
to the "source_currency" at the moment of transfer;
+ <code>fee</code> - transaction fee stated in the transfer;
+ <code>wallet_hash</code> - destination hash or invoice hash;
+ <code>sendmany</code> - pairs of hashes and values;
+ <code>params</code> - model <code>WithdrawParams</code>;
+ <code>expire_at_utc</code> - timestamp in UTC timezone; it may need to be divided by 1000;
+ <code>created_at_utc</code> - timestamp in the UTC timezone; it may need to be divided by 1000;
+ <code>amount</code> - amount received/transferred by an operation;
+ <code>sum_</code>:
  + *invoice*: params.amount + Plisio commission (if the customer pays the commission)
  or params.amount (if the merchant pays the commission);
  + *cash-out*: transfer amount + network fee;
  + *cash-in*: received amount.
+ <code>commission</code> - Plisio commission;
+ <code>tx_url</code> - link to the cryptocurrency block explorer;
+ <code>tx_id</code> - list of transaction ids;
+ <code>id_</code> - internal Plisio operation ID;
+ <code>actual_sum</code> - real incoming amount;
+ <code>actual_commission</code> - Plisio commission taken;
+ <code>actual_fee</code> - network fee (move invoice to wallet);
+ <code>actual_invoice_sum</code> - <code>actual_sum</code> -
<code>actual_commission_sum</code> - <code>actual_fee</code>;
+ <code>tx</code> - list of transactions details;
+ <code>status_code</code> - code of status.

#### WithdrawParams

There are **4** params:

+ <code>source_currency</code> - name of the cryptocurrency;
+ <code>source_rate</code> - exchange rate from the "cryptocurrency";
to the "source_currency" at the moment of transfer;
+ <code>usd_rate</code> - exchange rate from the "cryptocurrency";
to the **USD** at the moment of transfer;
+ <code>fee</code> - transaction fee stated in the transfer.


## Async usage

All these methods have their async analogues in **PlisioAioClient**.
They can be easily integrated into your async functions.

```python
import plisio
...

client = plisio.PlisioAioClient('your_secret_key')

currencies = await client.get_currencies(plisio.FiatCurrency.AUD)
```
