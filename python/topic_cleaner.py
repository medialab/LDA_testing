# !/usr/bin/env python
# -*- coding: utf8 -*-

import sys
import csv
from itertools import izip
from collections import defaultdict

def pairwise(iterable):
    a = iter(iterable)
    return izip(a, a)

documents = csv.reader(open(sys.argv[1], 'r'))
agregated = csv.writer(open('topics_agregated.csv', 'w'))
named = csv.writer(open('topics_named.csv', 'w'))

max_topics = {
	'1' : ('wouf', '1'),
	'2' : ('miaou', '2'),
	'3' : ('miaou', '2'),
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
	'14' : ('wouf', '1'),
	'15' : ('wouf', '1'),
	'16' : ('wouf', '1'),
	'17' : ('miaou', '2'),
	'18' : ('baw', '3'),
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
	
	topics_agregated_dict = defaultdict(float)
	for topic, score in pairwise(topics):
		if topic in max_topics.keys():
			topics_agregated_dict[max_topics[topic][1]] += float(score)

	topics_agregated_array = []
	topics_named_array = []
	for topic in topics_agregated_dict.keys():
		topics_agregated_array.append((topic, topics_agregated_dict[topic]))
		if topics_agregated_dict[topic] > 0.15:
			topics_named_array.append((max_topics[topic][0], topics_agregated_dict[topic]))


	if len(topics_named_array) > 0:
		topics_named_array = sorted(topics_named_array, key=lambda x: x[1], reverse=True)
		topics_named_array = topics_named_array[:3]

	line_agregated = [path, webid]
	line_named = [path, webid]
	line_agregated.extend([i for topic_tuple in topics_agregated_array for i in topic_tuple])
	line_named.extend([i for topic_tuple in topics_named_array for i in topic_tuple])

	agregated.writerow(line_agregated)
	named.writerow(line_named)


