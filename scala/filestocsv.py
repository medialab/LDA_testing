# !/usr/bin/env python
# -*- coding: utf8 -*-

import sys
import os
import csv
import re

# Opens folder where corpus files are located and creates a csv writer for the output
folder = '../corpus_files/'
outputfile = csv.writer(open('files.csv', 'w'), delimiter=',', quotechar='"')

# Walks the folder of corpus files and puts the non-empty files into an indexed csv
count = 0
for root, dirs, files in os.walk(folder):
	for file in files:
		file = open(os.path.join(root, file), 'r').read()
		# Remove line breaks, double quotes and consecutive white spaces
		file = re.sub(' +', ' ', file.replace('\n', ' ').replace('"', ''))
		if file != '':
			count += 1
			line = [str(count), file]
			outputfile.writerow(line)
