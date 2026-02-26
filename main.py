import os
import time
import requests

# In IP công khai để đăng ký với SSI
import requests
print("PUBLIC IP của Railway:", requests.get('https://api.ipify.org').text)

# Load từ Environment Variables trên Railway
CONSUMER_ID = os.getenv('CONSUMER_ID')
CONSUMER_SECRET = os.getenv('CONSUMER_SECRET')
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

if not all([CONSUMER_ID, CONSUMER_SECRET, TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID]):
    print("❌ Thiếu biến môi trường. Kiểm tra Settings → Variables trên Railway.")
    exit(1)

def get_access_token():
    url = "https://api.ssi.com.vn/v1/oauth/token"
    payload = {
        "grant_type": "client_credentials",
        "client_id": CONSUMER_ID,
        "client_secret": CONSUMER_SECRET
    }
    try:
        r = requests.post(url, data=payload)
        r.raise_for_status()
        token = r.json().get("access_token")
        print("✅ Lấy Access Token thành công")
        return token
    except Exception as e:
        print(f"❌ Lỗi lấy token: {e}")
        return None

def send_telegram(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    try:
        requests.post(url, data={"chat_id": TELEGRAM_CHAT_ID, "text": message})
        print("✅ Telegram sent")
    except Exception as e:
        print(f"Lỗi gửi Telegram: {e}")

def update_prices():
    token = get_access_token()
    if not token:
        send_telegram("❌ Không lấy được Access Token từ SSI")
        return

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
        except Exception as e:
            print(f"Lỗi {ticker}: {e}")

if __name__ == "__main__":
    print("🚀 HA-System bắt đầu chạy...")
    while True:
        update_prices()
        time.sleep(30)
