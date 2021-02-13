import requests
import yaml

# Process the yaml auth file storing API token data
def process_yaml(auth_location):
    with open(auth_location) as file:
        return yaml.safe_load(file)

# Create a twitter API access token from the auth.yml file token
def create_token(data):
    return data["twitter_api"]["bearer_token"]

# Authenticate and connect to the twitter APIs
def twitter_auth_and_connect(twitter_api_token, url):
    headers = {"Authorization": "Bearer {}".format(twitter_api_token)}
    response = requests.request("GET", url, headers=headers)
    return response.json()

# Run the twitter API request url passed to the function, and return the results
def run_twitter_request_fetch_tweets(url, auth_location):
    err = None
    res_json = run_twitter_request(url, auth_location)
    if res_json['meta']['result_count'] == 0:
        err = "noTweetsFound"
    return res_json, err

# Run the twitter API request url passed to the function, and return the results
def run_twitter_request_fetch_account_info(url, auth_location):
    err = None
    data = process_yaml(auth_location)
    twitter_api_token = create_token(data)
    res_json = twitter_auth_and_connect(twitter_api_token, url)
    # if res_json['meta']['result_count'] == 0:
    #     err = "noTweetsFound"
    return res_json, err

# Run the twitter API request url passed to the function, and return the results
def run_twitter_request(url, auth_location):
    data = process_yaml(auth_location)
    twitter_api_token = create_token(data)
    res_json = twitter_auth_and_connect(twitter_api_token, url)
    return res_json