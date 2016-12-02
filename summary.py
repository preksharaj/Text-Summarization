from __future__ import absolute_import
from __future__ import division, print_function, unicode_literals

from sumy.nlp.tokenizers import Tokenizer
from LSA import LsaSummarizer as Summarizer
from sumy.parsers.plaintext import PlaintextParser
from sumy.summarizers.lex_rank import LexRankSummarizer
from sumy.summarizers.text_rank import TextRankSummarizer
import textrank
#import textsum




from sumy.nlp.stemmers import Stemmer
from sumy.utils import get_stop_words
import os
import sys

LANGUAGE = "english"
SENTENCES_COUNT = 5


def lexrankReferenceSummary(path):
    sentencesList = []
    parser = PlaintextParser.from_file(path, Tokenizer(LANGUAGE))
    stemmer = Stemmer(LANGUAGE)
    summarizer = LexRankSummarizer(stemmer)
    summarizer.stop_words = get_stop_words(LANGUAGE)

    for sentence in summarizer(parser.document, SENTENCES_COUNT):
        #print("LEX"+sentence._text)
    #print("*************")
        sentencesList.append(sentence._text)

    return sentencesList


def textrankReferenceSummary(path):
    sentencesList = []
    parser = PlaintextParser.from_file(path, Tokenizer(LANGUAGE))
    stemmer = Stemmer(LANGUAGE)
    summarizer = TextRankSummarizer(stemmer)
    summarizer.stop_words = get_stop_words(LANGUAGE)

    for sentence in summarizer(parser.document, SENTENCES_COUNT):
        #print("TEXT"+sentence._text)
    #print("*************")
        sentencesList.append(sentence._text)
    newsent= ' '.join(sentencesList)

    return newsent


def lsarankReferenceSummary(path):
    sentencesList = []
    parser = PlaintextParser.from_file(path, Tokenizer(LANGUAGE))
    stemmer = Stemmer(LANGUAGE)
    summarizer = Summarizer(stemmer)
    summarizer.stop_words = get_stop_words(LANGUAGE)

    for sentence in summarizer(parser.document, SENTENCES_COUNT):
        #print("LSA"+sentence._text)
    #print("LSA ends here")
        sentencesList.append(sentence._text)

    return sentencesList


if __name__ == "__main__":
    writer = open('output2.txt', 'w+')

    for root, dirs, files in os.walk(sys.argv[1]):
        for i in range(0, len(files)):
            filename = root + '/' + files[i]
            parser = PlaintextParser.from_file(filename, Tokenizer(LANGUAGE))
            stemmer = Stemmer(LANGUAGE)

            suma4 = " "

            suma1=lexrankReferenceSummary(filename)
            suma2 = textrankReferenceSummary(filename)
            suma3= lsarankReferenceSummary(filename)
            suma4=textrank.summary_main(filename)

            #keywords_ex = textsum.getKeywords(filename)

            #print(keywords_ex)

            writer.write("Filename= "+filename+"\n")
            writer.write('Reference Summary'+ "\n")
            writer.write(suma2 + "\n")
            writer.write("Our Summary"+"\n")
            writer.write(suma4 + "\n")
            #writer.write("Keywords"+"\n")
            #writer.write(keywords_ex + "\n")
            writer.write("\n")

    writer.close()
