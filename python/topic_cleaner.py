# !/usr/bin/env python
# -*- coding: utf8 -*-

### This script allows for agregation and renaming of topics output by an LDA model ###

import sys
import csv
from itertools import izip
from collections import defaultdict

# iterate through a list in pairs of items
def pairwise(iterable):
    a = iter(iterable)
    return izip(a, a)

# documents : input should be the document list output by lda_gensim.py
documents = csv.reader(open(sys.argv[1], 'r'))

# output will be two lists of documents similar to the output of lda_gensim.py
agregated = csv.writer(open('topics_agregated.csv', 'w'))
named = csv.writer(open('topics_named.csv', 'w'))

# agregation and renaming are based on the following dictionary
# keys = old topic number / value = (new topic name, new topic number)
# number of new topic names and new topic numbers should be consistent
max_topics = {
	'1' : ('wouf', '1'),
	'2' : ('miaou', '2'),
	'4' : ('miaou', '2'),
	'5' : ('wouf', '1'),
	'6' : ('wouf', '1'),
	'7' : ('miaou', '2'),
	'8' : ('baw', '3'),
	'9' : ('miaou', '2'),
	'10' : ('miaou', '2'),
	'11' : ('miaou', '2'),
	'12' : ('wouf', '1'),
	'13' : ('baw', '3'),
	'15' : ('wouf', '1'),
	'16' : ('wouf', '1'),
	'17' : ('miaou', '2'),
	'19' : ('baw', '3'),
	'20' : ('baw', '3'),
	'21' : ('atchi', '4'),
	'22' : ('atchi', '4'),
	'23' : ('wouf', '1'),
	'24' : ('wouf', '1'),
	'25' : ('atchi', '4'),
	'26' : ('wouf', '1'),
	'27' : ('atchi', '4'),
	'28' : ('atchi', '4'),
	'29' : ('atchi', '4'),
	'30' : ('baw', '3'),
	'31' : ('baw', '3'),
	'32' : ('baw', '3')
}

for document in documents:
	path = document[0]
	webid = document[1]
	topics = filter(None, document[2:])
	
	# creates a dictionary of agregated topics // NB : scores are accumulated
	topics_agregated_dict = defaultdict(float)
	for topic, score in pairwise(topics):
		if topic in max_topics.keys():
			topics_agregated_dict[max_topics[topic][1]] += float(score)

	# turns the dictionary into 2 different lists
	# 1 : topics agregated with scores accumulated
	# 2 : topics renamed and filtered (topics with score beneath 0.15 are discarded)
	topics_agregated_array = []
	topics_named_array = []
	for topic in topics_agregated_dict.keys():
		topics_agregated_array.append((topic, topics_agregated_dict[topic]))
		if topics_agregated_dict[topic] > 0.15:
			topics_named_array.append((max_topics[topic][0], topics_agregated_dict[topic]))

	# keeps only the top 3 topics with higher scores in the list n°2 (named topics)
	if len(topics_named_array) > 0:
		topics_named_array = sorted(topics_named_array, key=lambda x: x[1], reverse=True)
		topics_named_array = topics_named_array[:3]

	# builds csv output lines
	line_agregated = [path, webid]
	line_named = [path, webid]
	line_agregated.extend([i for topic_tuple in topics_agregated_array for i in topic_tuple])
	line_named.extend([i for topic_tuple in topics_named_array for i in topic_tuple])

	# writes csv output lines to files
	agregated.writerow(line_agregated)
	named.writerow(line_named)


