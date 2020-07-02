from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import json
from dhooks import Webhook, Embed

import credentials


class TweetListener(StreamListener):
    def on_data(self, raw_data):
        data = json.loads(raw_data)
        name = data['user']['name']
        screen_name = data['user']['screen_name']
        com_name = name + ' @' + screen_name
        profile_url = 'https://twitter.com/' + data['user']['screen_name']
        avatar_url = data['user']['profile_image_url_https']
        text = data['text']
        tweet_url = 'https://twitter.com/' + data['user']['screen_name'] + '/status/' + str(data['id'])
        time = data['created_at'][:-11]

        hook = Webhook(credentials.WEBHOOK_URL)

        embed = Embed(
            color=0x1DA1F2
        )

        embed.set_author(name=com_name, url=profile_url, icon_url=avatar_url)
        embed.add_field(name="Tweet:", value=text, inline=False)
        embed.add_field(name="Time:", value=time, inline=False)
        embed.add_field(name="Link:", value=tweet_url, inline=False)
        embed.set_footer(text="Webhook made by gabrielix29", icon_url="https://avatars2.githubusercontent.com/u/57343754?s=400&u=b453123201189a7bf012aedcb8abd317ca557e69&v=4")

        hook.send(embed=embed)
        return True

    def on_error(self, status_code):
        print(status_code)
        return False


if __name__ == "__main__":
    listener = TweetListener()

    auth = OAuthHandler(credentials.TWITTER_CONSUMER_KEY, credentials.TWITTER_CONSUMER_SECRET)
    auth.set_access_token(credentials.TWITTER_ACCESS_TOKEN, credentials.TWITTER_ACCESS_TOKEN_SECRET)

    stream = Stream(auth, listener)

    stream.filter(follow=['<twitter_user_id_1>', '<twitter_user_id_2>'])
