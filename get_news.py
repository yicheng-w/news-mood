import requests
import json
import pickle
from HeadlineSentiment import SentimentAnalyzer

key = open("google_news.key").read()[:-1]
api_endpt = "https://newsapi.org/v1/articles?apiKey={}&source=google-news".format(key)
sentiment_lookup = ['anger', 'disgust', 'fear', 'joy', 'sadness', 'surprise']

def get_news_headlines():
    r = requests.get(api_endpt, data = {"source" : "google-news", "apiKey" : key})
    r = json.loads(r.text)
    headlines = [article['title'] for article in r['articles']]
    return headlines

analyzer = SentimentAnalyzer("emotion_data.csv")

headlines = get_news_headlines()

for headline in headlines:
    print headline
    ranked_list = sorted(analyzer.predict_all(headline), reverse=True, key=lambda i: i[1])
    for i in ranked_list:
        print sentiment_lookup[i[0]] + " (" + str(i[1]) + ")"
    print "====="
