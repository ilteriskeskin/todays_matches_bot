import configs
import requests

from datetime import datetime, timedelta
from test_data import TEST_RESPONSE_DATA
from flask import Flask, jsonify, request

app = Flask(__name__)
app.secret_key = configs.SECRET_KEY


def set_date():
    start_date = datetime.now().strftime("%Y-%m-%d")
    start_date_obj = datetime.strptime(start_date, "%Y-%m-%d")
    end_date_obj = start_date_obj + timedelta(days=30)
    end_date = end_date_obj.strftime("%Y-%m-%d")

    return start_date, end_date


def get_todays_matches(competition_id: str) -> dict:
    start_date, end_date = set_date()

    api_url = configs.FOOTBALL_DATA_API_URL
    api_uri = f"{api_url}{competition_id}/matches?dateFrom={start_date}&dateTo={end_date}&status=SCHEDULED"

    response = requests.get(api_uri, headers=configs.HEADERS)

    if response.status_code == 200:
        matches_data = response.json()

        if not matches_data:
            matches_data = TEST_RESPONSE_DATA

        matches_data = matches_data['matches']

        return matches_data
    else:
        print(f'Error message: {response.text}')

        return {"status": False, "message": response.text}


def clean_and_extract_data(matches_data: list) -> list:
    """
    :param matches_data:
    :return:
    """
    keys_to_remove = ['area', 'competition', 'group', 'id', 'last_updated', 'odds', 'score', 'stage', 'status']

    for i, match in enumerate(matches_data):
        matches_data[i] = {k: v for k, v in match.items() if k not in keys_to_remove}

    return matches_data


@app.route('/today_matches/<string:competition_id>')
def today_matches(competition_id: str):
    if not competition_id:
        competition_id = 'SA'

    matches_data = get_todays_matches(competition_id=competition_id)
    cleaned_matches_data = clean_and_extract_data(matches_data=matches_data)

    return jsonify(cleaned_matches_data)


@app.route('/')
def main():
    current_url = request.url
    main_data = {
        "endpoints": [
            {
                "matches in the next month": f"{current_url}today_matches/competition_id"
            }
        ],
        "competition_ids": [
            {
                "La Liga": "PD",
                "Seria A": "SA",
                "Premier League": "PL",
                "Bundesliga": "BL1",
                "Ligue 1": "FL1"
            }
        ]
    }

    return jsonify(main_data)


if __name__ == '__main__':
    app.run(debug=False)
