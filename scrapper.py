# scrapper.py
import requests
from bs4 import BeautifulSoup
import csv
import time
import os

BASE_URL = "http://books.toscrape.com/"
START_URL = "http://books.toscrape.com/catalogue/page-1.html"

def get_soup(url):
    """Fetch the content of a given URL and return a BeautifulSoup object."""
    response = requests.get(url)
    if response.status_code == 200:
        return BeautifulSoup(response.text, 'lxml')
    else:
        print(f"Failed to retrieve {url} - status code: {response.status_code}")
        return None

def get_book_description(detail_url):
    """
    Fetch the book's detail page and extract the real product description.
    """
    soup = get_soup(detail_url)
    if not soup:
        return "No real description found."

    # The description is often under a div with id="product_description"
    desc_header = soup.find('div', id='product_description')
    if desc_header:
        # The next sibling <p> usually contains the actual text
        desc_paragraph = desc_header.find_next_sibling('p')
        if desc_paragraph:
            return desc_paragraph.get_text(strip=True)
    return "No real description found."

def parse_book_data(book):
    """
    Extract details from a single book item on the listing page.
    Returns a dictionary with the relevant information, including real description.
    """
    # Title
    title_element = book.select_one('h3 a')
    title = title_element['title'] if title_element else "No title"

    # Relative URL to the book's detail page
    book_url = book.select_one('h3 a')['href']
    detail_url = BASE_URL + "catalogue/" + book_url.replace('../', '')

    # Price
    price_element = book.select_one('.price_color')
    price = price_element.get_text(strip=True) if price_element else "No price"

    # Availability
    availability_element = book.select_one('.instock.availability')
    availability = availability_element.get_text(strip=True) if availability_element else "No info"

    # Rating (e.g., "star-rating Three")
    rating_element = book.select_one('.star-rating')
    rating = rating_element.get('class')[1] if rating_element else "No rating"

    # Get the real description from the detail page
    description = get_book_description(detail_url)

    return {
        "title": title,
        "price": price,
        "availability": availability,
        "rating": rating,
        "detail_url": detail_url,
        "description": description
    }

def scrape_page(url):
    """
    Scrape all books on a single page and return a list of dictionaries.
    """
    soup = get_soup(url)
    if not soup:
        return []

    book_list = soup.select('.product_pod')
    data = []
    for book in book_list:
        book_info = parse_book_data(book)
        data.append(book_info)
    return data

def find_next_page(soup):
    """
    Check if there's a 'next' page link, and construct the full URL if it exists.
    """
    next_button = soup.select_one('.next a')
    if next_button:
        next_page_url = next_button.get('href')
        base_catalogue_url = "http://books.toscrape.com/catalogue/"
        return base_catalogue_url + next_page_url
    return None

def main():
    all_data = []
    current_url = START_URL

    while True:
        print(f"Scraping page: {current_url}")
        soup = get_soup(current_url)
        if not soup:
            break

        page_data = scrape_page(current_url)
        all_data.extend(page_data)

        next_url = find_next_page(soup)
        if next_url:
            current_url = next_url
            time.sleep(1)  # Politeness delay
        else:
            break

    # Make sure data folder exists
    os.makedirs('data', exist_ok=True)

    # Save data to CSV
    csv_path = os.path.join('data', 'books_data.csv')
    with open(csv_path, 'w', newline='', encoding='utf-8') as f:
        fieldnames = ["title", "price", "availability", "rating", "detail_url", "description"]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(all_data)

    print(f"Scraping complete! Collected {len(all_data)} books with descriptions.")

if __name__ == "__main__":
    main()
