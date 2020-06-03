import json
import requests
from time import sleep


latest_video_url = ''


def get_config():
    with open("config/config.json", "r") as read_file:
        return json.load(read_file)


class Telegram:
    def __init__(self):
        self.token = get_config()["telegram_token"]
        self.chat_id = get_config()["telegram_chai_id"]

    def send_message(self, msg):
        requests.get(
            f"https://api.telegram.org/bot{self.token}/sendMessage?text={msg}&chat_id={self.chat_id}")


class YouTubeVideos:
    def __init__(self):
        self.url = f"https://www.youtube.com/user/{get_config()['youtube_channel_username']}/videos"

    def rm_duplicates(self, items_list):
        return list(dict.fromkeys(items_list))

    def get_videos(self):
        res = str(requests.get(self.url).content).split(' ')
        youtube_urls = [i.replace('href="', 'https://youtube.com') for i in res if 'href="/watch?' in i]
        return self.rm_duplicates(youtube_urls)


def main():
    global latest_video_url

    try:
        t = Telegram()
        y = YouTubeVideos()

        while True:
            new_video_urls = y.get_videos()

            if len(new_video_urls) != 0:
                if len(latest_video_url) == 0:
                    latest_video_url = [u[:-1] for u in new_video_urls][:-1][0]
                    t.send_message(latest_video_url)

                new_latest_url = [un[:-1] for un in new_video_urls][:-1][0]
                if new_latest_url != latest_video_url:
                    latest_video_url = new_latest_url
                    t.send_message(latest_video_url)
            else:
                main()

            sleep(3600)
    except Exception as e:
        t.send_message(str(e))
        main()


if __name__ == "__main__":
    main()
