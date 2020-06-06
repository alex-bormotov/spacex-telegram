import json
import requests
from time import sleep
from twitter_scraper import get_tweets


latest_video_url = ''
latest_tweet_url = ''


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

    def rm_duplicates(self, items_list):
        return list(dict.fromkeys(items_list))

    def get_videos(self):
        while True:
            sleep(1)
            res = requests.get(self.url)
            if res.ok and len(res.content) != 0:
                ress = str(res.content).split(' ')
                youtube_urls = [i.replace('href="', 'https://youtube.com') for i in ress if 'href="/watch?' in i]
                new_video_urls = self.rm_duplicates(youtube_urls)
                video_url = [un[:-1] for un in new_video_urls][:-1][0]
                return video_url


class Twitter:
    def __init__(self):
         self.twitter_username = get_config()['twitter_username']

    def get_tweets(self):
         while True:
             sleep(1)
             new_tweets = [f"https://twitter.com{tweet['tweetUrl']}" for tweet in get_tweets(self.twitter_username, pages=1)]
             return new_tweets[0]


def main():
    global latest_video_url
    global latest_tweet_url
    t = Telegram()
    y = YouTube()
    tw = Twitter()

    try:
        while True:
            new_video_url = y.get_videos()
            if len(latest_video_url) == 0:
                latest_tweet_url = new_video_url
            if new_video_url != latest_video_url:
                latest_video_url = new_video_url
                t.send_message(latest_video_url)

            new_tweet_url = tw.get_tweets()
            if len(latest_tweet_url) == 0:
                latest_tweet_url = new_tweet_url
            if new_tweet_url != latest_tweet_url:
                latest_tweet_url = new_tweet_url
                t.send_message(latest_tweet_url)

            sleep(300)
    except Exception as e:
        t.send_message(str(e))
        main()


if __name__ == "__main__":
    main()
