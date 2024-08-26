import stripe
import os
from lambda_decorators import json_http_resp, cors_headers, load_json_body
import psycopg2

stripe.api_key = os.environ.get('stripe_secret_key')

@cors_headers
@load_json_body
@json_http_resp
def lambda_handler(event,context):
    print(event)
    cognito_id=event['requestContext']['authorizer']['claims']['sub']
    account_id = event['body']['account_id']
    price_id = event['body']['price_id']
    user = os.environ.get('db_username')
    host = os.environ.get('db_host')
    password = os.environ.get('db_password')
    database = os.environ.get('db_database')
    try:
        # TODO get the unit amount of the price id and calculate comission
        data = stripe.PaymentLink.create(
            line_items=[
                {
                "price": price_id,
                "quantity": 1,
                },
            ],
            metadata={"account_id" : account_id},
            automatic_tax={
                "enabled": True
            },
            allow_promotion_codes=True,
            transfer_data={
                "destination":account_id,
            },
            application_fee_percent=70
            )
        
        payment_url = data['url']
        json_path = [price_id]
        with psycopg2.connect(
            host=host,
            database=database,
            user=user,
            password=password,
            port="5432",
            sslmode='require') as conn:

            with conn.cursor() as cur:
                query = """
                UPDATE sellers SET price_urls = jsonb_set(
                    coalesce(price_urls, '{}')::jsonb,
                    %s::text[],
                    to_jsonb(%s::text),
                    true
                )
                WHERE account_id = %s AND cognito_id = %s;
                """
                # The path to set the value in the JSON object
                
                
                params = (json_path, payment_url, account_id, cognito_id)
                cur.execute(query, params)
                conn.commit()
                print('com')
        # Update seller user
        
        return payment_url
    except stripe.error.StripeError as e:
        # Handle Stripe errors
        return {
            'statusCode': 400,
            'body': {
                'error': str(e)
            }
        }
