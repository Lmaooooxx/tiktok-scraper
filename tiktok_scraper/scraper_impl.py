from datetime import datetime, timezone, timedelta
from TikTokApi import TikTokApi

class TikTokScraperImpl:
    def __init__(self, cookies: list = None):
        self.cookies = cookies or []
        self.api = TikTokApi(logging_level=30)

    async def setup(self):
        await self.api.create_sessions(
            cookies=self.cookies,
            num_sessions=1,
            headless=False,
            browser="chromium"
        )

    async def get_today_videos(self, username: str, count: int = 50):
        today_videos = []
        tz_vn = timezone(timedelta(hours=7))
        today_vn = datetime.now(tz=tz_vn).date()

        user = self.api.user(username=username)
        async for video in user.videos(count=count):
            v = video.as_dict
            ct = v.get("create_time") or v.get("createTime")
            if not ct:
                continue
            video_date_vn = datetime.fromtimestamp(ct, tz=timezone.utc).astimezone(tz=tz_vn).date()
            
            # Chỉ lấy video hôm nay
            if video_date_vn != today_vn:
                continue

            # ✅ Dùng link trang TikTok thật
            video_id = v.get("id", "")
            video_url = f"https://www.tiktok.com/@{username}/video/{video_id}"

            today_videos.append({
                "id": video_id,
                "desc": v.get("desc", ""),
                "url": video_url,
                "likes": v.get("stats", {}).get("digg_count", 0),
                "comments": v.get("stats", {}).get("comment_count", 0),
                "date": str(video_date_vn)
            })

        return today_videos

    async def cleanup(self):
        await self.api.close_sessions()
        await self.api.stop_playwright()
