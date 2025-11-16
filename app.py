# app.py
import sys
import asyncio
import json
import os
import streamlit as st

# ===== 1️⃣ Patch Windows + Streamlit =====
try:
    import nest_asyncio
    nest_asyncio.apply()
except ModuleNotFoundError:
    st.error(
        "Module 'nest_asyncio' chưa được cài.\n"
        "Chạy lệnh sau trong terminal của môi trường ảo của bạn:\n"
        "pip install nest_asyncio"
    )
    st.stop()

# Windows ProactorEventLoopPolicy để Playwright chạy subprocess
if sys.platform.startswith("win"):
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

# ===== 2️⃣ Import TikTokScraperImpl sau khi patch =====
from tiktok_scraper.scraper_impl import TikTokScraperImpl

# ===== 3️⃣ Hàm async lấy video hôm nay =====
async def fetch_today_videos(username: str, cookies: list):
    scraper = TikTokScraperImpl(cookies=cookies)
    await scraper.setup()
    videos = await scraper.get_today_videos(username)
    await scraper.cleanup()
    return videos

# ===== 4️⃣ Streamlit UI =====
st.set_page_config(page_title="TikTok Today", layout="centered")
st.title("TikTok Today – Lấy video đăng hôm nay")
st.write("Nhập username TikTok và hệ thống sẽ trả về danh sách video được đăng **hôm nay**.")

# Load cookies tự động
cookies_file = "cookies.json"
cookies = []
if os.path.exists(cookies_file):
    with open(cookies_file, "r", encoding="utf-8") as f:
        cookies = json.load(f)
else:
    st.warning(f"Không tìm thấy file {cookies_file}. TikTok có thể yêu cầu đăng nhập lại.")

# Nhập username TikTok  
username = st.text_input("Nhập TikTok username:", "")

# Button lấy video
run_btn = st.button("Lấy video hôm nay")

if run_btn:
    if username.strip() == "":
        st.warning("Vui lòng nhập username!")
    else:
        st.info("⏳ Đang xử lý, đợi tí nhé...")
        try:
            videos = asyncio.run(fetch_today_videos(username.strip(), cookies))

            st.success(f"🎉 Tìm thấy {len(videos)} video hôm nay cho @{username}")

            if len(videos) == 0:
                st.warning("Không có video nào hôm nay.")
            else:
                for v in videos:
                    st.subheader(f"Video ID: {v['id']}")
                    st.write(f"**Mô tả:** {v['desc']}")
                    st.write(f"**Ngày:** {v['date']}")
                    st.write(f"[Xem video]({v['url']})")
                    st.write("---")

        except Exception as e:
            st.error(f"Lỗi: {e}")
