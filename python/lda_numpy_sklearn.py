# !/usr/bin/env python
# -*- coding: utf8 -*-

import os
import sys
import lda
import csv
import math
import numpy as np
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import CountVectorizer

# takes a folder of text files
corpus_files = sys.argv[1]

# csv output for the win
csv_doctopic = open("lda_docXtopic.csv", 'w')
csv_topicwords = open("lda_topicXwords.csv", 'w')

# stopwords from nltk
stopwords = stopwords.words('english') + stopwords.words('french') + stopwords.words('german')

# get files path from folder
filenames = []
for root, dirs, files in os.walk(corpus_files):
	for file in files:
		filenames.append(os.path.join(root, file))

# build the document-term matrix using sklearn feature extraction 
vectorizer = CountVectorizer(input='filename', stop_words=stopwords)
dtm = vectorizer.fit_transform(filenames)
# extracts vocabulary from the vector
vocab = vectorizer.get_feature_names()

# turns document-term matrix and vocab into numpy array
dtm = dtm.toarray()
vocab = np.array(vocab)

# builds an LDA model and fits it to the document-term matrix
print "\n######## building the LDA model ########\n"
model = lda.LDA(n_topics=10, n_iter=100, random_state=1)
model.fit(dtm)

# prints the 20 words most probable for each topic of the model 
print "\n######## top 20 words for each topic ########\n"
topic_word = model.topic_word_
n = 20
for i, topic_dist in enumerate(topic_word):
    topic_words = np.array(vocab)[np.argsort(topic_dist)][:-(n+1):-1]
    toprint = u'- Topic {}\n{}'.format(i, ' '.join(topic_words))
    csv_row = u'"topic {}";"{}"\n'.format(i, '";"'.join(topic_words))
    csv_topicwords.write(csv_row)
    print toprint

# prints the top topic for each document of the corpus
print "\n######## top topic for each document ########\n"
doc_topic = model.doc_topic_
for i in range(len(filenames)):
	csv_row = '"{}";"{}";"{}"\n'.format(filenames[i],
			doc_topic[i].argmax(),
			round(doc_topic[i][doc_topic[i].argmax()], 3))
	print("{} (top topic: {}, value: {})"
		.format(filenames[i],
			doc_topic[i].argmax(),
			round(doc_topic[i][doc_topic[i].argmax()], 3)))
	csv_doctopic.write(csv_row)

# # print the topic probability of n documents
# doc_topic = model.doc_topic_
# for n in range(10):
#     topic_most_pr = doc_topic[n].argmax()
#     print("doc: {} topic: {}".format(n, topic_most_pr))

###################
# Useful comments #
###################

# CountVectorizer : http://scikit-learn.org/stable/modules/generated/sklearn.feature_extraction.text.CountVectorizer.html
# the method has multiple parameters that can be exploited, here's a unexhaustive list of cool stuff
# - takes filename, file object, or content (string) as input
# - tokenizer can be overridden
# - can build ngrams instead of words (as terms in the document-term-matrix)
# - max_df and min_df params can be used to exclude words with document frequency higher or lower than thresholds

# lda.LDA() parameters :
# n_topics = number of topics
# n_iter = number of iteration the model should run (no control for convergence of EM algo here so leave it between 500 and 1000 depending on the time you have)
# random_state = I have no idea what that is honestly
# + optional parameters
# alpha = Dirichlet parameter for distribution over topics
# eta = Dirichlet parameter for distribution over words
# These two should be between 0 and 1, default is 0.1. They're the "priors" and control distribution of probability
# A bit of litterature concerning that : http://papers.nips.cc/paper/3854-rethinking-lda-why-priors-matter

