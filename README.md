# eMAG Scraper 

Hey there! 

Welcome to my eMAG scraper :D

This is a python script that scrapes the names and prices of items on Emag.ro based on a search query.
After scraping, it stores the item name and price in to a csv or excel file.

## How eMAG.ro displays items

eMAG uses three different methods to show items:
 1. Static elements in the initial HTML
 2. A hidden endpoint with up to 100 items (these seem to be some kind of recommended/trend items)
 3. A second endpoint that contains all the remaining items (maybe the full product list, im not sure)

## Tools & Methods

 - For the static elements i used requests + BeautifulSoup to scrape the HTML 
 - For the hidden APIs, I used Selenium Wire to capture the necessary endpoints.
      - I couldn't directly call the hidden API with just the search term, because it applies some kind of filters or recommendation logic that I couldn't reverse-engineer.

## Workflow

 1. Grab the static items from the HTML.
 2. Use the first endpoint to retrieve up to 100 items.
 3. Move on to the second endpoint, looping through all pages (could be over 5000 items, with each page containing up to 100).
 4. A system is in place to skip duplicates so no item is repeated.
 5. The script extracts:
    - Item name
    - Price
    - Currency (e.g. "RON")

All data is saved into a CSV file using pandas.



Note: I'm not very familiar with pandas yet, so I haven't implemented filtering or data manipulation features — just simple extraction and saving for now.

