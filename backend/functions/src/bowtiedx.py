import requests
import pandas as pd
import json
from datetime import datetime
import os
from dotenv import load_dotenv


class BowTiedTwitter:
    def __init__(self) -> None:
        load_dotenv()
        self.search_url = "https://x.com/i/api/graphql/UN1i3zUiCWa-6r-Uaho4fw/SearchTimeline?variables=%7B%22rawQuery%22%3A%22bowtied%22%2C%22count%22%3A20%2C%22querySource%22%3A%22typeahead_click%22%2C%22product%22%3A%22People%22%7D&features=%7B%22rweb_tipjar_consumption_enabled%22%3Atrue%2C%22responsive_web_graphql_exclude_directive_enabled%22%3Atrue%2C%22verified_phone_label_enabled%22%3Afalse%2C%22creator_subscriptions_tweet_preview_api_enabled%22%3Atrue%2C%22responsive_web_graphql_timeline_navigation_enabled%22%3Atrue%2C%22responsive_web_graphql_skip_user_profile_image_extensions_enabled%22%3Afalse%2C%22communities_web_enable_tweet_community_results_fetch%22%3Atrue%2C%22c9s_tweet_anatomy_moderator_badge_enabled%22%3Atrue%2C%22articles_preview_enabled%22%3Atrue%2C%22responsive_web_edit_tweet_api_enabled%22%3Atrue%2C%22graphql_is_translatable_rweb_tweet_is_translatable_enabled%22%3Atrue%2C%22view_counts_everywhere_api_enabled%22%3Atrue%2C%22longform_notetweets_consumption_enabled%22%3Atrue%2C%22responsive_web_twitter_article_tweet_consumption_enabled%22%3Atrue%2C%22tweet_awards_web_tipping_enabled%22%3Afalse%2C%22creator_subscriptions_quote_tweet_preview_enabled%22%3Afalse%2C%22freedom_of_speech_not_reach_fetch_enabled%22%3Atrue%2C%22standardized_nudges_misinfo%22%3Atrue%2C%22tweet_with_visibility_results_prefer_gql_limited_actions_policy_enabled%22%3Atrue%2C%22rweb_video_timestamps_enabled%22%3Atrue%2C%22longform_notetweets_rich_text_read_enabled%22%3Atrue%2C%22longform_notetweets_inline_media_enabled%22%3Atrue%2C%22responsive_web_enhance_cards_enabled%22%3Afalse%7D"
        self.payload = {}
        self.headers = {
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.9',
        'authorization': os.getenv('x_bearer_token'),
        'content-type': 'application/json',
        'cookie': os.getenv('x_cookie'),
        'priority': 'u=1, i',
        'referer': 'https://x.com/search?q=bowtied&src=typeahead_click&f=user',
        'sec-ch-ua': '"Not)A;Brand";v="99", "Google Chrome";v="127", "Chromium";v="127"',
        'sec-ch-ua-mobile': '?1',
        'sec-ch-ua-platform': '"Android"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Mobile Safari/537.36',
        'x-client-transaction-id': os.getenv('x_transaction_id'),
        'x-csrf-token': os.getenv('x_csrf_token'),
        'x-twitter-active-user': 'yes',
        'x-twitter-auth-type': 'OAuth2Session',
        'x-twitter-client-language': 'en'
        }

    def search_bowtied(self):
        res = requests.request("GET", self.search_url, headers=self.headers, data=self.payload)
        res_json = res.json()
        parse_res = self.parse_search(res_json)
        return parse_res
    
    def parse_search(self,data):
        info = []
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        # Extract all users mentioned in the timeline
        for entry in data['data']['search_by_raw_query']['search_timeline']['timeline']['instructions'][1]['entries']:
            if 'itemContent' in entry['content']:
                user_info = entry['content']['itemContent']['user_results']['result']['legacy']
                user_data = {
                    'name': user_info['name'],
                    'description': user_info['description'],
                    'followers_count': user_info['followers_count'],
                    'created_at': user_info['created_at'],
                    'screen_name': user_info['screen_name'],
                    'timestamp': timestamp,
                }
                info.append(user_data)

        df = pd.DataFrame(info)
        df_sorted = df.sort_values(by='followers_count', ascending=False)
        return df_sorted



if __name__ == '__main__':
    twitter_client = BowTiedTwitter()
    search_res = twitter_client.search_bowtied()
    print(search_res)


