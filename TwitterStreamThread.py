import json
import time
import sys

from threading import Thread
from twython import TwythonStreamer

import GLOBALS
import KEYS


class _StreamerThread(TwythonStreamer, Thread):

    _lang = None
    _timestamp = None
    _count = None
    _limit = None
    _track = None

    def __init__(self, track, lang='en', limit=100):
        TwythonStreamer.__init__(self, KEYS.CONSUMER_KEY, KEYS.CONSUMER_SECRET, KEYS.ACCESS_TOKEN, KEYS.ACCESS_TOKEN_SECRET)
        Thread.__init__(self)
        self._lang = lang
        self._timestamp = time.time()
        self._count = 0
        self._limit = limit
        self._track = track

    # Received data
    def on_success(self, data):
        tweet_data = self._process_tweet(data)
        self._save_to_json(tweet_data)
        self._count += 1

        if self._count == self._limit:
            sys.exit()

    # Problem with the API
    def on_error(self, status_code, data):
        print(status_code, data)
        self.disconnect()

    def run(self):
        self.statuses.filter(track=self._track, language=self._lang)

    @property
    def get_count(self):
        return self._count

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


class StreamTimer():
    _track: str = None
    _timer: int = None
    _lang: str = None
    _limit: int = None
    _number_returned = None

    def __init__(self, track, timer=60, lang='en', limit=100):
        self._track = track
        self._timer = timer
        self._lang = lang
        self._limit = limit

    def start(self):
        stream = _StreamerThread(self._track, lang=self._lang, limit=self._limit)
        stream.start()
        while self._timer > 0 and stream.is_alive():
            time.sleep(0.8)
            self._timer -= 1
        stream.disconnect()
        self._number_returned = stream.get_count()

    @property
    def get_count(self):
        return self._number_returned

    def set_timer(self, timer):
        assert isinstance(timer, int)
        self._timer = timer

    def set_track(self, track):
        assert isinstance(track, str)
        self._track = track

    def set_limit(self, limit):
        assert isinstance(limit, int)
        self._limit = limit

    def set_lang(self, lang):
        assert isinstance(lang, str)
        self._lang = lang



tmr = StreamTimer(track='data', timer=5, limit=50)
tmr.start()