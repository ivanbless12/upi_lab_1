# Variant: 21
# Task: 16

import argparse
import requests

def create_parser():
    param = argparse.ArgumentParser()
    param.add_argument(
                    "-er",
                    "--exchange_rate",
                    type=float,
                    help="Set currency exchange rate manually. It will be rounded to 2 digits after the dot. Format: USD/RUB (Example: 98.65)."
    )
    param.add_argument(
                    "-et",
                    "--exchange_type",
                    choices=['RUB/USD', 'USD/RUB'],
                    required=True,
                    help="Set currency exchange type. Required parameter. Choices: 'RUB/USD', 'USD/RUB'."
    )
    param.add_argument(
                    "-am",
                    "--amount",
                    type=float,
                    default=1000.0,
                    help="Set amount need to exchange. It will be rounded to 2 digits after the dot. Default: 1000.0."
    )
    return param

def get_currency_exchange_rate():
    url = "https://api.exchangerate.host/latest?base=USD&symbols=RUB&places=2"
    try:
        response = requests.get(url)
        data = response.json()
        currency_exchange_rate = float(list(data['rates'].values())[0])
        return currency_exchange_rate
    except Exception as e:
        print(f"An error occurred while accessing the API server. You can restart the program by setting the currency rate manually (flag '-er').\nError: {e}")
        exit(1)

def get_exchange(amount, exchange_type, exchange_rate):
    int_amount = int(amount*100)
    int_exchange_rate = int(exchange_rate*100)
    if exchange_type == "USD/RUB":
        int_result = int(int_amount * int_exchange_rate/100)
    else:
        int_result = int(int_amount / int_exchange_rate*100)
    float_result = int_result / 100
    return float_result

if __name__ == '__main__':
    parser = create_parser()
    params = parser.parse_args()
    if params.exchange_rate is None:
        currency_exchange_rate = get_currency_exchange_rate()
    else:
        currency_exchange_rate = round(params.exchange_rate, 2)
    result = get_exchange(round(params.amount,2), params.exchange_type, currency_exchange_rate)
    print(f"\nExchange rate: {currency_exchange_rate} (RUB/USD)\nExchange type: {params.exchange_type}\nAmount to exchange: {params.amount}\n\nResult: {result} {params.exchange_type.split('/')[1]}")