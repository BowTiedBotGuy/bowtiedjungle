import stripe
import os
from lambda_decorators import json_http_resp, cors_headers, load_json_body

stage = os.environ.get('stage')
stripe.api_key = os.environ.get('stripe_secret_key')

@cors_headers
@load_json_body
@json_http_resp
def lambda_handler(event,context):
    print(event)
    cognito_id=event['requestContext']['authorizer']['claims']['sub']
    try:
        account = stripe.Account.create(type="express",metadata={'cognito_id': cognito_id})
        account_id = account['id']
        domain_starter = 'app' if stage == 'prd' else 'dev'
        url = f'https://{domain_starter}.bowtiedlist.com'  

        account_link = stripe.AccountLink.create(
        account=account_id,
        refresh_url=f"{url}/refresh",
        return_url=f"{url}/sellers",
        type="account_onboarding",
        )

        return {'url': account_link['url']}
    except stripe.error.StripeError as e:
        # Handle Stripe errors
        return {
            'statusCode': 400,
            'body': {
                'error': str(e)
            }
        }

