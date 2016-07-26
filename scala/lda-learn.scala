// Stanford TMT Example 2 - Learning an LDA model
// http://nlp.stanford.edu/software/tmt/0.4/

// Tells Scala where to find the TMT classes
import scalanlp.io._;
import scalanlp.stage._;
import scalanlp.stage.text._;
import scalanlp.text.tokenize._;
import scalanlp.pipes.Pipes.global._;

import edu.stanford.nlp.tmt.stage._;
import edu.stanford.nlp.tmt.model.lda._;
import edu.stanford.nlp.tmt.model.llda._;

// Loads the csv files and tells script where to find ids
val source = CSVFile("files.csv") ~> IDColumn(1);

// Construct a tokenizer
val tokenizer = {
  SimpleEnglishTokenizer() ~>            // tokenize on space and punctuation
  CaseFolder() ~>                        // lowercase everything
  WordsAndNumbersOnlyFilter() ~>         // ignore non-words and non-numbers
  MinimumLengthFilter(3)                 // take terms with >=3 characters
}

// Reads from loaded csv, tokenizes and filters terms based on textual statistics 
val text = {
  source ~>                              // read from the source file
  Column(2) ~>                           // select column containing text
  TokenizeWith(tokenizer) ~>             // tokenize with tokenizer above
  TermCounter() ~>                       // collect counts (needed below)
  TermMinimumDocumentCountFilter(4) ~>   // filter terms in <4 docs
  TermDynamicStopListFilter(30) ~>       // filter out 30 most common terms
  DocumentMinimumLengthFilter(5)         // take only docs with >=5 terms
}

// Turns the text into a dataset ready to be used with LDA
val dataset = LDADataset(text);

// Defines the model parameters
val params = LDAModelParams(numTopics = 10, dataset = dataset,
  topicSmoothing = 0.01, termSmoothing = 0.01);

// Names of the output model folder to generate
val modelPath = file("lda-"+dataset.signature+"-"+params.signature);

// Trains the model: the model (and intermediate models) are written to the
// output folder.  If a partially trained model with the same dataset and
// parameters exists in that folder, training will be resumed.
TrainGibbsLDA(params, dataset, output=modelPath, maxIterations=1500);
