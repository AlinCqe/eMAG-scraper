# eMAG Scraper

A Python web scraper for eMAG, using Flask, Selenium, BeautifulSoup, and MongoDB.  
It fetches product data via HTML and hidden APIs, saves price history, and exposes endpoints for scraping.

## Features

- Scrape eMAG search results via HTML and hidden APIs
- Save product price history in MongoDB
- Avoid duplicate entries and track price changes
- Web interface for triggering scrapes
- Easily extensible for more product details (reviews, photos, links, etc.)

## Setup

1. **Clone the repo:**
    ```bash
    git clone https://github.com/AlinCqe/eMAG-scraper.git
    cd eMAG-scraper
    ```

2. **Install dependencies:**
    ```bash
    pip install -r requerements.txt
    ```

3. **Configure MongoDB:**
    - Add your MongoDB URI to `.env`:
      ```
      MONGODB_URI = 'your-mongodb-uri'
      ```

4. **Run the Flask app:**
    ```bash
    python3 -m app.app
    ```

5. **Access the web interface:**
    - Open [http://localhost:5000](http://localhost:5000) in your browser.

## Usage

- Enter a search term and optionally enable "Deep Search" for more results.
- The scraper will fetch product data and save it to MongoDB.
- Price history is tracked for each product.

## Testing

- Run tests with pytest:
    ```bash
    pytest
    ```

## Project Structure

- `app/` — Flask app, templates, static files
- `core/` — Scraper logic, DB config
- `test/` — Pytest tests
- `.env` — MongoDB credentials (not tracked in git)
- `requerements.txt` — Python dependencies

## TODO

- Batch DB queries for efficiency
- Scrape more product details (reviews, links, photos)
- Schedule daily scraping for selected items
- Tests for DataScraper class

---

**Note:**  
- Use responsibly. Scraping large amounts of data may violate eMAG's terms of service.
- For development only.  