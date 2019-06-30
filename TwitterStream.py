from twython import TwythonStreamer
import json
from time import time

import GLOBALS
import KEYS


class TwitterStreamer(TwythonStreamer):

    _lang = None
    _timestamp = None
    _count = None
    _limit = None

    def __init__(self, lang='en', limit=100):
        super().__init__(KEYS.CONSUMER_KEY, KEYS.CONSUMER_SECRET, KEYS.ACCESS_TOKEN, KEYS.ACCESS_TOKEN_SECRET)
        self._lang = lang
        self._timestamp = time()
        self._count = 0
        self._limit = limit

    # Received data
    def on_success(self, data):
        if data['lang'] == self._lang:
            tweet_data = self._process_tweet(data)
            self._save_to_json(tweet_data)
            self._count += 1

        if self._count == self._limit:
            self.disconnect()

    # Problem with the API
    def on_error(self, status_code, data):
        print(status_code, data)
        self.disconnect()

    # Save each tweet to json file
    def _save_to_json(self, tweet):
        with open(GLOBALS.STREAM_FILE.replace('id', str(self._timestamp)), 'a') as json_file:
            json.dump(tweet, json_file)
            json_file.write("\n")

    def _process_tweet(self, tweet):
        d = {}
        d['hashtags'] = [hashtag['text'] for hashtag in tweet['entities']['hashtags']]
        d['text'] = tweet['text']
        d['user'] = tweet['user']['screen_name']
        d['user_loc'] = tweet['user']['location']
        d['retweet_count'] = tweet['retweet_count']
        d['favorite_count'] = tweet['favorite_count']
        d['id'] = tweet['id']
        return d

# con = Connection()
#
# con.download_tweets()


streamer = TwitterStreamer(limit=5)
streamer.statuses.streamer()


