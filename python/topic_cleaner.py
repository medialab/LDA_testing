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

# output is a list of documents with a score by column for every new topic from the dictionary
output = csv.writer(open('topics_cleaned.csv', 'w'))

# agregation and renaming are based on the following dictionary
# keys = old topic number / value = new topic name
new_topics = {
	'1' : 'Terms of use',
	'2' : 'Personal records',
	'3' : 'Cloud  & server security',
	'4' : 'Card and ID fraud',
	'5' : 'Health',
	'6' : 'Airspace Security',
	'7' : 'Cloud  & server security',
	'10' : 'Social Media',
	'11' : 'Car and transport',
	'12' : 'Education',
	'13' : 'Research IT',
	'14' : 'Web and Computer security',
	'16' : 'Hacking',
	'17' : 'Business Tech and new media',
	'20' : 'Mobile OS and App',
	'21' : 'Freedom of citizens',
	'22' : 'Cyberdefense',
	'23' : 'Business Tech and new media',
	'24' : 'Surveillance FR',
	'25' : 'Data transmission',
	'26' : 'Cybersecurity',
	'27' : 'Data Regulation FR',
	'28' : 'Wearable & IOT',
	'29' : 'Cybersecurity',
	'30' : 'Crypto & Access',
	'33' : 'Telecom Operators FR',
	'34' : 'Cyberdefense',
	'35' : 'Data transmission',
	'36' : 'Data Regulation US',
	'37' : 'Communication traces',
	'39' : 'Web and Computer security',
	'41' : 'Surveillance FR',
	'42' : 'Copyright',
	'44' : 'Crypto & Access',
	'46' : 'Surveillance US',
	'47' : 'Surveillance US',
	'48' : 'Surveillance FR',
	'49' : 'Bitcoin',
	'50' : 'Mobile OS and App',
	'51' : 'Surveillance FR',
	'52' : 'Cookies and tracking',
	'53' : 'Data Regulation EU',
	'54' : 'Big data & Analyitcs',
	'56' : 'Surveillance US',
	'57' : 'Consumer data',
	'58' : 'Cloud  & server security'
}

topics_names = sorted(list(set(new_topics.values())))
headers = ["webentity_id", "page_id"] + topics_names
output.writerow(headers)

for document in documents:
	webentity_id = document[0].split('/')[1]
	page_id = document[1]
	topics = filter(None, document[2:])
	
	# creates a dictionary of agregated topics - NB : scores are accumulated
	topics_agregated = defaultdict(float)
	for topic, score in pairwise(topics):
		if topic in new_topics:
			topics_agregated[new_topics[topic]] += float(score)

	# turns the dictionary into a list of score percentages
	score_array = []
	for topic in topics_names:
		if topic in topics_agregated:
			score_array.append(round(topics_agregated[topic], 4) * 100)
		else:
			score_array.append(0.0)

	# builds csv output line and writes it to output file
	output_line = [webentity_id, page_id] + score_array
	output.writerow(output_line)


