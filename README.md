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


## API Endpoints

Your frontend interacts with three main endpoints to trigger different scraping methods.

---

### 1. `POST /htmlscraper`

- **Purpose:** Scrape product data from eMAG’s HTML search page.  
- **Request JSON:**
  ```json
  {
    "query": "laptop"
  }
  ```
- **Response JSON:**  
  A list of scraped items, each an object like:
  ```json
  {
    "item_id": 123456,
    "item_name": "Product Name",
    "item_price": "1999.99",
    "item_currency": "RON"
  }
  ```

---

### 2. `GET /firstapiscraper`

- **Purpose:** Scrape product data from the first hidden API.  
- **No request body needed.**  
- **Response JSON:**  
  A list of scraped items with the same format as `/htmlscraper`.

---

### 3. `GET /secondapiscraper`

- **Purpose:** Scrape product data from the second hidden API (experimental and slower).  
- **No request body needed.**  
- **Response JSON:**  
  A list of scraped items in the same format.  
- **Note:** Can take up to 10 minutes or more on large queries. Use only when **Deep Search** is enabled.

---

💡 **Usage flow:**

- Frontend calls `/htmlscraper` with the search term.  
- Then `/firstapiscraper` is called automatically.  
- If **Deep Search** is checked, `/secondapiscraper` is called last.

---

See your Flask `views.py` file for implementation details.


## Testing

- Run tests with pytest:
    ```bash
    python3 -m pytest
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
- The second hidden API scraper is fully functional and stores product data, but its performance is not optimized. It may take up to 10 minutes to complete, especially for large searches. Currently, it doesn't offer a clear benefit over the primary scraper, but it's kept for experimentation and potential future enhancements.
