import feedparser
from lambda_decorators import json_http_resp, cors_headers, load_json_body

@cors_headers
@load_json_body
@json_http_resp
def lambda_handler(event,context):
    rawrss = ['https://bowtiedbull.substack.com/feed']

    posts = []
    try:
        # dict_keys(['bozo', 'entries', 'feed', 'headers', 'etag', 'href', 'status', 'encoding', 'version', 'namespaces'])
        for url in rawrss:
            feed = feedparser.parse(url)
            for post in feed.entries:
                posts.append({'id':post.id,'title': post.title, 'link': post.link, 'summary': post.summary, 'detail': post.summary_detail, 'published': post.published})
        
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
    lambda_handler({},{})
