import requests
from bs4 import BeautifulSoup

class AmazonProductScraper:
    """
    A class to scrape product data from Amazon.
    """

    def __init__(self, url):
        """
        Initialize the scraper with the provided URL.

        Args:
            url (str): The URL of the Amazon product page.
        """
        self.url = url
        self.soup = None

    def fetch_page(self):
        """
        Fetch the HTML content of the product page.
        """
        response = requests.get(self.url)
        self.soup = BeautifulSoup(response.text, 'html.parser')

    def extract_product_sku(self):
        """
        Extract the product SKU from the page.

        Returns:
            str: The product SKU, or None if not found.
        """
        sku_header = self.soup.find('th', string='ASIN')
        if sku_header:
            sku = sku_header.find_next_sibling('td').text.strip()
            return sku
        return None

    def extract_product_name(self):
        """
        Extract the product name from the page.

        Returns:
            str: The product name, or None if not found.
        """
        name_element = self.soup.find('span', id='productTitle')
        if name_element:
            name = name_element.text.strip()
            return name
        return None

    def extract_product_description(self):
        """
        Extract the product description from the page.

        Returns:
            str: The product description, or None if not found.
        """
        description_element = self.soup.find('div', id='productDescription')
        if description_element:
            description = description_element.text.strip()
            return description
        return None

    def extract_product_image_url(self):
        """
        Extract the main product image URL from the page.

        Returns:
            str: The main product image URL, or None if not found.
        """
        image_element = self.soup.find('img', id='landingImage')
        if image_element:
            image_url = image_element['src']
            return image_url
        return None

    def extract_other_product_image_urls(self):
        """
        Extract the URLs of other product images from the page.

        Returns:
            list: A list of other product image URLs, or an empty list if not found.
        """
        other_images = []
        image_thumbnails = self.soup.find_all('img', class_='a-thumbnail-image')
        for thumbnail in image_thumbnails:
            other_images.append(thumbnail['src'])
        return other_images

    def extract_price(self):
        """
        Extract the product price from the page.

        Returns:
            str: The product price, or None if not found.
        """
        price_element = self.soup.find('span', class_='a-price-whole')
        if price_element:
            price = price_element.text.strip()
            return price
        return None

    def extract_discounted_price(self):
        """
        Extract the discounted product price from the page.

        Returns:
            str: The discounted product price, or regular price if not found.
        """
        discounted_price_element = self.soup.find('span', class_='a-price a-text-price a-size-base')
        if discounted_price_element:
            discounted_price = discounted_price_element.find('span', class_='a-offscreen').text.strip()
            return discounted_price
        return self.extract_price()

    def extract_category(self):
        """
        Extract the product category breadcrumb from the page.

        Returns:
            str: The product category breadcrumb, or None if not found.
        """
        breadcrumb_element = self.soup.find('div', id='wayfinding-breadcrumbs_container')
        if breadcrumb_element:
            categories = [li.text.strip() for li in breadcrumb_element.find_all('li')]
            return ' > '.join(categories)
        return None

    def scrape_product_data(self):
        """
        Scrape all the product data from the page.

        Returns:
            dict: A dictionary containing the extracted product data.
        """
        self.fetch_page()
        product_data = {
            'sku': self.extract_product_sku(),
            'name': self.extract_product_name(),
            'description': self.extract_product_description(),
            'image_url': self.extract_product_image_url(),
            'other_image_urls': self.extract_other_product_image_urls(),
            'price': self.extract_price(),
            'discounted_price': self.extract_discounted_price(),
            'category': self.extract_category()
        }
        return product_data

# Example usage
url = 'https://www.amazon.com/dp/B07X6C9RMF'
scraper = AmazonProductScraper(url)
product_data = scraper.scrape_product_data()
print(product_data)