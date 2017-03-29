from flask import Flask, render_template
import requests
import dill
from HeadlineSentiment import SentimentAnalyzer
from get_news import get_news_headlines
import json
import os

app = Flask(__name__)

sentiment_lookup = ['anger', 'disgust', 'fear', 'joy', 'sadness', 'surprise']

def get_news():
    response_dict = {}
    headlines = get_news_headlines()
    sentiment_tally = [0, 0, 0, 0, 0, 0]
    h_data = []
    for headline in headlines:
        data = {'headline': headline}
        ranked_list = sorted(analyzer.predict_all(headline), reverse=True, key=lambda i: i[1])
        data['primary_emotion'] = sentiment_lookup[ranked_list[0][0]]
        sentiment_tally[ranked_list[0][0]] += 1
        for i in ranked_list:
            data[sentiment_lookup[i[0]]] = i[1]
        h_data.append(data)

    dominant_feel = -1
    dominant_count = -1
    for i in xrange(len(sentiment_tally)):
        if sentiment_tally[i] > dominant_count:
            dominant_count = sentiment_tally[i]
            dominant_feel = i

    return {'dominant_sentiment': sentiment_lookup[dominant_feel],
            'headlines': h_data}

@app.route("/api/news_feels")
def api_news():
    return json.dumps(get_news())

@app.route("/")
def root():
    news = get_news()
    return render_template("main.html", emotion=news['dominant_sentiment'])

if __name__ == "__main__":
    print "Training..."
    analyzer = SentimentAnalyzer("emotion_data.csv")
    f = open("analyzer.dill", 'wb')
    dill.dump(analyzer, f)
    print "Done!"

    app.run(host="0.0.0.0", port=11235)
