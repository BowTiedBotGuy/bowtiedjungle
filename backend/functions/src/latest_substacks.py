import feedparser
from lambda_decorators import json_http_resp, cors_headers, load_json_body

@cors_headers
@load_json_body
@json_http_resp
def lambda_handler(event,context):
    rawrss = ['https://bowtiedbull.substack.com/feed']

    posts = []

    # dict_keys(['bozo', 'entries', 'feed', 'headers', 'etag', 'href', 'status', 'encoding', 'version', 'namespaces'])
    for url in rawrss:
        feed = feedparser.parse(url)
        for post in feed.entries:
            posts.append((post.title, post.link, post.summary, post.summary_detail, post.content, post.published))

    
    return posts

