import os
import json
import stripe
import psycopg2

user = os.environ.get('db_username')
host = os.environ.get('db_host')
password = os.environ.get('db_password')
database = os.environ.get('db_database')


stripe.api_key = os.environ.get('stripe_secret_key')
endpoint_secret = os.environ.get('stripe_webhook_key')

# ---------------- Stripe Webhook Setup ----------------
def lambda_handler(event,context):
    payload = event['body']
    sig_header = event['headers']['Stripe-Signature']
    
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        # Invalid payload
        raise e
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        raise e
    
    payload = json.loads(payload)
        
    if payload['type'] == 'account.updated':
        user_pool_id = os.environ.get('user_pool_id')  # Set your User Pool ID as an env variable
        account = payload['data']['object']
        cognito_id = account['metadata']['cognito_id']
        account_id = account['id']
        charges_enabled = account['charges_enabled']

        try:
            with psycopg2.connect(
                host=host,
                database=database,
                user=user,
                password=password,
                port="5432",
                sslmode='require') as conn:

                with conn.cursor() as cur:
                    query = """INSERT INTO sellers (account_id, cognito_id, user_pool_id,charges_enabled) VALUES (%s, %s, %s,%s)
                    ON CONFLICT (cognito_id) DO UPDATE SET
                    account_id = EXCLUDED.account_id,
                    user_pool_id = EXCLUDED.user_pool_id,
                    charges_enabled = EXCLUDED.charges_enabled
                    """
                    params = (account_id, cognito_id, user_pool_id,charges_enabled)
                    cur.execute(query, params)
                    conn.commit()
                    print('com')

        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        
    return {
        'statusCode': 200,
        'body': json.dumps('Done!')
    }