import json
from tiktok_scraper.scraper_impl import TikTokScraperImpl

class TikTokToolImpl:
    def __init__(self, cookies_file="cookies.json"):
        with open(cookies_file, "r", encoding="utf-8") as f:
            cookies = json.load(f)
        self.scraper = TikTokScraperImpl(cookies)

    async def run(self, channels_file="channels.txt"):
        await self.scraper.setup()

        # Đọc danh sách kênh
        with open(channels_file, "r", encoding="utf-8") as f:
            channels = [line.strip() for line in f if line.strip()]

        # Duyệt từng kênh
        for channel in channels:
            print(f"Đang xử lý kênh: {channel}")
            videos = await self.scraper.get_today_videos(channel)
            if not videos:
                print("Không có video nào được đăng hôm nay.")
            else:
                print(f"Tìm thấy {len(videos)} video hôm nay:")
                for v in videos:
                    print(v)
            print("-" * 50)

        # Cleanup session
        await self.scraper.cleanup()
