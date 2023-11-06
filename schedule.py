import requests


def make_api_request():
    print("Schedule is running")
    url = "http://127.0.0.1:6543/automation"
    response = requests.get(url)

    print("Response from API:", response.status_code, response.text)


make_api_request()
