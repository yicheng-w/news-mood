import nltk
import os
import pickle
import math
import numpy as np
import matplotlib.pyplot as plt
from NaiveBayes import NaiveBayesClassifier

def acceptable_chars(char):
    order = ord(char)
    return ((order >= 48 and order <= 57) or
            (order >= 65 and order <= 90) or
            (order >= 97 and order <= 122) or
            order == 9 or order == 32)

def clean_text(text):
    result = ""
    for i in text:
        if (acceptable_chars(i)):
            result += i
    return result



class NaiveBayesianTextAnalyzer:
    threshold = 50

    def __init__(self):
        self.classifier = NaiveBayesClassifier(2, 0)
        self.features = {} # hashmap of features to freq
        self.raw_data = [] # list of (set(token), outcome) tuples
        self.feature_list = []

    def add_training_data(self, text, outcome):
        token_set = set([])
        for token in nltk.word_tokenize(clean_text(text)):
            if token not in token_set:
                if token in self.features:
                    self.features[token] += 1
                else:
                    self.features[token] = 1
                token_set.add(token)

        self.raw_data.append((token_set, outcome))

    def train(self):
        self.feature_list = [key for key in self.features
                                if self.features[key] > self.threshold]

        self.classifier.set_feature_count(len(self.feature_list))

        for (tokens, outcome) in self.raw_data:
            f_vector = np.zeros(len(self.feature_list))
            for i in xrange(len(self.feature_list)):
                f_vector[i] = 1 if self.feature_list[i] in tokens else 0
            self.classifier.fit(f_vector, outcome)

    def save(self, location):
        with open(location, 'wb') as f:
            pickle.dump(self.classifier, f)

    def load(self, location):
        with open(location, 'rb') as f:
            self.classifier = pickle.load(f)

    def predict(self, text):
        token_set = set(nltk.word_tokenize(clean_text(text)))
        f_vector = np.zeros(len(self.feature_list))
        for i in xrange(len(self.feature_list)):
            f_vector[i] = 1 if self.feature_list[i] in token_set else 0
        return self.classifier.predict(f_vector)
