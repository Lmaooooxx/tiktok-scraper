from datetime import datetime, timezone
from TikTokApi import TikTokApi

class TikTokScraperImpl:
    def __init__(self, cookies: list):
        self.cookies = cookies
        self.api = TikTokApi(logging_level=30)  # tắt debug log

    async def setup(self):
        # Tạo session với cookies
        await self.api.create_sessions(cookies=self.cookies, num_sessions=1)

    async def get_today_videos(self, username: str, count: int = 20):
        today_videos = []
        today = datetime.now(timezone.utc).date()
        try:
            # Không dùng await khi khởi User object
            user = self.api.user(username=username)

            # Async iterator lấy video
            async for video in user.videos(count=count):
                video_date = datetime.fromtimestamp(video.create_time, tz=timezone.utc).date()
                if video_date == today:
                    today_videos.append({
                        "id": video.id,
                        "desc": video.desc,
                        "url": video.video.play_addr,
                        "likes": video.stats.digg_count,
                        "comments": video.stats.comment_count,
                        "date": str(video_date)
                    })
            return today_videos
        except Exception as e:
            print(f"Lỗi khi lấy dữ liệu cho {username}: {e}")
            return []

    async def cleanup(self):
        await self.api.close_sessions()
        await self.api.stop_playwright()
