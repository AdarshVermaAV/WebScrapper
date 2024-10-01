import tkinter as tk
from tkinter import messagebox, scrolledtext
from flask import Flask, request, jsonify, render_template
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re

app = Flask(__name__)

@app.route('/')
def documentation():
    return render_template('documentation.html')

class ScraperApp:
    def __init__(self):
        self.driver = None
        self.keywords = ["protein", "powder", "capsules", "DNA", "genes", "CODE Complex", "nutritional supplement"]

    def create_driver(self):
        options = Options()
        options.add_argument("--headless")       
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument("--incognito")
        options.add_argument("--ignore-certificate-errors")
        options.add_argument("--window-size=1920x1080")
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    def close_driver(self):
        if self.driver:
            self.driver.quit()

    def scrape_urls(self, urls):
        results = {}
        self.create_driver()

        for url in urls:
            if url:
                try:
                    self.driver.get(url)
                    WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))

                    results[url] = {
                        "paragraphs": self.extract_paragraphs(),
                        "urls": self.extract_urls(),
                        "headings": self.extract_headings(),
                        "images": self.extract_images(),
                        "list_items": self.extract_list_items(),
                        "span_texts": self.extract_span_texts(),
                        "table_data": self.extract_table_data()
                    }
                except Exception as e:
                    results[url] = {"error": str(e)}

        self.close_driver()
        return results

    def extract_paragraphs(self):
        try:
            paragraphs = self.driver.find_elements(By.TAG_NAME, 'p')
            return "\n".join(element.text for element in paragraphs)
        except Exception as e:
            return f"Error fetching paragraphs: {str(e)}"

    def extract_urls(self):
        try:
            link_elements = self.driver.find_elements(By.TAG_NAME, 'a')
            urls = [link.get_attribute('href') for link in link_elements if link.get_attribute('href')]
            return self.filter_referral_urls(urls)
        except Exception as e:
            return f"Error fetching URLs: {str(e)}"

    def extract_headings(self):
        try:
            heading_elements = self.driver.find_elements(By.TAG_NAME, 'h1')
            return [heading.text for heading in heading_elements]
        except Exception as e:
            return f"Error fetching headings: {str(e)}"

    def extract_images(self):
        try:
            image_elements = self.driver.find_elements(By.TAG_NAME, 'img')
            return [img.get_attribute('src') for img in image_elements if img.get_attribute('src')]
        except Exception as e:
            return f"Error fetching images: {str(e)}"

    def extract_list_items(self):
        try:
            list_elements = self.driver.find_elements(By.TAG_NAME, 'li')
            return [item.text for item in list_elements]
        except Exception as e:
            return f"Error fetching list items: {str(e)}"

    def extract_span_texts(self):
        try:
            span_elements = self.driver.find_elements(By.TAG_NAME, 'span')
            return [span.text for span in span_elements]
        except Exception as e:
            return f"Error fetching span texts: {str(e)}"

    def extract_table_data(self):
        try:
            table_elements = self.driver.find_elements(By.TAG_NAME, 'table')
            table_data = []
            for table in table_elements:
                rows = table.find_elements(By.TAG_NAME, 'tr')
                for row in rows:
                    cells = row.find_elements(By.TAG_NAME, 'td')
                    cell_data = [cell.text for cell in cells]
                    table_data.append(cell_data)
            return table_data
        except Exception as e:
            return f"Error fetching table data: {str(e)}"

    def filter_referral_urls(self, urls):
        filtered_urls = []
        pattern = re.compile(r'https://(.*?snipnutrition\.com|.*?\.snipnutrition\.com|snipnutrition\.com/.*?)')
        for url in urls:
            if pattern.search(url):
                filtered_urls.append(url)
        return filtered_urls


@app.route('/scrape', methods=['POST'])
def scrape():
    data = request.get_json()
    urls = data.get('urls', [])

    if not urls:
        return jsonify({"error": "No URLs provided"}), 400

    scraper = ScraperApp()
    results = scraper.scrape_urls(urls)
    return jsonify(results)


if __name__ == "__main__":
    app.run(debug=True)
