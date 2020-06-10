import json
import praw
import requests
from time import sleep
from twitter_scraper import get_tweets

latest_video_url = ''
latest_tweet_url = ''
latest_reddit_url = ''

def get_config():
    with open("config/config.json", "r") as read_file:
        return json.load(read_file)


class Telegram:
    def __init__(self):
        self.token = get_config()["telegram_token"]
        self.chat_id = get_config()["telegram_chai_id"]

    def send_message(self, msg):
        requests.get(f"https://api.telegram.org/bot{self.token}/sendMessage?text={msg}&chat_id={self.chat_id}")


class YouTube:
    def __init__(self):
        self.url = f"https://www.youtube.com/user/{get_config()['youtube_channel_username']}/videos"

    def get_videos(self):
        while True:
            sleep(1)
            res = requests.get(self.url)
            if res.ok and len(res.content) != 0:
                ress = str(res.content).split(' ')
                youtube_urls = [i.replace('href="', 'https://youtube.com') for i in ress if 'href="/watch?' in i]
                y_urls = [u[:-1] for u in list(dict.fromkeys(youtube_urls))][:-1]
                if len(y_urls) != 0:
                    return y_urls[0]


class Twitter:
    def __init__(self):
         self.twitter_username = get_config()['twitter_username']

    def get_tweets(self):
         while True:
             sleep(1)
             new_tweets = [f"https://twitter.com{tweet['tweetUrl']}" for tweet in get_tweets(self.twitter_username, pages=1)]
             if len(new_tweets) != 0:
                 return new_tweets[0]


class Reddit:
    def __init__(self):
        self.reddit_client_id = get_config()['reddit_client_id']
        self.reddit_client_secret = get_config()['reddit_client_secret']
        self.reddit_user_agent = get_config()['reddit_user_agent']
        self.subreddit = get_config()['subreddit']
        self.reddit = praw.Reddit(client_id=self.reddit_client_id, client_secret=self.reddit_client_secret, user_agent=self.reddit_user_agent)

    def get_reddit_url(self):
        while True:
            sleep(1)
            reddit_url = [post.url for post in self.reddit.subreddit(self.subreddit).new(limit=1)]
            if len(reddit_url) != 0:
                return reddit_url[0]


def main():
    global latest_video_url
    global latest_tweet_url
    global latest_reddit_url

    t = Telegram()
    y = YouTube()
    tw = Twitter()
    rd = Reddit()

    try:
        while True:
            new_video_url = y.get_videos()
            new_tweet_url = tw.get_tweets()
            new_reddit_url = rd.get_reddit_url()

            if len(latest_video_url) == 0:
                latest_video_url = new_video_url
            if new_video_url != latest_video_url:
                latest_video_url = new_video_url
                t.send_message(latest_video_url)

            if len(latest_tweet_url) == 0:
                latest_tweet_url = new_tweet_url
            if new_tweet_url != latest_tweet_url:
                latest_tweet_url = new_tweet_url
                t.send_message(latest_tweet_url)

            if len(latest_reddit_url) == 0:
                latest_reddit_url = new_reddit_url
            if new_reddit_url != latest_reddit_url:
                latest_reddit_url = new_reddit_url
                t.send_message(latest_reddit_url)

            sleep(300)
    except Exception as e:
        t.send_message(str(e))
        main()


if __name__ == "__main__":
    main()
