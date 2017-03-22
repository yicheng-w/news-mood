from bayesAnalyzer import NaiveBayesianTextAnalyzer
from os import listdir, system
from sys import argv
import pickle
from multiprocessing import Pool
from functools import reduce

if __name__ == "__main__":
    analyzer = NaiveBayesianTextAnalyzer()

    if argv[1] == "train":
        system("echo -n 'Loading Data: ['")
        files = listdir("./train/pos")
        total = len(files) * 2
        done = 0.
        for i in files:
            if (done / total > 1. / 10):
                system("echo -n '='")
                done = 0.
            f = open('./train/pos/' + i, 'r').read()
            analyzer.add_training_data(f, 1)
            done+=1
        files = listdir('./train/neg')
        for i in files:
            if (done / total > 1. / 10):
                system("echo -n '='")
                done = 0.
            f = open('./train/neg/' + i, 'r').read()
            analyzer.add_training_data(f, 0)

        system("echo -n ']\t\t[done]\n'")

        system("echo -n 'Training...'")

        analyzer.train()

        system("echo -n '\t\t[done]\n'")

#        analyzer.save(argv[2])
#
#    elif argv[1] == "test":
#        analyzer.load(argv[2])

        total = 0
        correct = 0

        files = listdir("./test/pos")
        #pool = Pool()

        #correct = reduce(lambda t, p: t + 1 if p == 1 else t, pool.map(lambda f: analyzer.predict(open("./test/pos/" + f, 'r').read())[0], files), 0)

        for i in files:
            f = open("./test/pos/" + i, 'r').read()
            if analyzer.predict(f)[0] == 1:
                correct += 1
            total += 1
            if total % 100 == 0:
                print total

        files = listdir("./test/neg")

        #correct = reduce(lambda t, p: t + 1 if p == 0 else t, pool.map(lambda f: analyzer.predict(open("./test/neg/" + f, 'r').read())[0], files), 0)
        for i in files:
            f = open("./test/neg/" + i, 'r').read()
            if analyzer.predict(f)[0] == 0:
                correct += 1
            total += 1
            if total % 100 == 0:
                print total

        print "Accuracy: %.2f" % (float(correct) / total)

