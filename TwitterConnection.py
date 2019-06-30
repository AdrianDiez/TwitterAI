import twython as tw
import json

import GLOBALS
import KEYS


class Connection:

    _user_twitter = None
    _public_twitter = None
    _user_info_dict = None

    def __init__(self, user_info=False):

        self._user_twitter = tw.Twython(KEYS.CONSUMER_KEY, KEYS.CONSUMER_SECRET,
                                        KEYS.ACCESS_TOKEN, KEYS.ACCESS_TOKEN_SECRET)
        self._public_twitter = tw.Twython(KEYS.CONSUMER_KEY, KEYS.CONSUMER_SECRET)

        self._user_dict = self._user_twitter.verify_credentials() if user_info else None

    def download_tweets(self):
        tweets_json = self._get_all_tweets()

        file = open(GLOBALS.FILE, "w")

        file.write(json.dumps(tweets_json, indent=4, sort_keys=True))
        file.close()

    def _get_all_tweets(self, since_id=None, user=_user_twitter):
        tweets_json = user.get_user_timeline(exclude_replies=True, include_rts=True, trim_user=True,
                                                          count=200, since_id=since_id)
        num_tweets = len(tweets_json)
        if num_tweets == 0:
            return tweets_json
        else:
            last_id = tweets_json[num_tweets - 1]['id']
            return self._get_all_tweets(since_id=last_id) + tweets_json

## TODO Add functionality to check global and local trends per user.
## TODO Create class json_parser to extract the json information into table

con = Connection()



print(con._public_twitter.get_place_trends(id=1))
