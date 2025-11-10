from abc import ABC, abstractmethod

class TikTokToolInterface(ABC):
    @abstractmethod
    def run(self):
        pass
