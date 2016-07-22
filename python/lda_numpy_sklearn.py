# !/usr/bin/env python
# -*- coding: utf8 -*-

import os
import sys
import lda
import numpy as np
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import CountVectorizer

corpus_files = sys.argv[1]
stopwords = stopwords.words('english') + stopwords.words('french') + stopwords.words('german')

filenames = []
for root, dirs, files in os.walk(corpus_files):
	for file in files:
		filenames.append(os.path.join(root, file))

vectorizer = CountVectorizer(input='filename', stop_words=stopwords)
dtm = vectorizer.fit_transform(filenames)
vocab = vectorizer.get_feature_names()

dtm = dtm.toarray()
vocab = np.array(vocab)

model = lda.LDA(n_topics=20, n_iter=500, random_state=1)
model.fit(dtm)

topic_word = model.topic_word_
n = 20
for i, topic_dist in enumerate(topic_word):
    topic_words = np.array(vocab)[np.argsort(topic_dist)][:-(n+1):-1]
    toprint = u'*Topic {}\n- {}'.format(i, ' '.join(topic_words))
    print toprint

# doc_topic = model.doc_topic_
# for n in range(10):
#     topic_most_pr = doc_topic[n].argmax()
#     print("doc: {} topic: {}".format(n, topic_most_pr))


