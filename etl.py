import pandas as pd
import os
import re
import sqlite3
from goodbooks_web_scrapper import GoodBooksWebScrapper

def extract():
    GoodBooksWebScraper = GoodBooksWebScrapper()
    book_data = GoodBooksWebScraper.getBooks()
    df = pd.DataFrame.from_dict(data=book_data, orient='index')
    df = df.reset_index()
    df = df.rename(columns={'index': 'book_title'})
    return df

def transform(data):
    data['book_categories'] = data['book_categories'].apply(lambda x: ', '.join(x))
    data['book_description'] = data['book_description'].str.encode('ascii', 'ignore').str.decode('ascii')    
    return data


def load_to_sqlite(data):
    conn = sqlite3.connect('db/db_books')
    print("Writing to DB")
    data.to_sql('books', con=conn, if_exists='replace')
    conn.commit()
    conn.close()

def main():
    df = extract()
    df = transform(df)
    load_to_sqlite(df)
    
    
if __name__ == "__main__":
    main()