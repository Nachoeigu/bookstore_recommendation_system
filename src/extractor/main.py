import os
from dotenv import load_dotenv
import sys
import asyncio
import aiohttp
from lxml import html
import json
from urllib.parse import urljoin
import logging
import html as html_parser

# Load environment variables
load_dotenv()

WORKDIR = os.getenv("WORKDIR")
os.chdir(WORKDIR)
sys.path.append(WORKDIR)

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(message)s')

class ScrapeBooks:
    def __init__(self, base_url):
        self.base_url = base_url
        self.books = []
        self.book_urls = []

    async def fetch_page(self, session, url):
        async with session.get(url) as response:
            response.raise_for_status()
            content = await response.text()
            return content

    async def parse_catalog_page(self, session, page_number):
        catalog_url = self.base_url + f'catalogue/page-{page_number}.html'
        logging.info(f"Extracting books URLs from Home: page number {page_number} from home")
        page_content = await self.fetch_page(session, catalog_url)
        tree = html.fromstring(page_content)
        book_urls = tree.xpath('//article[@class="product_pod"]/h3/a/@href')
        book_urls = [urljoin(self.base_url, 'catalogue/' + url) for url in book_urls]
        self.book_urls.extend(book_urls)
        next_page = tree.xpath('//li[@class="next"]/a/@href')
        return bool(next_page)

    async def parse_all_catalog_pages(self):
        async with aiohttp.ClientSession() as session:
            page_number = 1
            while await self.parse_catalog_page(session, page_number):
                page_number += 1

    async def parse_book_page(self, session, book_url, book_number, total_books):
        page_content = await self.fetch_page(session, book_url)
        tree = html.fromstring(page_content)
        title = tree.xpath('//h1/text()')[0]
        logging.info(f"Extracting detailed info from book {title}")
        price = tree.xpath('//p[@class="price_color"]/text()')[0]
        availability = tree.xpath('//p[@class="instock availability"]/text()')
        availability = availability[0].strip() if availability else ""
        rating = tree.xpath('//p[contains(@class, "star-rating")]/@class')[0].split()[-1]
        description = tree.xpath('//div[@id="product_description"]/following-sibling::p/text()')
        upc = tree.xpath('//th[text()="UPC"]/following-sibling::td/text()')[0]
        product_type = tree.xpath('//th[text()="Product Type"]/following-sibling::td/text()')[0]
        price_excl_tax = tree.xpath('//th[text()="Price (excl. tax)"]/following-sibling::td/text()')[0]
        price_incl_tax = tree.xpath('//th[text()="Price (incl. tax)"]/following-sibling::td/text()')[0]
        tax = tree.xpath('//th[text()="Tax"]/following-sibling::td/text()')[0]
        number_of_reviews = tree.xpath('//th[text()="Number of reviews"]/following-sibling::td/text()')[0]
        category = tree.xpath('//ul[@class="breadcrumb"]/li/a/text()')[2]
        image_url = tree.xpath('//div[@class="item active"]/img/@src')[0]

        # Clean data
        price = float(price[1:])  # Removing currency symbol
        availability = int(''.join(filter(str.isdigit, availability))) if any(char.isdigit() for char in availability) else 0
        rating = self.convert_rating_to_number(rating)
        description = html_parser.unescape(description[0]) if description else ""
        image_url = urljoin(self.base_url, image_url)  # Make image URL absolute

        book_data = {
            "title": title,
            "price in pounds": price,
            "availability": availability,
            "rating": rating,
            "description": description,
            "UPC": upc,
            "product type": product_type,
            "price (excl. tax) in pounds": float(price_excl_tax[1:]),
            "price (incl. tax) in pounds": float(price_incl_tax[1:]),
            "tax in pounds": float(tax[1:]),
            "number of reviews": int(number_of_reviews),
            "category": category,
            "image_url": image_url
        }

        self.books.append(book_data)
        logging.info(f"We are scrapping the book number {book_number + 1}")
        scrapped_percentage = (book_number + 1) / total_books * 100
        logging.info(f"We scraped {scrapped_percentage:.2f}% of total books")

    def convert_rating_to_number(self, rating_str):
        ratings = {
            "One": 1,
            "Two": 2,
            "Three": 3,
            "Four": 4,
            "Five": 5
        }
        return ratings.get(rating_str, 0)

    def save_to_json(self, filename):
        with open(filename, 'w', encoding='utf-8') as json_file:
            json.dump(self.books, json_file, indent=4, ensure_ascii=False)

    async def scrape(self):
        await self.parse_all_catalog_pages()
        total_books = len(self.book_urls)
        async with aiohttp.ClientSession() as session:
            tasks = [
                self.parse_book_page(session, book_url, book_number, total_books)
                for book_number, book_url in enumerate(self.book_urls)
            ]
            await asyncio.gather(*tasks)
        self.save_to_json(f'{WORKDIR}/datasource/new_data.json')

if __name__ == '__main__':
    scraper = ScrapeBooks('http://books.toscrape.com/')
    asyncio.run(scraper.scrape())