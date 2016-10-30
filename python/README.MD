### LDA_numpy_sklearn

Abandonned because it couldn't handle a corpus load above 90 thousands documents (100 million words). Basically the whole corpus had to be stored in RAM, and consequently => problems.

### LDA_gensim

Gensim package allows not to load everything in RAM. And also other cool things, like clever trimming of the dictionary, efficient filtering of words (stopwords) or reloading model from pickled files.

### topic_cleaner

This script can merge, suppress and rename topics and produce 2 _clean_ output files from the list of document and their associated topics output by LDA_gensim.

It needs a python dictionary as an input (yes it's hardcoded in the script, don't judge I'm on a deadline here).

dictionary = {
    old topic number : (new topic name, new topic number)
}

Ensure that the number of new topic names is consistent with the number of new topic numbers and that they match when you manually build your dictionary.