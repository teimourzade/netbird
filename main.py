import os
import cloudscraper
import feedparser
import requests

# اطلاعات تلگرام از تنظیمات گیت‌هاب خوانده می‌شود
TELEGRAM_TOKEN = os.environ.get('TELEGRAM_TOKEN')
TELEGRAM_CHAT_ID = os.environ.get('TELEGRAM_CHAT_ID')
RSS_URL = 'https://learningdl.net/feed/'
LAST_COURSE_FILE = 'last_course.txt'

def send_telegram_message(text):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        'chat_id': TELEGRAM_CHAT_ID,
        'text': text,
        'parse_mode': 'HTML'
    }
    requests.post(url, data=payload)

def main():
    # خواندن آخرین لینک ذخیره شده
    last_link = ""
    if os.path.exists(LAST_COURSE_FILE):
        with open(LAST_COURSE_FILE, 'r', encoding='utf-8') as f:
            last_link = f.read().strip()

    # عبور از کلودفلر و گرفتن RSS
    scraper = cloudscraper.create_scraper()
    response = scraper.get(RSS_URL)
    
    if response.status_code != 200:
        print(f"Error fetching RSS: {response.status_code}")
        return

    # پردازش اطلاعات RSS
    feed = feedparser.parse(response.text)
    
    if not feed.entries:
        print("No entries found in RSS.")
        return

    # گرفتن آخرین دوره منتشر شده
    latest_entry = feed.entries[0]
    latest_title = latest_entry.title
    latest_link = latest_entry.link

    # مقایسه با دوره قبلی
    if latest_link != last_link:
        # دوره جدید است! ارسال پیام
        message = f"📚 <b>دوره جدید منتشر شد!</b>\n\n📌 نام: {latest_title}\n🔗 لینک: {latest_link}"
        send_telegram_message(message)
        
        # ذخیره لینک جدید در فایل
        with open(LAST_COURSE_FILE, 'w', encoding='utf-8') as f:
            f.write(latest_link)
        print("New course found and message sent.")
    else:
        print("No new courses.")

if __name__ == '__main__':
    main()
