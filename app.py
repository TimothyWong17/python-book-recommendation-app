from flask import Flask, render_template, request, url_for
import pandas as pd
from db import DB
from book_recommendations import BookRecommendations



app = Flask(__name__)
    
def getRecommendations(user_input_book_title):
    sqlite_db = DB('db/db_books')
    df = sqlite_db.get_table_data('books')
    BookRecommendation = BookRecommendations(df)
    top_5_book_title_recommendations = BookRecommendation.get_recommendations(user_input_book_title)
    book_recommendations = df[df['book_title'].isin(top_5_book_title_recommendations)]
    return book_recommendations


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/recommendations', methods=['POST'])
def recommendations():
    book_title = request.form['book-title']
    data = getRecommendations(book_title)    
    book_titles = data['book_title'].values
    book_authors = data['book_author'].values
    data = [(book_titles[i], book_authors[i]) for i in range(0, len(book_titles))]
    return render_template('index.html', data=data)




if __name__ == "__main__":
    app.run(debug=True)
    