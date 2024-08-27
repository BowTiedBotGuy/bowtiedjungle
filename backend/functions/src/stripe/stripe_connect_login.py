import stripe
import os
from lambda_decorators import json_http_resp, cors_headers, load_json_body

stripe.api_key = os.environ.get('stripe_secret_key')

@cors_headers
@load_json_body
@json_http_resp
def lambda_handler(event,context):
    print(event)
    account_id = event['body']['account_id']
    try:
        login_response = stripe.Account.create_login_link(
        account_id,
        )
        return {'url': login_response['url']}
    except stripe.error.StripeError as e:
        # Handle Stripe errors
        return {
            'statusCode': 400,
            'body': {
                'error': str(e)
            }
        }
