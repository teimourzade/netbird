import os
import requests

TELEGRAM_TOKEN = os.environ.get('TELEGRAM_TOKEN')
TELEGRAM_CHAT_ID = os.environ.get('TELEGRAM_CHAT_ID')

# لینک RSS سایت
RSS_URL = 'https://learningdl.net/feed/'
# استفاده از سرویس واسطه rss2json
API_URL = f'https://api.rss2json.com/v1/api.json?rss_url={RSS_URL}'

def send_telegram_message(text):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": text,
        "parse_mode": "HTML"
    }
    requests.post(url, json=payload)

def main():
    try:
        response = requests.get(API_URL)
        if response.status_code != 200:
            print(f"Error: API returned status code {response.status_code}")
            return
            
        data = response.json()
        
        if data.get('status') != 'ok' or not data.get('items'):
            print("Error: Could not parse items or feed is empty.")
            return

        # گرفتن آخرین دوره (اولین آیتم در لیست)
        latest_item = data['items'][0]
        latest_title = latest_item['title']
        latest_link = latest_item['link']

        # خواندن لینک آخرین دوره ثبت شده
        last_saved_link = ""
        if os.path.exists('last_course.txt'):
            with open('last_course.txt', 'r', encoding='utf-8') as f:
                last_saved_link = f.read().strip()

        # بررسی اینکه آیا دوره جدید است یا خیر
        if latest_link != last_saved_link:
            message = f"🆕 <b>دوره جدید اضافه شد!</b>\n\n🔹 {latest_title}\n🔗 <a href='{latest_link}'>مشاهده دوره</a>"
            send_telegram_message(message)
            
            # ذخیره لینک جدید در فایل
            with open('last_course.txt', 'w', encoding='utf-8') as f:
                f.write(latest_link)
            print("New course found! Message sent and file updated.")
        else:
            print("No new courses found.")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == '__main__':
    main()
