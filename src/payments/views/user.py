from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.http.response import HttpResponse
import stripe
from myproject.settings import STRIPE_SECRET_KEY, STRIPE_WEBHOOK_SECRET_KEY
stripe.api_key = STRIPE_SECRET_KEY
from payments.models import Payment
from rest_framework.permissions import AllowAny
import requests
import base64
from django.shortcuts import redirect

@csrf_exempt
def stripe_webhook(request):
    endpoint_secret = STRIPE_WEBHOOK_SECRET_KEY
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)

    # Handle the checkout.session.completed event
    if event['type'] == 'checkout.session.completed':
        payment_id = event['data']['object']['metadata']['payment_id']
        payment = Payment.objects.filter(id=payment_id).first()
        payment.transaction_number = event['data']['object']['payment_intent']
        payment.payment_status = 'paid'
        payment.save()
    return HttpResponse(status=200)


@method_decorator(csrf_exempt, name='dispatch')
class Status(APIView):
    permission_classes = (AllowAny,)
    
    def get(self, request, *args, **kwargs):
        data = {
                "client_id": "AQ6oVBBo02Ft5CaQe9l27BjayUxJHf0vCS2YpAmbvNekU3oI0qeBwVr77c_MkVI65XZYu-TUM5D0aFSs",
                "client_secret": "EDy82omyxEjTm-EsIxRaE31qt7qvlauWEwOqVp9Cm8zG8Dg94ifNzps2swx7QMexl16N14QnhVKv16lp",
                "grant_type":"client_credentials"
            }
        headers = {
                "Content-Type": "application/x-www-form-urlencoded",
                "Authorization": "Basic {0}".format(base64.b64encode(("AQ6oVBBo02Ft5CaQe9l27BjayUxJHf0vCS2YpAmbvNekU3oI0qeBwVr77c_MkVI65XZYu-TUM5D0aFSs" + ":" + "EDy82omyxEjTm-EsIxRaE31qt7qvlauWEwOqVp9Cm8zG8Dg94ifNzps2swx7QMexl16N14QnhVKv16lp").encode()).decode())
            }
        token = requests.post('https://api.sandbox.paypal.com/v1/oauth2/token', data, headers=headers)
        token = token.json()['access_token']
        payment_token = request.GET.get('token')
        captureurl = f'https://api.sandbox.paypal.com/v2/checkout/orders/{payment_token}/capture'
        headers = {"Content-Type": "application/json", "Authorization": "Bearer "+token}
        response = requests.post(captureurl, headers=headers)
        response = response.json()

        if response.get('status') == 'COMPLETED':
            terns = response.get('purchase_units')[0].get('payments').get('captures')[0].get('id')
            payment_id = response.get('purchase_units')[0].get('payments').get('captures')[0].get('custom_id')
            payment = Payment.objects.filter(id=payment_id).first()
            payment.transaction_number = terns
            payment.payment_status = 'paid'
            payment.save()
            return redirect('https://www.google.com/')