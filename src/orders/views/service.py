from dataclasses import dataclass
import stripe
from myproject.settings import STRIPE_SECRET_KEY
stripe.api_key = STRIPE_SECRET_KEY
import requests
import json
import base64
url = "https://api.sandbox.paypal.com/v1/oauth2/token"
clientID = 'AQ6oVBBo02Ft5CaQe9l27BjayUxJHf0vCS2YpAmbvNekU3oI0qeBwVr77c_MkVI65XZYu-TUM5D0aFSs'
clientSecret = 'EDy82omyxEjTm-EsIxRaE31qt7qvlauWEwOqVp9Cm8zG8Dg94ifNzps2swx7QMexl16N14QnhVKv16lp'

@dataclass
class PaymentProcess:
    order_id: int
    net_price: int
    payment_type: str
    payment_id: int
    customer_id: int

    def __call__(self) -> dict:
        data = {}
        if self.payment_type == "stripe":
            checkout_session = stripe.checkout.Session.create(
                line_items=[
                        {
                            'name': 'Medicine',
                            'quantity': 2,
                            'currency': 'usd',
                            'amount': self.net_price*100,
                        },
                        {
                            'name': 'Medicine 2',
                            'quantity': 5,
                            'currency': 'usd',
                            'amount': self.net_price*100,
                        }
                ],
                client_reference_id=self.customer_id,
                metadata={'order_id': self.order_id, 'payment_id': self.payment_id, 'customer_id': self.customer_id},
                mode='payment',
                success_url= 'https://facebook.com',
                cancel_url= 'https://facebook.com/sabbir1021',
            )
            data["url"] = checkout_session.url

        if self.payment_type == "paypal":
            data = {
                    "client_id": "AQ6oVBBo02Ft5CaQe9l27BjayUxJHf0vCS2YpAmbvNekU3oI0qeBwVr77c_MkVI65XZYu-TUM5D0aFSs",
                    "client_secret": "EDy82omyxEjTm-EsIxRaE31qt7qvlauWEwOqVp9Cm8zG8Dg94ifNzps2swx7QMexl16N14QnhVKv16lp",
                    "grant_type":"client_credentials"
                }
            headers = {
                    "Content-Type": "application/x-www-form-urlencoded",
                    "Authorization": "Basic {0}".format(base64.b64encode(("AQ6oVBBo02Ft5CaQe9l27BjayUxJHf0vCS2YpAmbvNekU3oI0qeBwVr77c_MkVI65XZYu-TUM5D0aFSs" + ":" + "EDy82omyxEjTm-EsIxRaE31qt7qvlauWEwOqVp9Cm8zG8Dg94ifNzps2swx7QMexl16N14QnhVKv16lp").encode()).decode())
                }
            token = requests.post(url, data, headers=headers)
            
            token = token.json()['access_token']
            print(token)
            headers = {
                'Content-Type': 'application/json',
                'Authorization': 'Bearer '+token,
            }
            json_data = {
                "intent": "CAPTURE",
                "application_context": {
                    "notify_url": "http://127.0.0.1:8000/api/v1.0/payments/user/status/",
                    "return_url": "http://127.0.0.1:8000/api/v1.0/payments/user/status/",#change to your doma$
                    "cancel_url": "http://127.0.0.1:8000/", #change to your domain
                    "brand_name": "PESAPEDIA SANDBOX",
                    "landing_page": "BILLING",
                    "shipping_preference": "NO_SHIPPING",
                    "user_action": "CONTINUE"
                },
                "purchase_units": [
                    {
                        "reference_id": "294375635",
                        "description": "African Art and Collectibles",

                        "custom_id": self.payment_id,
                        "soft_descriptor": "AfricanFashions",
                        "amount": {
                            "currency_code": "USD",
                            "value": "200" #amount,
                        },
                    }
                ]
            }
            response = requests.post('https://api-m.sandbox.paypal.com/v2/checkout/orders', headers=headers, json=json_data)
            order_id = response.json()['id']
            linkForPayment = response.json()['links'][1]['href']
            data["url"] = linkForPayment
        return data