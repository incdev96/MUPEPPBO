from celery import shared_task
import requests
from .models import Mutualist, Sms, SmsDetails
import time


def generate_api_token():
    api_token_url = "https://api.orange.com/oauth/v3/token"
    headers = {
        "Authorization": "Basic Zk9jVDdoaUpaOURyb1pwZ3k0R2Q5RlA3amMxQUh0dkQ6M0p4a3dyNDNoc3NobXlMMQ==",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    payload = {
        "grant_type":"client_credentials"
    }
    rq = requests.post(url=api_token_url, data=payload, headers=headers)
    api_token =  rq["access_token"]
    return api_token


@shared_task()
def send_mass_sms_task(phone_numbers, message):
    access_token = generate_api_token()
    api_url = "https://api.orange.com/smsmessaging/v1/outbound/tel%3A%2B0707830932/requests"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json" 
    }
    for phone_number in phone_numbers:
        payload = {
            "outboundSMSMessageRequest": {
            "address": f"tel:+{phone_number}",
            "senderAddress":"tel:+0707830932",
            "senderName": "MUPEPPBO",
            "outboundSMSTextMessage": {
                "message": message
                }
            }

        }
        rq = requests.post(url=api_url, json=payload, headers=headers)
        time.sleep(0.2)
    