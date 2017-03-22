import numpy as np

class Outcome:
    def __init__(self, f_count):
        self.n = 0
        self.distribution = np.zeros(f_count)

    def resize_features(self, new_f_count):
        self.distribution.resize(new_f_count)

    def add_sample(self, f_array):
        self.distribution += f_array
        self.n += 1

    def predict(self, f_array):
        probs = [self.distribution.take(i) / self.n
                    if f_array[i]
                    else 1 - self.distribution.take(i) / self.n
                        for i in xrange(self.n)]
        return reduce(lambda x,y: x * y, probs)

class NaiveBayesClassifier:
    def __init__(self, outcome_count, feature_count):
        self.outcomes = [Outcome(feature_count) for i in xrange(outcome_count)]
        self.sample_size = 0

    def fit(self, feature_vector, outcome_id):
        self.outcomes[outcome_id].add_sample(feature_vector)
        self.sample_size += 1

    def train(self, inputs):
        for (data, outcome) in inputs:
            self.fit(data, outcome)

    def predict(self, data):
        outcome_id = -1
        outcome_probs = -1
        for i in xrange(len(self.outcomes)):
            try:
                i_prob = float(self.outcomes[i].n) / self.sample_size * self.outcomes[i].predict(data)
            except IndexError:
                print i
            if i_prob > outcome_probs:
                outcome_probs = i_prob
                outcome_id = i

        return (outcome_id, outcome_probs)

    def set_feature_count(self, new_f_count):
        map(lambda o: o.resize_features(new_f_count), self.outcomes)
