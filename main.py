import os
import time
import requests
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

# ================== CONFIG ==================
CONSUMER_ID = "bc7856ded484a50b96e47ee39dd8f61"
CONSUMER_SECRET = "7c9cfd02f9534850b3fa5ec2342defe9"
TELEGRAM_CHAT_ID = "797077732"

# ================== LẤY ACCESS TOKEN ==================
def get_access_token():
    url = "https://api.ssi.com.vn/v1/oauth/token"
    payload = {
        "grant_type": "client_credentials",
        "client_id": CONSUMER_ID,
        "client_secret": CONSUMER_SECRET
    }
    try:
        r = requests.post(url, data=payload)
        return r.json().get("access_token")
    except:
        return None

# ================== CẬP NHẬT GIÁ ==================
def update_prices():
    token = get_access_token()
    if not token:
        send_telegram("❌ Không lấy được Access Token")
        return

    # Lấy danh sách ticker từ Google Sheets (bạn sẽ kết nối sau)
    # Hiện tại dùng danh sách mẫu để test
    tickers = ["HPG", "FPT", "ACB", "CTG", "MSN", "IJC"]

    for ticker in tickers:
        try:
            url = f"https://fc-data.ssi.com.vn/v2.0/Market?symbol={ticker}"
            headers = {"Authorization": f"Bearer {token}"}
            r = requests.get(url, headers=headers)
            if r.status_code == 200:
                data = r.json()
                price = data.get("lastPrice", 0)
                print(f"{ticker}: {price}")
                # Sau này sẽ ghi vào Google Sheets
        except:
            print(f"Lỗi {ticker}")

    send_telegram("✅ Đã cập nhật giá thành công")

# ================== GỬI TELEGRAM ==================
def send_telegram(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": TELEGRAM_CHAT_ID, "text": message})

# ================== CHẠY LIÊN TỤC ==================
if __name__ == "__main__":
    print("🚀 HA-System bắt đầu chạy...")
    while True:
        update_prices()
        time.sleep(30)   # Chạy mỗi 30 giây (sau này chỉnh thành 10 giây)
