import requests
import json
import smtplib
import os
from dotenv import load_dotenv, dotenv_values

load_dotenv()

MY_EMAIL = os.getenv("MY_SECRET_EMAIL")
MY_PASSWORD = os.getenv("MY_SECRET_EMAIL_PASSWORD")
CURRENCY_ENDPOINT = os.getenv("ENDPOINT_URL")
CURRENCY_API_KEY = os.environ.get('CURRENCY_KEY')

headers = {
    'apikey': CURRENCY_API_KEY
}

response = requests.request('GET', CURRENCY_ENDPOINT, headers=headers)
resp_text = response.text
dict=json.loads(resp_text)
GBP = float(dict['data']['GBP']['value'])
EUR = float(dict['data']['EUR']['value'])
USD = float(dict['data']['USD']['value'])
last_update = dict['meta']['last_updated_at'][:10]

GBP_change = round(1/GBP)
EUR_change = round(1/EUR)
USD_change = round(1/USD)


def GBP_send_email():
    with smtplib.SMTP("smtp.gmail.com") as connection:
            connection.starttls()
            connection.login(user=MY_EMAIL, password=MY_PASSWORD)
            connection.sendmail(
                from_addr=MY_EMAIL,
                to_addrs="norbert.nagy.1994@gmail.com",
                msg=f"Subject:GBP central rate alert!\n\nGBP's central rate just droped below 435HUF, as it is {GBP_change}HUF now.\nLet's buy some!\n\nLast update: {last_update}")

def send_email():
    with smtplib.SMTP("smtp.gmail.com") as connection:
            connection.starttls()
            connection.login(user=MY_EMAIL, password=MY_PASSWORD)
            connection.sendmail(
                from_addr=MY_EMAIL,
                to_addrs="norbert.nagy.1994@gmail.com",
                msg=f"Subject:GBP, EUR and USD central rate\n\nGBP's central rate is: {GBP_change}HUF.\nEUR's central rate is: {EUR_change}HUF.\nUSD's central rate is: {USD_change}HUF.\n\nLast update: {last_update}")

if GBP_change <= 435:
    GBP_send_email()
else:
    send_email()



print(last_update)


