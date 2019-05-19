import twython as tw
import KEYS

twitter = tw.Twython(KEYS.CONSUMER_KEY, KEYS.CONSUMER_SECRET,
                     KEYS.ACCESS_TOKEN, KEYS.ACCESS_TOKEN_SECRET)

for status in twitter.search(q='pokemon')['statuses']:
    user = status['user']['screen_name'].encode('utf-8')
    text = status['text'].encode('utf-8')
    date = status['created_at']
    hashtag = status['entities']['hashtags']

    print(user, ':', text, date, hashtag)




class Connection:
    user_twitter = None
    public_twitter = None

    def __init__(self):

        self.user_twitter = tw.Twython(KEYS.CONSUMER_KEY, KEYS.CONSUMER_SECRET,
                                       KEYS.ACCESS_TOKEN, KEYS.ACCESS_TOKEN_SECRET)
        self.public_twitter = tw.Twython(KEYS.CONSUMER_KEY, KEYS.CONSUMER_SECRET)

con = Connection()

print(con.user_twitter.verify_credentials())
