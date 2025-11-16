import json
import os
from tiktok_scraper.scraper_impl import TikTokScraperImpl

class TikTokToolImpl:
    def __init__(self, cookies_file="cookies.json"):
        if not os.path.exists(cookies_file):
            raise FileNotFoundError(f"File {cookies_file} không tồn tại.")
        with open(cookies_file, "r", encoding="utf-8") as f:
            cookies = json.load(f)
        self.scraper = TikTokScraperImpl(cookies)

    async def run(self):
        await self.scraper.setup()

        username = input("Nhập ID TikTok: ").strip()

        print(f"Đang lấy video hôm nay của: {username}")

        videos = await self.scraper.get_today_videos(username)

        if not videos:
            print("Không có video nào đăng hôm nay.")
        else:
            print(f"Tìm thấy {len(videos)} video hôm nay:\n")
            for v in videos:
                print(f"- {v['url']}")

        await self.scraper.cleanup()
