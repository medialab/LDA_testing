library(tm)
library(lda)

# Just tells you what your working dir is
wd <- getwd()
cat("Current working dir: ", wd, "\n\n")

# Prints out the file names
cat("files\n")
filenames <- dir(path="../corpus_files", pattern=".*.txt", full.names=TRUE)
cat(filenames, sep="\n")
cat("\n")

# Reads from the files and removes the line breaks
files <- sapply(filenames, readLines)
files <- lapply(files, paste, collapse = " ")

# Builds a VCorpus with tm
corpus <- Corpus(VectorSource(files))

# Apply various treatments on corpus (explicit)
corpus <- tm_map(corpus, removePunctuation)
corpus <- tm_map(corpus, removeNumbers)
corpus <- tm_map(corpus, tolower)
corpus <- tm_map(corpus, removeWords, stopwords("english"))
corpus <- tm_map(corpus, removeWords, stopwords("french"))
corpus <- tm_map(corpus, removeWords, stopwords("german"))
corpus <- tm_map(corpus, stripWhitespace)
# paperCorp <- tm_map(paperCorp, stemDocument) # optional stemming

# Retransforms the modified content of the Corpus into a simple vector of texts
files <- c(corpus$content)

# Lexicalize the files (lda prerequisite)
lexical <- lexicalize(files)

# Lists documents and vocabulary from the lexicalized corpus
documents <- lexical$documents
vocab <- lexical$vocab

# Builds the LDA model from the documents and vocab (10 topics and 100 runs)
modelda <- lda.collapsed.gibbs.sampler(documents, 10, vocab, 500, 0.1, 0.1)

# Prints out the top 10 words for each 10 topics
print(top.topic.words(modelda$topics))

###################
# Useful comments #
###################

# The lda.collapsed.gibbs.sampler has the following arguments in this script
# documents : A list whose length is equal to the number of documents, each element of documents is an integer matrix with two rows.  Each column of documents[[i]] (i.e., document i ) represents a word occurring in the document.
# 10 (2nd positional arg) : the desired number of topics in the model
# vocab : A character vector specifying the vocabulary words associated with the word indices used in documents.
# 500 (4th positional arg) : number of run the model should run (no control for convergence implemented so this params depends on the time you have to run the script, leave it between 500 and 1000)
# 0.1 (5th positional arg) : alpha, Dirichlet parameter for distribution over topics
# 0.1 (6th positional arg) : eta, Dirichlet parameter for distribution over words
# These last two should be between 0 and 1, default is 0.1. They're the "priors" and control distribution of probability
# A bit of litterature concerning that : http://papers.nips.cc/paper/3854-rethinking-lda-why-priors-matter
