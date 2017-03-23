
f = open("./AffectiveText.test/affectivetext_test.xml", 'r').read().split('\n')[1:-2]

g = open("./AffectiveText.trial/affectivetext_trial.xml",
'r').read().split('\n')[1:-2]

f = f + g

filtered = []

for i in f:
    filtered.append(i.split('>')[1].split('<')[0].replace("\"", ""))

f = open("./AffectiveText.test/affectivetext_test.emotions.gold",
'r').read().split('\n')[:-1]

g = open("./AffectiveText.trial/affectivetext_trial.emotions.gold",
'r').read().split('\n')[:-1]

f = f + g

assert len(filtered) == len(f)

to_csv = []

for i in xrange(len(f)):
    to_csv.append("\"" + filtered[i] + "\", " + ", ".join(f[i].split(' ')[1:]) + '\n')

csv = open("emotion_data.csv", 'w')
csv.write("headline, anger, disgust, fear, joy, sadness, surprise\n")
for i in to_csv:
    csv.write(i)

csv.close()
