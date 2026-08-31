import requests
from bs4 import BeautifulSoup
import sqlite3
from datetime import datetime
import smtplib
from email.mime.text import MIMEText

# ==========================================
# 1. SCRAPING
# ==========================================
url = "https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html"
headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36"
}

response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, 'html.parser')

book_title = soup.find("h1").text
price_text = soup.find("p", class_="price_color").text

# Clean the price string
clean_string = ''.join(char for char in price_text if char.isdigit() or char == '.')
clean_price = float(clean_string)

print(f"Scraped Price: {clean_price}")

# ==========================================
# 2. DATABASE SAVING
# ==========================================
conn = sqlite3.connect('price_tracker.db')
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS price_history (
        date TEXT,
        item_name TEXT,
        price REAL
    )
''')

today_date = datetime.now().strftime("%Y-%m-%d")
cursor.execute("INSERT INTO price_history (date, item_name, price) VALUES (?, ?, ?)",
               (today_date, book_title, clean_price))
conn.commit()
conn.close()

# ==========================================
# 3. THE ALERT LOGIC
# ==========================================
TARGET_PRICE = 52.00  # The budget we want to stay under

if clean_price < TARGET_PRICE:
    print(f"PRICE DROP ALERT! It is under £{TARGET_PRICE}. Sending email...")

    # Email Settings 
    sender_email = "YOUR_SENDER_EMAIL@gmail.com"
    app_password = "YOUR_APP_PASSWORD"
    receiver_email = "YOUR_RECEIVER_EMAIL@gmail.com"

    # Craft the message
    msg = MIMEText(f"Good news! {book_title} has dropped to £{clean_price}!")
    msg['Subject'] = f"Sale Alert: {book_title}"
    msg['From'] = sender_email
    msg['To'] = receiver_email

    try:
        # Log into Google's email server and send it
        server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
        server.login(sender_email, app_password)
        server.sendmail(sender_email, receiver_email, msg.as_string())
        server.quit()
        print("Email sent successfully!")
    except Exception as e:
        print(f"Failed to send email. Error: {e}")

else:
    print(f"Price is still too high. (Needs to be under £{TARGET_PRICE})")
