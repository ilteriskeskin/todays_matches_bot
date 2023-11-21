import requests
import src.configs as configs

from requests_oauthlib import OAuth1

# X/Twitter API keys
consumer_key = configs.X_CONSUMER_KEY
consumer_secret = configs.X_CONSUMER_SECRET
access_token = configs.X_ACCESS_TOKEN
access_token_secret = configs.X_ACCESS_TOKEN_SECRET
X_BEARER_TOKEN = configs.X_BEARER_TOKEN


def tweet(tweet_text: str = ""):
    try:
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {X_BEARER_TOKEN}'
        }

        auth = OAuth1(consumer_key, consumer_secret, access_token, access_token_secret)
        tweet_url = 'https://api.twitter.com/2/tweets'
        response = requests.post(
            tweet_url,
            json={
                'text': tweet_text
            },
            headers=headers,
            auth=auth
        )

        if response.status_code == 201:
            print("Tweet successfully")
        else:
            print(f"Failed: {response.text}")

    except Exception as e:
        print("Error: ", e)
