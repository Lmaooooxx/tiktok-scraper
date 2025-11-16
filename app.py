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

# ===== 2️⃣ Import TikTokScraperImpl sau patch =====
from tiktok_scraper.scraper_impl import TikTokScraperImpl

# ===== 3️⃣ Hàm async lấy video hôm nay =====
async def fetch_today_videos(usernames: list, cookies: list):
    scraper = TikTokScraperImpl(cookies=cookies)
    await scraper.setup()

    results = {}  # {username: [videos]}

    for username in usernames:
        videos = await scraper.get_today_videos(username)
        results[username] = videos

    await scraper.cleanup()
    return results

# ===== 4️⃣ Streamlit UI =====
st.set_page_config(page_title="TikTok Today", layout="centered")
st.title("TikTok Today – Lấy video đăng hôm nay")
st.write("Nhập **1 hoặc nhiều** username TikTok, cách nhau bằng dấu phẩy.")

# Load cookies tự động
cookies_file = "cookies.json"
cookies = []
if os.path.exists(cookies_file):
    with open(cookies_file, "r", encoding="utf-8") as f:
        cookies = json.load(f)
else:
    st.warning(f"Không tìm thấy file {cookies_file}. TikTok có thể yêu cầu đăng nhập lại.")

# Nhập username TikTok
raw_input = st.text_input("Nhập TikTok username :", "")

# Button
run_btn = st.button("Lấy video hôm nay")

if run_btn:
    usernames = [u.strip() for u in raw_input.split(",") if u.strip()]

    if not usernames:
        st.warning("Vui lòng nhập ít nhất 1 username!")
    else:
        st.info("Đang xử lý...")

        try:
            results = asyncio.run(fetch_today_videos(usernames, cookies))

            # ---- Hiển thị kết quả ----
            for username in usernames:
                videos = results.get(username, [])

                st.subheader(f"@{username}")

                if not videos:
                    st.warning(f"@{username} không có video nào đăng hôm nay.")
                else:
                    st.success(f"{len(videos)} video hôm nay từ @{username}")

                    for v in videos:
                        st.write(f"**Video ID:** {v['id']}")
                        st.write(f"**Mô tả:** {v['desc']}")
                        st.write(f"**Ngày:** {v['date']}")
                        st.write(f"**Comments:** {v['comments']}")
                        st.write(f"[🔗 Xem video]({v['url']})")
                        st.write("---")

        except Exception as e:
            st.error(f"Lỗi: {e}")
