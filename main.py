import bs4
import requests
from twitterscraper import query_tweets
import datetime as dt
import nltk
import glob, os
from nltk.corpus import stopwords 
from nltk.stem import PorterStemmer 
from nltk import word_tokenize
import csv
import re
from textblob import TextBlob
from sklearn.feature_extraction.text import TfidfVectorizer

# function to retrieve list of current playing movies
def get_recent_movies():
    # Link to scrape the data 
    url = "https://www.imdb.com/chart/boxoffice/?ref_=hm_cht_sm"
    response = requests.get(url)
    content = bs4.BeautifulSoup(response.content, "html.parser")
    # Find td class named titleColumn and store into movie
    movie = content.findAll('td',{'class','titleColumn'})
    # For each movie 
    for movie_name in movie:
        # Remove spaces and passes movie name into get_tweets
        get_tweets(str(movie_name.find("a").text).replace(" ", ""))

# function to retrieve tweets
def get_tweets(movie):
    # Starting date
    begin_date = dt.date(2020,3,19)

    # Ending date
    end_date = dt.date(2020,3,21)
    limit = 1
    lang = 'english'
    
    # Hashtag to search 
    hashtag = "#" + movie

    # Filename to save 
    filename = movie + ".txt"
    # Create and save file in filename
    files = open(filename, 'w', encoding='utf8')

    # Calls twitter scraper library to look for tweets
    tweets = query_tweets(hashtag, begindate = begin_date, enddate = end_date, limit = limit, lang = lang)
    # Each tweet returned
    for t in tweets:

        # Remove mentions and link from data
        t.text = re.sub(r"(?:\@|https?\://)\S+", "", t.text)
        # Remove media url from data
        t.text = re.sub(r"pic.twitter.com\S+", "", t.text)

        # If tweet is classified as English, save to the file
        if TextBlob(t.text).detect_language() == 'en':
            files.write(t.text + "\n")
    files.close()

# Function to preprocess csv file
def preprocess(location,name):
    # Filename to save 
    filename = name[:-4] + "_new.txt"
    # Create and save file in filename
    files = open(filename, 'w', encoding='utf8')

    # Import stemmer
    ps = PorterStemmer()
    # Import list from NLTK library that contains stop words
    stop_words = set(stopwords.words('english'))
    # Open and reads file and split it into objects
    words = open(location,encoding='utf8').read().split()

    # Loop to go through list of words
    for word in words: 
        # Check in word is a stop word
        if not word in stop_words:
            # Calls the porter algo to stem
            files.write(ps.stem(word) + " ")
    files.close()

# Function to train model using SVM
def train():
    with open("C:\\Users\\Jian\\Desktop\\Movie-Tweet-Analyzer\\dataset.csv", 'r') as csvfile: 
        csvreader = csv.reader(csvfile)
        for row in csvreader:
            review = row[0]
            sentiment = row[1]

            # TO DO
            # Vectorization
            vectorizer = TfidfVectorizer
            

if __name__ == '__main__':
    #get_recent_movies()
    # Location to look for txt files
    for file in os.listdir("C:\\Users\\Jian\\Desktop\\Movie-Tweet-Analyzer\\"):
        if file.endswith(".txt"):
            # Pass in file location for every CSV file found
            preprocess(os.path.join("C:\\Users\\Jian\\Desktop\\Movie-Tweet-Analyzer\\", file),file)
    #train()