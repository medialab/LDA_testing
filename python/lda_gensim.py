# !/usr/bin/env python
# -*- coding: utf8 -*-

import os
import re
import sys
import time
import pickle
import string
import gensim
from gensim import models
from gensim import corpora
from gensim import similarities
from pprint import pprint
from six import iteritems
from collections import defaultdict
from nltk.corpus import stopwords
from langdetect import detect
from langdetect import DetectorFactory
DetectorFactory.seed = 0 

start_time = time.time()
corpus_files = sys.argv[1]

# stopwords list is build for a multilingual french/english/german/spanish corpus
stops = []
stops.extend(stopwords.words('english'))
stops.extend(stopwords.words('french'))
stops.extend(stopwords.words('german'))
stops.extend(stopwords.words('spanish'))
stops.extend([u'', u' ', u'%', u'$', u'€', u'£', u'@', u'<', u'>', u'—', u'·', u'&', u'←', u'→', u'§', u'……', u'–', u'[…]', u'[]', u'\n', u' ', u'•', u'les', u'▪'])
stops.extend([u'a', u'ai', u'aie', u'aient', u'aies', u'ait', u'alors', u'as', u'au', u'aucun', u'aucuns', u'aura', u'aurai', u'auraient', u'aurais', u'aurait', u'auras', u'aurez', u'auriez', u'aurions', u'aurons', u'auront', u'aussi', u'autre', u'aux', u'avaient', u'avais', u'avait', u'avant', u'avec', u'avez', u'aviez', u'avions', u'avoir', u'avons', u'ayant', u'ayante', u'ayantes', u'ayants', u'ayez', u'ayons', u'bon', u'c', u"c'", u'car', u'ce', u'ceci', u'cela', u'celà', u'ces', u'cet', u'cette', u'ceux', u'chaque', u'ci', u'comme', u'comment', u'd', u"d'", u'dans', u'de', u'dedans', u'dehors', u'depuis', u'des', u'deux', u'devoir', u'devrait', u'devrez', u'devriez', u'devrions', u'devrons', u'devront', u'dois', u'doit', u'donc', u'dos', u'du', u'dès', u'dù', u'elle', u'elles', u'en', u'encore', u'es', u'est', u'et', u'eu', u'eue', u'eues', u'eurent', u'eus', u'eusse', u'eussent', u'eusses', u'eussiez', u'eussions', u'eut', u'eux', u'eûmes', u'eût', u'eûtes', u'faire', u'fais', u'faisez', u'fait', u'faites', u'fois', u'font', u'furent', u'fus', u'fusse', u'fussent', u'fusses', u'fussiez', u'fussions', u'fut', u'fûmes', u'fût', u'fûtes', u'ici', u'il', u'ils', u'j', u"j'", u'je', u'juste', u'l', u"l'", u'la', u'le', u'les', u'leur', u'leurs', u'lui', u'là', u'm', u"m'", u'ma', u'maintenant', u'mais', u'me', u'mes', u'moi', u'moins', u'mon', u'mot', u'même', u'n', u"n'", u'ne', u'ni', u'nom', u'nommé', u'nommée', u'nommés', u'nos', u'notre', u'nous', u'on', u'ont', u'ou', u'où', u'par', u'parce', u'pas', u'peu', u'peut', u'plupart', u'pour', u'pourquoi', u'qu', u'quand', u'que', u'quel', u'quelle', u'quelles', u'quels', u'qui', u's', u"s'", u'sa', u'sans', u'se', u'sera', u'serai', u'seraient', u'serais', u'serait', u'seras', u'serez', u'seriez', u'serions', u'serons', u'seront', u'ses', u'seulement', u'si', u'sien', u'soi', u'soient', u'sois', u'soit', u'sommes', u'son', u'sont', u'sous', u'soyez', u'soyons', u'suis', u'sujet', u'sur', u't', u"t'", u'ta', u'tandis', u'te', u'tellement', u'tels', u'tes', u'toi', u'ton', u'tous', u'tout', u'trop', u'très', u'tu', u'un', u'une', u'voient', u'vois', u'voit', u'vont', u'vos', u'votre', u'vous', u'vu', u'y', u'à', u'ça', u'étaient', u'étais', u'était', u'étant', u'étante', u'étantes', u'étants', u'état', u'étiez', u'étions', u'été', u'étée', u'étées', u'étés', u'êtes', u'être'])
stops.extend([u'january', u'february', u'march', u'april', u'may', u'june', u'july', u'august', u'september', u'october', u'november', u'december'])
stops.extend([u'janvier', u'février', u'mars', u'avril', u'mai', u'juin', u'juillet', u'août', u'septembre', u'octobre', u'novembre', u'décembre'])
stops.extend([u'lundi', u'mardi', u'mercredi', u'jeudi', u'vendredi', u'samedi', u'dimanche'])
stops.extend([u'a', u'b', u'c', u'd', u'e', u'f', u'g', u'h', u'i', u'j', u'k', u'l', u'm', u'n', u'o', u'p', u'q', u'r', u's', u't', u'u', u'v', u'w', u'x', u'y', u'z'])
stops = list(set(stops))

punctuation = re.compile(r'[-+=#/_.?!,":;(){}[]|0-9]')

# iterator over files in the input folder yields a tuple
# a cleaned up list of tokens (strings) associated with the name of its file
# language detection drops files which text is not (mostly) in english, german or french
def corpusIterator():
	for root, dirs, files in os.walk(corpus_files):
		for file in files:
			text = open(os.path.join(root, file), 'r').read().lower().strip()
			text = re.sub(r'\s+', ' ', text) # consecutive spaces
			text = re.sub(r'[\n\t\r]', ' ', text) # line breaks
			text = text.replace('“','').replace('”','') # strange quote chars...
			text = text.replace('«','').replace('»','') # that are non-unicode
			text = punctuation.sub("", text)
			try:
				lang = detect(text.decode('utf-8'))
			except:
				lang = 'en'
			if lang == 'de' or lang == 'en' or lang == 'fr':
			file_name = os.path.join(root, file)
			text_array = text.split()
			yield (file_name, text_array)

# builds the dictionary of all terms used in all documents
# drops stopwords, single letters and words used only once
def buildDictionary():
	dictionary = corpora.Dictionary(document[1] for document in corpusIterator())
	stop_ids = [dictionary.token2id[stopword] for stopword in stops if stopword in dictionary.token2id]
	# letter_ids = [dictionary.token2id[letter] for letter in string.ascii_lowercase if letter in dictionary.token2id]
	once_ids = [tokenid for tokenid, docfreq in iteritems(dictionary.dfs) if docfreq == 1]
	dictionary.filter_tokens(stop_ids + once_ids )#+ letter_ids)
	# dictionary.filter_extremes(no_below=3, keep_n=1000000)
	dictionary.compactify()
	return dictionary

# this class allows not to load all of the corpus in ram
# it uses the corpus iterator and the dictionary to yield one vector (one document) at a time
class corpusLove(object):
	def __iter__(self):
		current_id = 0
		for document in corpusIterator():
			doc_ids[current_id] = document[0]
			yield dictionary.doc2bow(document[1])
			current_id += 1
		pickle.dump(doc_ids, open("results/doc_ids.p", 'wb'))

# exports the list of topics with 50 associated words from the model to a csv file
def exportTopics(model, filename):
	topicword = open('results/topicXwords_' + filename + '.csv', 'w')
	for elem in model.print_topics(num_topics=-1, num_words=50):
		topic = elem[0]
		words = elem[1].split(' + ')
		line = '"' + str(topic) + '";"'
		for word in words:
			line += word.split('*')[1] + '";"'
		line = line[:-2] + '\n'
		topicword.write(line.encode('utf-8'))

# exports the list of documents with their associated topics from the model to a csv file
def exportDocuments(model, filename):
	doctopic = open('results/docXtopic_' + filename + '.csv', 'w')
	for doc in doc_ids:
		line = '"' + doc_ids[doc] + '","' + doc_ids[doc].split('/')[2][:-4] + '","'
		topics = ""
		for topic in model[corpus[doc]]:
			topics += str(topic[0]) + '","' + str(topic[1]) + '","'
		line += topics[:-2] + '\n'
		doctopic.write(line)

# if a full model (dictionary + corpus + lda model) exists on disk it'll be loaded instead of re-run
if (os.path.exists("results/dictionary.dict") and os.path.exists("results/corpus.lda-c") and os.path.exists("results/model.lda")):
	dictionary = corpora.Dictionary.load('results/dictionary.dict')
	corpus = corpora.BleiCorpus('results/corpus.lda-c')
	model = models.LdaModel.load('results/model.lda')
	doc_ids = pickle.load(open('results/doc_ids.p', 'rb'))
	print("Loaded dictionary, corpus and model from files saved on disk")
else:
	print "building the dictionary"
	dictionary = buildDictionary()
	dictionary.save('results/dictionary.dict')
	dict_time = time.time()
	print "%s seconds" % round(dict_time - start_time, 2)
	print "%s minutes" % round((dict_time - start_time)/60, 2)

	print "creating the corpus"
	doc_ids = {}
	corpus = corpusLove()
	corpora.BleiCorpus.serialize('results/corpus.lda-c', corpus)
	corpus = corpora.BleiCorpus('results/corpus.lda-c')
	corpus_time = time.time()
	print "%s seconds" % round(corpus_time - dict_time, 2)
	print "%s minutes" % round((corpus_time - dict_time)/60, 2)

	print "tuning the model"
	# this line contains the LDA parameters as explicit parameters of the tuning function
	model = models.LdaModel(corpus, id2word=dictionary, num_topics=60, iterations=500, eval_every=10, alpha='auto')
	model.save('results/model.lda')
	model_time = time.time()
	print "%s seconds" % round(model_time - corpus_time, 2)
	print "%s minutes" % round((model_time - corpus_time)/60, 2)

exportTopics(model, "model_last")
exportDocuments(model, "model_last")

print "doing all of this"
print "%s seconds" % round((time.time() - start_time), 2)
print "%s minutes" % round((time.time() - start_time)/60, 2)







