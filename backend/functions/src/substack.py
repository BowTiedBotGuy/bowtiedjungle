import feedparser
import pandas as pd

rawrss = ['https://bowtiedbull.substack.com/feed', 'https://bowtiedox.substack.com/feed']

posts = []

# dict_keys(['bozo', 'entries', 'feed', 'headers', 'etag', 'href', 'status', 'encoding', 'version', 'namespaces'])
for url in rawrss:
    feed = feedparser.parse(url)
    print(feed.feed)
    for post in feed.entries:
        posts.append((post.title, post.link, post.summary, post.summary_detail, post.content, post.published))
df = pd.DataFrame(posts, columns=['title', 'link', 'summary', 'summary_detail', 'content', 'published'])
print(df)