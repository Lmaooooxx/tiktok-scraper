import asyncio
from tiktok_tool.tool_impl import TikTokToolImpl

async def main():
    tool = TikTokToolImpl(cookies_file="cookies.json")
    await tool.run("channels.txt")

if __name__ == "__main__":
    asyncio.run(main())
