# eMAG Price Tracker

A Python automation project that scrapes eMAG product data daily, tracks price history, and saves results in MongoDB.  
It uses **Selenium-Wire** and hidden APIs to fetch data efficiently, handles pagination, and avoids duplicate entries.  

---

## Features

- Scrape eMAG search results via HTML and hidden APIs.  
- Track price changes for products over time.  
- Store all product details and price history in MongoDB.  
- Automatically manage pagination, rate-limiting, and request headers.  
- Designed to run as a daily automation task.  
- Show case a chart with price changes a the end of the workflow.
---

## 💡 How It Works

- Scraper fetches product data via **HTML parsing** and **hidden API endpoints**.  
- Price changes are compared with the latest stored prices and **recorded if different**.  
- All product details, prices, and changes are saved in MongoDB in **structured JSON format**.  

---

## 💡 Usage Flow

- `main.py` runs the scraper for all predefined search terms.  
- Scraper fetches data via **HTML parsing** and hidden APIs.  
- If a price change is detected, it is **recorded in the price changes collection**.  
- Updated product data and price history are **saved to MongoDB**.  

---

## Setup

1. **Clone the repository:**

```bash
git clone https://github.com/AlinCqe/eMAG-scraper.git
cd eMAG-scraper
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```


3. **Configure MongoDB:**

Create a .env file in the project root.

Add your MongoDB URI:
```bash
MONGODB_URI='your-mongodb-uri'
```

**Usage**

In main.py file, in the main_workflow function, change the Scraping session item.
```bash 
scraping_session = ScrapingSession("eg. G29")
```

Run the scraper:
```bash
python main.py
```

-The script fetches products from eMAG for the predefined search terms.
-Price history and changes are automatically updated in MongoDB.

**Project Structure**

core/ — Scraper logic, DB connection, utilities
test/ — Tests for scraping and data processing logic
.env — MongoDB credentials (not tracked in git)
requirements.txt — Python dependencies
main.py - A-to-Z worflow runner

**Testing**

**Run tests with pytest:**
```bash
python3 -m pytest
```

**Notes**

Make sure to respect eMAG's terms of service when scraping.

Designed for personal or development use only.
