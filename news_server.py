from flask import Flask, render_template
import requests
import dill
from HeadlineSentiment import SentimentAnalyzer
import json
import os
from database import DBManager
import constants as c

app = Flask(__name__)
db_manager = DBManager()

sentiment_lookup = ['anger', 'disgust', 'fear', 'joy', 'sadness', 'surprise']
key = open("google_news.key").read()[:-1]
api_endpt = "https://newsapi.org/v1/articles?apiKey={}&source=google-news".format(key)

def get_news():
    response_dict = {}
    r = requests.get(api_endpt, data = {"source" : "google-news", "apiKey" : key})
    r = json.loads(r.text)
    sentiment_tally = [0, 0, 0, 0, 0, 0]
    h_data = []
    for article in r['articles']:
        headline = article['title']
        data = {'headline': headline}
        ranked_list = sorted(analyzer.predict_all(headline), reverse=True, key=lambda i: i[1])
        data['primary_emotion'] = sentiment_lookup[ranked_list[0][0]]
        data['other_emotions'] = [sentiment_lookup[ranked_list[1][0]], sentiment_lookup[ranked_list[2][0]]]
        sentiment_tally[ranked_list[0][0]] += 1
        sentiment_tally[ranked_list[1][0]] += 0.75
        sentiment_tally[ranked_list[2][0]] += 0.5
        for i in ranked_list:
            data[sentiment_lookup[i[0]]] = i[1]
        data['url'] = article['url']
        data['description'] = article['description']
        data['author'] = article['author']
        data['h_id'] = db_manager.add_headline(headline)
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

### api endpts
@app.route("/react/<h_id>/<emotion>/")
def add_feedback(h_id, emotion):
    print("FEEDBACK! on " + str(h_id) + ": " + emotion)
    db_manager.add_emotion(h_id, c.sentiment_lookup_reverse[emotion])
    return json.dumps({"result" : "success"})

if __name__ == "__main__":
    print "Training..."
    analyzer = SentimentAnalyzer("emotion_data.csv")
    f = open("analyzer.dill", 'wb')
    dill.dump(analyzer, f)
    print "Done!"

    app.run(host="0.0.0.0", port=11235)
