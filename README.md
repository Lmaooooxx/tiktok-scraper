# TikTok Today – Lấy Video Đăng Hôm Nay

## Mô tả
Project này giúp lấy danh sách video được đăng hôm nay của một hoặc nhiều user TikTok.  


## Cấu trúc project
```
project/
│── app.py # Streamlit Web UI
│── cookies.json # Cookie TikTok để đăng nhập
│── requirements.txt # Dependencies
├── tiktok_scraper/ # Package chuyên về scraping TikTok
│ ├── init.py
│ ├── scraper_impl.py
│ ├── scraper_interface.py
└── tiktok_tool/ # Package CLI tool
├── init.py
├── tool_impl.py
├── tool_interface.py
```
## Cài đặt
1. Clone project hoặc tải về máy:
2. Tạo môi trường ảo(nên dùng):
```bash
python -m venv venv
# Linux/macOS
source venv/bin/activate
# Windows
venv\Scripts\activate
```
3. Cài dependencies:
```bash
pip install -r requirements.txt
```
4. Cài Playwright browser binaries:
```bash
playwright install

```
## Chạy Web UI (Streamlit)
1. Chạy lệnh:
```bash
streamlit run app.py
```
2. Streamlit sẽ mở trình duyệt hoặc link localhost.
3. Nhập username TikTok
4. Click nút Lấy video hôm nay.
5. Danh sách video được đăng hôm nay sẽ hiển thị:
   - Video ID
   - Mô tả
   - Ngày đăng
   - Link xem video trên TikTok  
