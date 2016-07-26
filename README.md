# LDA_testing

##python

Tests lda package implementation. Dependencies include numpy to take care of sparse matrices and sklearn to build the initial document-term matrix from raw text (handles stopwords exclusion)

####dependencies

- lda
- nltk + installation of the stopwords corpus 
- numpy
- scikit learn

##R

Tests LDA package. Dependencies include the tm package to take care of stopwords, numbers and punctuation removing. Watch out for working directory, you have to setwd to the r/ folder to execute the script.

####dependencies

- lda
- tm

##scala

This script is to be used with TMT, a tool designed by Stanford NLP group that can be found there : http://nlp.stanford.edu/software/tmt/tmt-0.4/

Watch out, it runs only with java jdk 1.7 and doesn't tell you so...

##corpus files

Small subset of texts. Any text files should work.