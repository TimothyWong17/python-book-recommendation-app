import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer

class BookRecommendations:
    def __init__(self, data):
        self.data = data
        
    def data_preprocessing(self):
        self.data['combined_features'] = self.data['book_title'] + self.data['book_author']
        return self.data
            
    def get_recommendations(self, book_title):
        self.data_preprocessing()
        cm = CountVectorizer().fit_transform(self.data['combined_features'])
        cs = cosine_similarity(cm)
        
        book_index = self.data[self.data['book_title'] == book_title]['index'].values[0]
        scores = list(enumerate(cs[book_index]))
        sorted_scores = sorted(scores, key=lambda x:x[1], reverse=True)
        top_5_scores = sorted_scores[1:6]
        top_5_book_recommendations = [self.data[self.data['index'] == item[0]]['book_title'].values[0] for item in top_5_scores]
        return top_5_book_recommendations            