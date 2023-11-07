import requests


def make_api_request():
    print("Schedule is running")
    url = "http://127.0.0.1:6543/automation"

    try:
        response = requests.get(url)
        response.raise_for_status()  # Raises HTTPError for bad requests (4xx and 5xx status codes)
        print("Response from API:", response.status_code, response.text)
    except requests.exceptions.RequestException as e:
        print("Error occurred:", e)


make_api_request()
