import csv
import numpy as np
import nltk

features = []
inv_features = {}
sentiment_lookup = ['anger', 'disgust', 'fear', 'joy', 'sadness', 'surprise']
feature_size = 18
output_size = 6
train_data = None
train_data_size = 0
train_data_cursor = 0
train_data_reader = None

def set_train_file_loc(path):
    global train_data_reader, train_data_size, train_data_cursor, features
    train_data = open(path, 'rb')
    train_data_reader = list(csv.DictReader(train_data))
    train_data_size = len(train_data_reader)

    word_freq = {}
    for row in train_data_reader:
        h_tokens = nltk.word_tokenize(row['headline'].lower())

        for token in h_tokens:
            if token in word_freq:
                word_freq[token] += 1
            else:
                word_freq[token] = 1

    features = sorted(word_freq.keys(), key=word_freq.get)[-1000:]
    inv_features = {}

    for i in xrange(len(features)):
        inv_features[features[i]] = i

def get_batch(batch_size):
    global train_data_cursor
    x = np.empty((batch_size, feature_size))
    y = np.empty((batch_size, output_size))

    for i in xrange(batch_size):
        row = train_data_reader[(i + train_data_cursor) % train_data_size]
        h_tokens = nltk.word_tokenize(row['headline'].lower())
        y[i, :] = (float(row[' anger']) / 100,
                   float(row[' disgust']) / 100,
                   float(row[' fear']) / 100,
                   float(row[' joy']) / 100,
                   float(row[' sadness']) / 100,
                   float(row[' surprise']) / 100)

        f_vector = []
        for token in h_tokens:
            if token in inv_features:
                f_vector.append(inv_features[token])
            else:
                f_vector.append(-1)

        while (len(f_vector) < 18):
            f_vector.append(-2)

        x[i, :] = f_vector

    train_data_cursor = (train_data_cursor + batch_size) % train_data_size

    return x, y

def read_test(file_location, rows_to_take = -1):
    with open(file_location, 'rb') as data:
        data_reader = csv.DictReader(data)
        data_reader = list(data_reader)

        if rows_to_take == -1:
            rows_to_take = len(data_reader)

        y = np.empty((rows_to_take, 6))
        x = np.empty((rows_to_take, 18))

        i = 0

        for row in data_reader:
            h_tokens = nltk.word_tokenize(row['headline'].lower())
            y[i, :] = (float(row[' anger']) / 100,
                       float(row[' disgust']) / 100,
                       float(row[' fear']) / 100,
                       float(row[' joy']) / 100,
                       float(row[' sadness']) / 100,
                       float(row[' surprise']) / 100)

            f_vector = []
            for token in h_tokens:
                if token in inv_features:
                    f_vector.append(inv_features[token])
                else:
                    f_vector.append(-1)

            while (len(f_vector) < 18):
                f_vector.append(-2)

            x[i, :] = f_vector

            i += 1

        return x,y

def compute_input_vec(headline):
    h_tokens = nltk.word_tokenize(headline.lower())

    x = np.empty((18, 1, 1))

    f_vector = []
    for token in h_tokens:
        if token in inv_features:
            f_vector.append(inv_features[token])
        else:
            f_vector.append(-1)

    while (len(f_vector) < 18):
        f_vector.append(-2)

    x[:,0,0] = f_vector

    return x

