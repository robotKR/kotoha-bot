import json
from requests_oauthlib import OAuth1Session
import time
from time import sleep
import tweepy
import requests
import schedule
import re
import random
import concurrent.futures
import tweets
import global_value as g
import os

# To set your enviornment variables in your terminal run the following line:
# export 'BEARER_TOKEN'='<your_bearer_token>'
consumer_key = os.environ['consumer_key']
consumer_secret = os.environ['consumer_secret']
access_token = os.environ['access_token']
access_token_secret = os.environ['access_token_secret']
bearer_token = os.environ['bearer_token']
API_KEY_mebo = os.environ['bearer_token']
agent_id = os.environ['bearer_token']

Client = tweepy.Client(bearer_token, consumer_key, consumer_secret, access_token, access_token_secret)

def bearer_oauth(r):
    """
    Method required by bearer token authentication.
    """

    r.headers["Authorization"] = f"Bearer {bearer_token}"
    r.headers["User-Agent"] = "v2FilteredStreamPython"
    return r


def get_rules():
    response = requests.get(
        "https://api.twitter.com/2/tweets/search/stream/rules", auth=bearer_oauth
    )
    if response.status_code != 200:
        raise Exception(
            "Cannot get rules (HTTP {}): {}".format(response.status_code, response.text)
        )
    print(json.dumps(response.json()))
    return response.json()


def delete_all_rules(rules):
    if rules is None or "data" not in rules:
        return None

    ids = list(map(lambda rule: rule["id"], rules["data"]))
    payload = {"delete": {"ids": ids}}
    response = requests.post(
        "https://api.twitter.com/2/tweets/search/stream/rules",
        auth=bearer_oauth,
        json=payload
    )
    if response.status_code != 200:
        raise Exception(
            "Cannot delete rules (HTTP {}): {}".format(
                response.status_code, response.text
            )
        )
    print(json.dumps(response.json()))


def set_rules(delete):
    # You can adjust the rules if needed
    sample_rules = [
        {"value": "to:k20824387"}
    ]
    payload = {"add": sample_rules}
    response = requests.post(
        "https://api.twitter.com/2/tweets/search/stream/rules",
        auth=bearer_oauth,
        json=payload,
    )
    if response.status_code != 201:
        raise Exception(
            "Cannot add rules (HTTP {}): {}".format(response.status_code, response.text)
        )
    print(json.dumps(response.json()))


def get_stream(set):
    response = requests.get(
        "https://api.twitter.com/2/tweets/search/stream?expansions=author_id&user.fields=name", auth=bearer_oauth, stream=True,
    )
    print(response.status_code)
    if response.status_code != 200:
        raise Exception(
            "Cannot get stream (HTTP {}): {}".format(
                response.status_code, response.text
            )
        )
    for response_line in response.iter_lines():
        if response_line:
            json_response = json.loads(response_line)
            #print(json.dumps(json_response, indent=4, sort_keys=True))
            
            tweet_id = json_response["data"]["id"] #ツイートID
            reply_text=json_response["data"]["text"] #相手の送ってきた内容
            user_id=json_response["data"]["author_id"]#ユーザーID
            user_name=json_response["includes"]["users"]#ユーザーネーム取得
            user_name=user_name[0]["name"]

            print(user_name)

            reply_text=re.sub(r'@([A-Za-z0-9_]+)', "", reply_text)

            headers_mebo = {'Content-Type': 'application/json'}
                        
            json_data = {
                            'api_key': API_KEY_mebo,
                            'agent_id': agent_id,
                            'utterance': reply_text,
                            'uid': 'mebo.ai_' + str(user_id),
                        }

            response = requests.post('https://api-mebo.dev/api', headers=headers_mebo, data=json.dumps(json_data))

            res_data = response.json()
            replay = response.text
            replay = json.loads(replay)
            replay = replay['bestResponse']['utterance']

            ###ここで自分のリプライの内容を設定します
            text = replay

            print(response.status_code)
            print(response.text)
            print(user_id)
            print(replay)

            print(text)
            Client.create_tweet(
                text=text,
                in_reply_to_tweet_id =tweet_id)


def tweet1():
    tweets.tweet()
    tweets1 = g.generation_list
    tweets1 = tweets1[1]
    tweets1 = re.sub(' ', "", tweets1)
    Client.create_tweet(text=tweets1)
    print("Tweet Done")

def morning():
    print("schedule morning done")
    random1 = random.randint(1,5)
    if random1 == 1:
        Client.create_tweet(text="おはよう！")
    elif random1 == 2:
        Client.create_tweet(text="おっはよおおお！")
    elif random1 == 3:
        Client.create_tweet(text="朝だぞー！起きろー！")
    elif random1 == 4:
        Client.create_tweet(text="おはよ！")
    elif random1 == 5:
        Client.create_tweet(text="おはー")

def night():
    print("schedule night done")
    random1 = random.randint(1,5)
    if random1 == 1:
        Client.create_tweet(text="今日もお疲れ様！おやすみ！")
    elif random1 == 2:
        Client.create_tweet(text="おやすみ！")
    elif random1 == 3:
        Client.create_tweet(text="おやすみなさい！")
    elif random1 == 4:
        Client.create_tweet(text="おやすみー！")
    elif random1 == 5:
        Client.create_tweet(text="おやすみー")

def schedule1():
    schedule.every().days.at("22:00").do(morning)
    schedule.every().days.at("14:00").do(night)
    schedule.every(2).hours.do(tweet1)
    
    while True:
        schedule.run_pending()
        time.sleep(1)

def main():
    rules = get_rules()
    delete = delete_all_rules(rules)
    set = set_rules(delete)
    executor = concurrent.futures.ThreadPoolExecutor(max_workers=2)
    executor.submit(schedule1)
    executor.submit(get_stream(set))


if __name__ == "__main__":
    main()