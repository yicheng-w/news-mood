import numpy as np
import math

class Outcome:
    def __init__(self, f_count):
        self.n = 0
        self.distribution = np.zeros(f_count)

    def resize_features(self, new_f_count):
        self.distribution.resize(new_f_count)

    def add_sample(self, f_array, probability = 1):
        self.distribution += np.multiply(f_array, probability)
        self.n += 1

    def predict(self, f_array):
        #result = 1
        result = math.log(1)
        for i in xrange(self.n):
            prob = math.log(1. + self.distribution.take(i)) - math.log(self.distribution.size + self.n)
            if f_array[i]:
                result += prob
            else:
                result += math.log(self.distribution.size + self.n - 1. - self.distribution.take(i)) - math.log(self.distribution.size + self.n)
            #probability = (1. + self.distribution.take(i)) / (self.distribution.size + self.n)
            #if f_array[i]:
            #    result *= probability
            #else:
            #    result *= (1 - probability)

        return result
        #probs = [self.distribution.take(i) / self.n
        #            if f_array[i]
        #            else 1 - self.distribution.take(i) / self.n
        #                for i in xrange(self.n)]
        #return reduce(lambda x,y: x * y, probs)

class NaiveBayesClassifier:
    def __init__(self, outcome_count, feature_count):
        self.outcomes = [Outcome(feature_count) for i in xrange(outcome_count)]
        self.sample_size = 0

    def fit(self, feature_vector, outcome_id, prob = 1):
        self.outcomes[outcome_id].add_sample(feature_vector, prob)
        self.sample_size += 1

    def train(self, inputs):
        for (data, outcome, prob) in inputs:
            self.fit(data, outcome, prob)

    def predict(self, data):
        outcome_id = -float('inf')
        outcome_probs = -float('inf')
        for i in xrange(len(self.outcomes)):
            #i_prob = float(self.outcomes[i].n) / self.sample_size * self.outcomes[i].predict(data)
            i_prob = math.log(self.outcomes[i].n) - math.log(self.sample_size) + self.outcomes[i].predict(data)
            if i_prob > outcome_probs:
                outcome_probs = i_prob
                outcome_id = i

        return (outcome_id, outcome_probs)

    def predict_all(self, data):
        result_vector = []
        for i in xrange(len(self.outcomes)):
            i_prob = float(self.outcomes[i].n) / self.sample_size * self.outcomes[i].predict(data)
            result_vector.append((i, i_prob))

        return result_vector

    def set_feature_count(self, new_f_count):
        map(lambda o: o.resize_features(new_f_count), self.outcomes)
