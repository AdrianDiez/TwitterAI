import twython as tw
import json
import pprint

import KEYS

# twitter = tw.Twython(KEYS.CONSUMER_KEY, KEYS.CONSUMER_SECRET,
#                      KEYS.ACCESS_TOKEN, KEYS.ACCESS_TOKEN_SECRET)
#
# for status in twitter.search(q='pokemon')['statuses']:
#     user = status['user']['screen_name'].encode('utf-8')
#     text = status['text'].encode('utf-8')
#     date = status['created_at']
#     hashtag = status['entities']['hashtags']
#
#     print(user, ':', text, date, hashtag)


class Connection:

    _user_twitter = None
    _public_twitter = None
    _user_info_dict = None

    def __init__(self, user_info=False):

        self._user_twitter = tw.Twython(KEYS.CONSUMER_KEY, KEYS.CONSUMER_SECRET,
                                        KEYS.ACCESS_TOKEN, KEYS.ACCESS_TOKEN_SECRET)
        self._public_twitter = tw.Twython(KEYS.CONSUMER_KEY, KEYS.CONSUMER_SECRET)

        self._user_dict = self._user_twitter.verify_credentials() if user_info else None

    def search_tweet(self):
        pass

    def download_tweets(self):
        tweets_json = self._get_all_tweets()

        file = open("user_tweets.json", "w")
        # magic happens here to make it pretty-printed
        pprint.pprint(tweets_json, file)
        # for tweet in tweets_json:
        #     file.write(json.dumps(json.loads(str(tweet))), indent=4, sort_keys=True)
        file.close()

    def _get_all_tweets(self, since_id=None):
        tweets_json = con._user_twitter.get_user_timeline(exclude_replies=True, include_rts=True, trim_user=True,
                                                          count=200, since_id=since_id)
        num_tweets = len(tweets_json)
        if num_tweets == 0:
            return tweets_json
        else:
            last_id = tweets_json[num_tweets - 1]['id']
            return self._get_all_tweets(since_id=last_id) + tweets_json

con = Connection()
pprint.pprint(con._user_twitter.get_user_timeline(exclude_replies=True, include_rts=True, trim_user=True, count=10000)[158]['id'])
print(len(con._user_twitter.get_user_timeline(exclude_replies=True, include_rts=True, trim_user=True, count=10000)))

con.download_tweets()


