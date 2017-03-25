from HeadlineSentiment import SentimentAnalyzer
import pickle

sentiment_lookup = ['anger', 'disgust', 'fear', 'joy', 'sadness', 'surprise']

if __name__ == "__main__":
    analyzer = SentimentAnalyzer("emotion_data.csv")

    print "Done training!"

    input = raw_input()
    while input != "exit":
        print input
        ranked_list = sorted(analyzer.predict_all(input), reverse=True, key=lambda i: i[1])
        for i in ranked_list:
            print sentiment_lookup[i[0]] + " (" + str(i[1]) + ")"
        print "======="
        input = raw_input()
