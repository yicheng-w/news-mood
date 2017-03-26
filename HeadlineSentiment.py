from NaiveBayes import NaiveBayesClassifier
import nltk
import numpy as np
import csv

class SentimentAnalyzer:
    def __init__(self, file_location):
        self.features = set([])
        raw_data = []
        training_data = []
        #self.word_freq = {}
        with open(file_location, 'rb') as data:
            data_reader = csv.DictReader(data)
            for row in data_reader:
                # print row
                h_tokens = nltk.word_tokenize(row['headline'].lower())
                self.features = self.features.union(set(h_tokens))

                #for token in h_tokens:
                #    if token in self.word_freq:
                #        self.word_freq[token] += 1
                #    else:
                #        self.word_freq[token] = 1

                raw_data.append((h_tokens, 0, float(row[' anger']) / 100)) # anger
                raw_data.append((h_tokens, 1, float(row[' disgust']) / 100)) # disgust
                raw_data.append((h_tokens, 2, float(row[' fear']) / 100)) # fear
                raw_data.append((h_tokens, 3, float(row[' joy']) / 100)) # joy
                raw_data.append((h_tokens, 4, float(row[' sadness']) / 100)) # sadness
                raw_data.append((h_tokens, 5, float(row[' surprise']) / 100)) # surprise

        for data in raw_data:
            f_vector = []
            for f in self.features:
                f_vector.append(1 if f in data[0] else 0)
            training_data.append((f_vector, data[1], data[2]))

        self.classifier = NaiveBayesClassifier(6, len(self.features))
        self.classifier.train(training_data)

    def predict(self, text):
        token_set = set(nltk.word_tokenize(text.lower()))
        f_vector = []
        for f in self.features:
            f_vector.append(1 if f in token_set else 0)
        return self.classifier.predict(f_vector)

    def predict_all(self, text):
        token_set = set(nltk.word_tokenize(text.lower()))
        f_vector = []
        for f in self.features:
            f_vector.append(1 if f in token_set else 0)
        return self.classifier.predict_all(f_vector)

    def test(self, test_file_location):
        test_data = open(test_file_location, 'rb')
        test_reader = csv.DictReader(test_data)
        total = 0
        correct = 0

        for row in test_reader:
            total += 1
            emotions = map(float, [row[' anger'], row[' disgust'], row[' fear'], row[' joy'], row[' sadness'], row[' surprise']])
            acceptable_emotions = []
            for i in xrange(len(emotions)):
                if emotions[i] > 1:
                    acceptable_emotions.append(i)
            acceptable_emotions = sorted(acceptable_emotions,
                    reverse=True, key=lambda x: emotions[x])
 
            #print acceptable_emotions
            #print emotion
            prediction = self.predict(row['headline'])[0]
            #print prediction

            if prediction in acceptable_emotions:
                correct+=1

        return float(correct) / total


if __name__ == "__main__":
    analyzer = SentimentAnalyzer("emotion_data.csv")
    print analyzer.test("emotion_data_test.csv")
