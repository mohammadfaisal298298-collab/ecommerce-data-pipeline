# Automated E-Commerce Data Pipeline

An ETL pipeline that scrapes web data, stores it in SQLite, and triggers email alerts.

## Project Highlights

* **Web Scraping:** Built a Python scraper using BeautifulSoup to extract live product data, using custom HTTP headers to bypass basic bot-protection systems.
* **Data Pipeline:** Wrote a cleaning script to sanitize messy HTML strings into usable float values to prevent math and encoding crashes.
* **Database Storage:** Set up a local SQLite database to permanently log daily price changes, making it easy to track historical price trends.
* **Automated Alerts:** Integrated Google's SMTP server to automatically dispatch an email alert to my phone whenever an item drops below a set budget.

## How to Run Locally

**1. Install Dependencies**  
This script uses standard Python libraries (`sqlite3`, `smtplib`, `datetime`) for the database and email logic, but requires two external packages for the web scraper. Install them via your terminal:
`pip install requests beautifulsoup4`

**2. Configure Your Credentials**  
Before running the script, open the Python file and replace the placeholder email variables with your own testing credentials. *Note: You must use a Google App Password, not a standard account password.*
```python
sender_email = "your_dummy_email@gmail.com"
app_password = "your_16_letter_app_password"
receiver_email = "your_real_email@gmail.com"
```

<img width="824" height="220" alt="ecommerce-data-pipeline-price_tracker" src="https://github.com/user-attachments/assets/73618f5c-7497-41b7-b8cc-52bfc6793d9c" />
