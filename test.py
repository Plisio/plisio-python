

import plisio

client = plisio.PlisioClient(api_key='aLU30JL9c1yeLp-XF7rsjoigB9SjIR9WaGDMcj8YImRPIsPDYVqyEz_4LMkapuFx')

# balance = client.get_operation('64d1df01224bd682be0c12c4')
second_invoice = client.create_invoice(
    plisio.CryptoCurrency.TRX,
    'TRXX6',
    20230903182401,
    allowed_currencies=[plisio.CryptoCurrency.TRX,plisio.CryptoCurrency.USDT_TRX],
    source_currency=plisio.FiatCurrency.USD,
    source_amount=10.1,
    callback_url='http://127.0.0.1:8000/call-back-url/1',
)

print(second_invoice)