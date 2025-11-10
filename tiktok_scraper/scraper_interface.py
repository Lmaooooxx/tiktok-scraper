from abc import ABC, abstractmethod

class TikTokScraperInterface(ABC):
    @abstractmethod
    def get_today_videos(self, username: str):
        pass
