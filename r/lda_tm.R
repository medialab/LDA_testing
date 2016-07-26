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

# Apply various treatments on corpus
corpus <- tm_map(corpus, removePunctuation)
corpus <- tm_map(corpus, removeNumbers)
corpus <- tm_map(corpus, tolower)
corpus <- tm_map(corpus, removeWords, stopwords("english"))
corpus <- tm_map(corpus, removeWords, stopwords("french"))
corpus <- tm_map(corpus, removeWords, stopwords("german"))
corpus <- tm_map(corpus, stripWhitespace)
# paperCorp <- tm_map(paperCorp, stemDocument)

# Retransforms the modified content of the Corpus into a simple vector of texts
files <- c(corpus$content)

# Lexicalize the files (lda prerequisite)
lexical <- lexicalize(files)

# Lists documents and vocabulary from the lexicalized corpus
documents <- lexical$documents
vocab <- lexical$vocab

# Builds the LDA model from the documents and vocab (10 topics and 100 runs)
modelda <- lda.collapsed.gibbs.sampler(documents, 10, vocab, 100, 0.1, 0.1)

# Prints out the top 10 words for each 10 topics
print(top.topic.words(modelda$topics))

