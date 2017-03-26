import requests
import json
import dill
from HeadlineSentiment import SentimentAnalyzer
import os

key = open("google_news.key").read()[:-1]
api_endpt = "https://newsapi.org/v1/articles?apiKey={}&source=google-news".format(key)
sentiment_lookup = ['anger', 'disgust', 'fear', 'joy', 'sadness', 'surprise']

def get_news_headlines():
    r = requests.get(api_endpt, data = {"source" : "google-news", "apiKey" : key})
    r = json.loads(r.text)
    headlines = [article['title'] for article in r['articles']]
    return headlines

if __name__ == "__main__":
    if "analyzer.dill" not in os.listdir('.'):
        print "Training..."
        analyzer = SentimentAnalyzer("emotion_data.csv")
        f = open("analyzer.dill", 'wb')
        dill.dump(analyzer, f)
        print "Done!"
    else:
        print "Loading analyzer..."
        with open("analyzer.dill", 'rb') as f:
            analyzer = dill.load(f)
        print "Done!"

    headlines = get_news_headlines()

    for headline in headlines:
        print headline
        ranked_list = sorted(analyzer.predict_all(headline), reverse=True, key=lambda i: i[1])
        for i in ranked_list:
            print sentiment_lookup[i[0]] + " (" + str(i[1]) + ")"
        print "====="
