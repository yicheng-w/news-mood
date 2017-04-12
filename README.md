# News Mood
Monitor of mood of current headlines, the web frontend is up (and collecting data) on http://hatch01.cs.unc.edu:11235

News provided by www.newsapi.org

Sentiment classification is done via 6 one-vs-rest naive Bayes classifiers (one for each emotion)

# Data
Originally trained with data from Rada Mihalcea's (EECS @ UMich) [Affective Text database](https://web.eecs.umich.edu/~mihalcea/downloads.html).

Currently collecting more data on the live site.

# Results / Accuracy
Due to limited data for a multiclass classifier (6 outcomes with ~1250 lines of data), the accuracy is not very high right now.

With 3-fold cross validation the accuracy (as measured by the "correct" emotion being the top 3 returned by the model) is approximately 72%.
