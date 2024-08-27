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
        result = session.execute(text("SELECT DISTINCT substack FROM bowtiedlist WHERE substack IS NOT NULL"))
        urls = [url[0] for url in result.fetchall()]
        return urls
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
    
    # Create the database engine
    engine = create_engine(f"postgresql://{user}:{password}@{host}/{database}", echo=True)
    
    # Create a configured "Session" class
    session_factory = scoped_session(sessionmaker(bind=engine))
    
    # Fetch URLs using the session factory
    urls = fetch_data(session_factory=session_factory)
    session_factory.remove()  # Correct usage of remove to clear any residual session after use

    rawrss = [url + '/feed' for url in urls]

    posts = []
    try:
        # dict_keys(['bozo', 'entries', 'feed', 'headers', 'etag', 'href', 'status', 'encoding', 'version', 'namespaces'])
        for url in rawrss:
            feed = feedparser.parse(url)
            feed_info = feed.feed
            name = feed_info.title
            # Extract the image URL
            if 'image' in feed_info and 'href' in feed_info['image']:
                image_url = feed_info['image']['href']
            for post in feed.entries:
                posts.append({'name':name,'image_url':image_url,'id':post.id,'title': post.title, 'link': post.link, 'summary': post.summary, 'detail': post.summary_detail, 'published': post.published})
        
        return {
                'statusCode': 200,
                'data': posts
            }
    except Exception as e:
        # An error occurred during processing
        return {
            'statusCode': 500,
            'error': str(e)
        }


if __name__ == '__main__':
    data = lambda_handler({},{})
    print(data)
