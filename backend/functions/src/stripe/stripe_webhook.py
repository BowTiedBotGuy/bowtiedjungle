import os
import json
import stripe
import psycopg2
import boto3
import psycopg2.extras
from botocore.exceptions import ClientError
from activation_code_message import html_mockup
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail


# Create a new SES client
# ses_client = boto3.client('ses')

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
    print(payload)
    print(payload['type'])
    if payload['type'] == 'checkout.session.completed':
        payload_object = payload['data']['object'] 
        session_id = payload_object['id']
        customer = payload_object['customer']
        retrieve_response = stripe.checkout.Session.retrieve(
        session_id,
        expand=['total_details.breakdown']
        )
        total_details = retrieve_response['total_details']['breakdown']
        discounts = total_details.get('discounts',[])
        discount = discounts[0]
        promo_code_id = discount['discount']['promotion_code']

        ## if there is already a connection you don't need to set it up
        metadata = payload_object['metadata']
        if 'account_id' in metadata:
            return {
                'statusCode': 200,
                'body': json.dumps('Done!')
            }
        try:
            with psycopg2.connect(
                host=host,
                database=database,
                user=user,
                password=password,
                port="5432",
                sslmode='require') as conn:

                with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
                    query = "SELECT account_id FROM sellers WHERE promo_code_id=%s"
                    cur.execute(query, (promo_code_id,))
                    result = cur.fetchone() or {}
                    account_id = result.get('account_id')
                    if account_id:
                        print('setting up connection')
                        stripe.Customer.modify(
                        customer,
                        metadata={"account_id": account_id},
                        )

                        insert_query = "INSERT INTO subscription_account_association (subscription_id, account_id) VALUES (%s, %s)"
                        subscription_id = retrieve_response['subscription']
                        cur.execute(insert_query, (subscription_id, account_id))
                        conn.commit()

                        amount_to_transfer = int(payload_object['amount_total'] * 0.30)
                        if amount_to_transfer > 0:
                            # Create a transfer to the connected account
                            print('transfering to account')
                            stripe.Transfer.create(
                                amount=amount_to_transfer,
                                currency=payload_object['currency'],
                                destination=account_id,
                                transfer_group=payload_object['invoice'],
                            )

        
        except (Exception,psycopg2.DatabaseError) as error:
            print(error)
    
    if payload['type'] == 'invoice.payment_succeeded':
        payload_object = payload['data']['object'] 
        invoice_id = payload_object['id']

        try:
            # Retrieve the invoice
            invoice = stripe.Invoice.retrieve(invoice_id)
            subscription_id = invoice.get('subscription')

            if subscription_id:
                # Database operation to find associated account
                with psycopg2.connect(
                    host=host,
                    database=database,
                    user=user,
                    password=password,
                    port="5432",
                    sslmode='require') as conn:

                    with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
                        # Query to find the associated account for this subscription
                        query = "SELECT account_id FROM subscription_account_association WHERE subscription_id=%s"
                        cur.execute(query, (subscription_id,))
                        result = cur.fetchone()

                        if result:
                            account_id = result.get('account_id')
                            if invoice['billing_reason'] == 'subscription_cycle':
                                # Check if this is the payment after the start
                                # Calculate 20% of the payment
                                amount_to_transfer = int(invoice['amount_paid'] * 0.30)
                                if amount_to_transfer > 0:
                                    # Create a transfer to the connected account
                                    print('transfering to account')
                                    stripe.Transfer.create(
                                        amount=amount_to_transfer,
                                        currency=invoice['currency'],
                                        destination=account_id,
                                        transfer_group=invoice_id,
                                    )
        except Exception as e:
            print(f"Error: {e}")

        

        
    if payload['type'] == 'customer.created':
        session = payload['data']['object']
        customer_email = session['email']
        customer_name = session['name']
        stripe_customer = session['id']
        
        # Generate an activation code
        activation_code = os.urandom(16).hex()
        # Store this activation code and email in your database.
        # TODO implement SQL
        try:
            with psycopg2.connect(
                host=host,
                database=database,
                user=user,
                password=password,
                port="5432",
                sslmode='require') as conn:

                with conn.cursor() as cur:
                    query = "INSERT INTO ActivationCodes (Email, Code, Customer_ID) VALUES (%s, %s, %s)"
                    params = (customer_email, activation_code, stripe_customer)
                    cur.execute(query, params)
                    conn.commit()
                    print('com')


        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

        # try:
        #     send_email(recipient_email=customer_email,activation_code=activation_code,customer_name=customer_name)
        # except Exception as e:
        #     raise e

    if payload['type'] == 'customer.subscription.deleted':
        stripe_customer = payload['data']['object']['customer']

        try:
            with psycopg2.connect(
                host=host,
                database=database,
                user=user,
                password=password,
                port="5432",
                sslmode='require') as conn:

                with conn.cursor() as cur:
                    # First, query the activated_codes table to get the email and activation code
                    query = "SELECT code FROM ActivationCodes WHERE customer_id = %s"
                    params = (stripe_customer,)
                    cur.execute(query, params)
                    activation_code = cur.fetchone()
                    if activation_code:

                        # Delete from activated_codes based on customer_id
                        query = "DELETE FROM ActivationCodes WHERE customer_id = %s"
                        params = (stripe_customer,)
                        cur.execute(query, params)

                        # Delete from activated_users based on the fetched email or activation code
                        query = "DELETE FROM ActivatedUsers WHERE customer_id = %s"
                        params = (activation_code,)
                        cur.execute(query, params)

                        conn.commit()

        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        
    return {
        'statusCode': 200,
        'body': json.dumps('Done!')
    }


# def send_email(recipient_email,activation_code,customer_name):
#     sender_email = "noreply@bowtiedlist.com"
#     subject = "Your Activation Code"
#     body_html = html_mockup(activation_code=activation_code,customer_name=customer_name)

#     # Define the email parameters
#     message = Mail(
#     from_email=sender_email,
#     to_emails=recipient_email,
#     subject=subject,
#     html_content=body_html)
#     try:
#         sg = SendGridAPIClient(os.environ.get('send_grid_key'))
#         response = sg.send(message)
#         print(response.status_code)
#         print(response.body)
#         print(response.headers)
#     except Exception as e:
#         print(e.message)
    # # Construct the email content
    # email_content = {
    #     'Subject': {
    #         'Data': subject
    #     },
    #     'Body': {
    #         'Text': {
    #             'Data': body_text
    #         },
    #         'Html': {
    #             'Data': body_html
    #         }
    #     }
    # }

    # # Send the email
    # try:
    #     response = ses_client.send_email(
    #         Source=sender_email,
    #         Destination={
    #             'ToAddresses': [recipient_email]
    #         },
    #         Message=email_content
    #     )
    #     print("Email sent! Message ID:", response['MessageId'])
    # except ClientError as e:
    #     print("Error sending email:", e.response['Error']['Message'])
