from flask import Flask, render_template
import requests
import dill
from HeadlineSentiment import SentimentAnalyzer
import json
import os

app = Flask(__name__)

sentiment_lookup = ['anger', 'disgust', 'fear', 'joy', 'sadness', 'surprise']
key = open("google_news.key").read()[:-1]
api_endpt = "https://newsapi.org/v1/articles?apiKey={}&source=google-news".format(key)
sentiment_lookup = ['anger', 'disgust', 'fear', 'joy', 'sadness', 'surprise']

def get_news():
    response_dict = {}
    r = requests.get(api_endpt, data = {"source" : "google-news", "apiKey" : key})
    r = json.loads(r.text)
    headlines = [article['title'] for article in r['articles']]
    sentiment_tally = [0, 0, 0, 0, 0, 0]
    h_data = []
    for article in r['articles']:
        headline = article['title']
        data = {'headline': headline}
        ranked_list = sorted(analyzer.predict_all(headline), reverse=True, key=lambda i: i[1])
        data['primary_emotion'] = sentiment_lookup[ranked_list[0][0]]
        sentiment_tally[ranked_list[0][0]] += 1
        for i in ranked_list:
            data[sentiment_lookup[i[0]]] = i[1]
        data['url'] = article['url']
        data['description'] = article['description']
        data['author'] = article['author']
        h_data.append(data)

    dominant_feel = -1
    dominant_count = -1
    for i in xrange(len(sentiment_tally)):
        if sentiment_tally[i] > dominant_count:
            dominant_count = sentiment_tally[i]
            dominant_feel = i

    return {'dominant_sentiment': sentiment_lookup[dominant_feel],
            'articles': h_data}

@app.route("/api/news_feels")
def api_news():
    return json.dumps(get_news())

@app.route("/")
def root():
    news = get_news()
    return render_template("main.html", news=news)

if __name__ == "__main__":
    print "Training..."
    analyzer = SentimentAnalyzer("emotion_data.csv")
    f = open("analyzer.dill", 'wb')
    dill.dump(analyzer, f)
    print "Done!"

    app.run(host="0.0.0.0", port=11235)
