from NaiveBayes import NaiveBayesClassifier
import nltk
import numpy as np
import csv

class SentimentAnalyzer:
    def __init__(self, file_location):
        self.features = set([])
        self.raw_data = []
        self.training_data = []
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

                self.raw_data.append((h_tokens, 0, float(row[' anger']) / 100)) # anger
                self.raw_data.append((h_tokens, 1, float(row[' disgust']) / 100)) # disgust
                self.raw_data.append((h_tokens, 2, float(row[' fear']) / 100)) # fear
                self.raw_data.append((h_tokens, 3, float(row[' joy']) / 100)) # joy
                self.raw_data.append((h_tokens, 4, float(row[' sadness']) / 100)) # sadness
                self.raw_data.append((h_tokens, 5, float(row[' surprise']) / 100)) # surprise

        for data in self.raw_data:
            f_vector = []
            for f in self.features:
                f_vector.append(1 if f in data[0] else 0)
            self.training_data.append((f_vector, data[1], data[2]))

        self.classifier = NaiveBayesClassifier(6, len(self.features))
        self.classifier.train(self.training_data)

    def predict(self, text):
        token_set = set(nltk.word_tokenize(text))
        f_vector = []
        for f in self.features:
            f_vector.append(1 if f in token_set else 0)
        return self.classifier.predict(f_vector)

    def predict_all(self, text):
        token_set = set(nltk.word_tokenize(text))
        f_vector = []
        for f in self.features:
            f_vector.append(1 if f in token_set else 0)
        return self.classifier.predict_all(f_vector)
