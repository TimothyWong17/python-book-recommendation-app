import requests 
from bs4 import BeautifulSoup
import csv
import pandas as pd
from datetime import datetime, date

class GoodBooksWebScrapper:
    def __init__(self):
        self.url = "https://www.goodbooks.io"
        self.data = {}
        
    def get_num_pages(self):
        r = requests.get(f"{self.url}/books")
        soup = BeautifulSoup(r.text, 'html.parser')
        total_pages = soup.find("div", {"class": "w-page-count page-count"}).text.split("/")[1].strip()
        return int(total_pages)
    
    def getBooks(self):
        for page in range(1, self.get_num_pages()+1): 
            url = f"{self.url}/books/?216112dc_page={page}"
            print(f"Scraping {url}")
            r = requests.get(url)
            soup = BeautifulSoup(r.text, 'html.parser')
            page_of_books = soup.findAll("div", {"id": "w-node-f88415e9-91c8-01b5-4b50-f9a0216112de-85bf548e"})
            for book in page_of_books:
                hash = {}
                book_title = book.find("a", {"class": "link-no-underline w-inline-block"}).h5.text.strip()
                book_author = book.find("a", {"class": "link-no-underline w-inline-block"}).h6.text.strip()
                book_detail_page = book.find("a", {"class": "link-no-underline w-inline-block"})['href']
                r = requests.get(f"{self.url}{book_detail_page}")
                print( f"Scraping Book: {book_title}, Book Url: {self.url}{book_detail_page}")
                soup = BeautifulSoup(r.text, 'html.parser')
                book_description =  soup.find("div", {"class": "book-summary w-richtext"}).text.strip() if soup.find("div", {"class": "book-summary w-richtext"}) is not None else None 
                book_categories = [cat.text.strip() for cat in soup.find("div", {"class": "category-badges w-dyn-list"}).findAll("div", {"class": "w-dyn-item"})]
                update_dt = soup.find("div", {"class": "text-small margin w-embed"}).text.split("Updated")[1].strip()
                update_dt = datetime.strptime(update_dt, '%b %d, %Y')
                book_likes = int(soup.find("div", {"class": "section-title"}).h2.text.split("recommendations")[0])
                
                hash["book_author"] = book_author
                hash["book_detail_page"] = book_detail_page
                hash["book_description"] = book_description
                hash["book_categories"] = book_categories
                hash["update_dt"] = update_dt
                hash["book_likes"] = book_likes
                
                self.data[book_title] = hash                

                #Save data to CSV
        with open('data/good_books_data.csv', 'w', newline='') as csvfile:
            columns = ['book_title', 'book_author', 'book_detail_page', 'book_description', 'book_categories', 'book_likes', 'update_dt']
            writer = csv.DictWriter(csvfile, fieldnames=columns)

            # Write header
            writer.writeheader()

            # Write data
            print("Writing Data to CSV")
            for row_key, inner_dict in self.data.items():
                row_data = {'book_title': row_key, **inner_dict}
                writer.writerow(row_data)
                
        return self.data
    