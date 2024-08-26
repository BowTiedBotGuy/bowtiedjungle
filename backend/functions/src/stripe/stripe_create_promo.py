import stripe
import os
import psycopg2
from lambda_decorators import json_http_resp, cors_headers, load_json_body

stripe.api_key = os.environ.get('stripe_secret_key')
user = os.environ.get('db_username')
host = os.environ.get('db_host')
password = os.environ.get('db_password')
database = os.environ.get('db_database')
stripe_coupon = os.environ.get('stripe_coupon')

@cors_headers
@load_json_body
@json_http_resp
def lambda_handler(event,context):
    print(event)
    promo_code = event['body']['promo_code']
    account_id = event['body']['account_id']
    cognito_id=event['requestContext']['authorizer']['claims']['sub']
    try:
        data = stripe.PromotionCode.create(
        coupon=stripe_coupon,
        code=promo_code,
        )
        with psycopg2.connect(
            host=host,
            database=database,
            user=user,
            password=password,
            port="5432",
            sslmode='require') as conn:

            with conn.cursor() as cur:
                query = """
                UPDATE sellers SET promo_code_id = %s , promo_code = %s
                WHERE account_id = %s AND cognito_id = %s;
                """
                params = (data['id'], promo_code,account_id, cognito_id,)
                cur.execute(query, params)
                conn.commit()
                print('com')
        return data
    except stripe.error.StripeError as e:
        # Handle Stripe errors
        return {
            'statusCode': 400,
            'body': {
                'error': str(e)
            }
        }
