import feedparser
import os
from lambda_decorators import json_http_resp, cors_headers, load_json_body
from sqlalchemy import create_engine,text
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from dotenv import load_dotenv

def fetch_data(session_factory):
    # Directly use the session factory to control the session lifecycle
    session = session_factory()
    try:
        result = session.execute(text("SELECT * FROM bowtiedlist"))
        results = result.fetchall()

        # Get column headers
        headers = result.keys()

        # Convert results to a list of dictionaries
        data = [dict(zip(headers, row)) for row in results]
        return data
    except SQLAlchemyError as e:
        print(f"Error fetching Substack URLs: {str(e)}")
        return []
    finally:
        session.close()  # Properly close the session


@cors_headers
@load_json_body
@json_http_resp
def lambda_handler(event,context):
    load_dotenv()
    # Retrieve database credentials and AWS S3 credentials from environment variables
    user = os.getenv('db_username')
    host = os.getenv('db_host')
    password = os.getenv('db_password')
    database = os.getenv('db_database')
    try:
        # Create the database engine
        engine = create_engine(f"postgresql://{user}:{password}@{host}/{database}", echo=True)
        
        # Create a configured "Session" class
        session_factory = scoped_session(sessionmaker(bind=engine))
        
        # Fetch URLs using the session factory
        bowtiedlist = fetch_data(session_factory=session_factory)
        session_factory.remove()  # Correct usage of remove to clear any residual session after use
        
        
        return {
                'statusCode': 200,
                'data': bowtiedlist
            }
    except Exception as e:
        # An error occurred during processing
        return {
            'statusCode': 500,
            'error': str(e)
        }


if __name__ == '__main__':
    data = lambda_handler({},{})
    print(data['body'])
