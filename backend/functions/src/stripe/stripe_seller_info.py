import psycopg2
import psycopg2.extras
from lambda_decorators import json_http_resp, cors_headers , load_json_body
import os

@cors_headers
@load_json_body
@json_http_resp
def lambda_handler(event, context):
    # TODO implement
    print(event)
    user = os.environ.get('db_username')
    host = os.environ.get('db_host')
    password = os.environ.get('db_password')
    database = os.environ.get('db_database')
    
    cognito_id=event['requestContext']['authorizer']['claims']['sub']
    result = {}
    try:
        with psycopg2.connect(
            host=host,
            database=database,
            user=user,
            password=password,
            port="5432",
            sslmode='require') as conn:

            with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
                query = "SELECT account_id, charges_enabled, price_urls,promo_code FROM sellers WHERE cognito_id=%s"
                cur.execute(query, (cognito_id,))
                result = cur.fetchone() or {}

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    
    return result