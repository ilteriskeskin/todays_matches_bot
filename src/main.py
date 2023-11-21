import configs
import requests

from datetime import datetime
from test_data import TEST_RESPONSE_DATA
from utils import tweet


def run():
    today = datetime.now()
    today_str = today.strftime("%Y-%m-%d")
    api_key = configs.FOOTBALL_DATA_API_KEY
    api_uri = f"{configs.FOOTBALL_DATA_API_URL}from={today_str}&to={today_str}&APIkey={api_key}"

    response = requests.get(api_uri, headers=configs.HEADERS)

    if response.status_code == 200:
        matches_data = response.json()

        if not matches_data:
            matches_data = TEST_RESPONSE_DATA

        for match in matches_data:
            tweet_text = f"{match['match_hometeam_name']} vs {match['match_awayteam_name']} - {match['match_time']}"
            tweet.tweet(tweet_text=tweet_text)

    else:
        print(f'Hata: {response.status_code}')


if __name__ == '__main__':
    run()
