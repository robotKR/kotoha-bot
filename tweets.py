# -*- coding: utf-8 -*-
from itertools import count
import markovify
import tweepy
import re
import MeCab
import os
import global_value as g
 
def tweet():

    # 取得した各種キーを格納---------------------------------------------
    consumer_key = os.environ['consumer_key']
    consumer_secret = os.environ['consumer_secret']
    access_token= os.environ['access_token']
    access_token_secret = os.environ['access_token_secret']
 
    # Twitterオブジェクトの生成
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)
    #-------------------------------------------------------------------
 
    #ツイートを投稿
    tweets = api.home_timeline(count=500, page=1)
    tweet_list = []
    text_list = []
    g.generation_list = []

    for tweet in tweets:
        tweet = tweet.text
        tweet=re.sub(r'https?://[\w/:%#\$&\?\(\)~\.=\+\-…]+', "", tweet)
        tweet=re.sub('RT', "", tweet)
        tweet=re.sub('お気に入り', "", tweet)
        tweet=re.sub(r'(?:^|\s)[＃#]{1}(\w+)', "", tweet)
        tweet=re.sub(r'@([A-Za-z0-9_]+)', "", tweet)
        tweet=re.sub(r':', "", tweet)
        tweet=re.sub('　', "", tweet)
        tweet=re.sub('。', "", tweet)
        tweet=tweet+"。"
        tweet_list.append(tweet)

    print(tweet_list)
    text = '\n'.join(tweet_list)

    # Replace Bad Symbols for markovify to function
    #Refer: https://github.com/jsvine/markovify/issues/84
    table = str.maketrans({
        # '\n': '',
        # '\r': '',
        '(': '（',
        ')': '）',
        '[': '［',
        ']': '］',
        '"':'”',
        "'":"’",
    })
    text = text.translate(table).split()
    url_pattern = "https?://[\w/:%#\$&\?\(\)~\.=\+\-]+"

    # Parse text using MeCab
    m = MeCab.Tagger('-Owakati')
    for line in text:
        splited_line = m.parse(line)
        text = str(splited_line)
        text_list.append(text)

    text = '\n'.join(text_list)

    # Build model
    text_model = markovify.NewlineText(text, state_size=3, well_formed=False)
    text_model = markovify.Text.from_json(text_model.to_json())
    for i in range(10): #10個のつぶやき生成
        generation =  text_model.make_short_sentence(140)
        g.generation_list.append(generation)
        g.generation_list = filter(None, g.generation_list)
        g.generation_list = list(g.generation_list)
        print(g.generation_list)

if __name__ == '__main__':
    tweet()