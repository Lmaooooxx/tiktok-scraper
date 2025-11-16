from abc import ABC, abstractmethod

class TikTokScraperInterface(ABC):

    @abstractmethod
    async def setup(self):
        pass

    @abstractmethod
    async def get_today_videos(self, username: str):
        pass

    @abstractmethod
    async def cleanup(self):
        pass
