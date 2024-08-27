import stripe
import os
from lambda_decorators import json_http_resp, cors_headers

stripe.api_key = os.environ.get('stripe_secret_key')
product_id = os.environ.get('stripe_product_id')

@cors_headers
@json_http_resp
def lambda_handler(event,context):
    print(event)
    try:
        data = stripe.Price.list(type='recurring',product=product_id,active=True)
        return data
    except stripe.error.StripeError as e:
        # Handle Stripe errors
        return {
            'statusCode': 400,
            'body': {
                'error': str(e)
            }
        }
