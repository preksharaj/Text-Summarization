from __future__ import absolute_import
from __future__ import division, print_function, unicode_literals
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.nlp.stemmers import Stemmer
from sumy.utils import get_stop_words
import os
import sys
import numpy
import math
from numpy.linalg import svd as singular_value_decomposition
from sumy.summarizers._summarizer import AbstractSummarizer

LANGUAGE = "english"
SENTENCES_COUNT = 2
stop_words =['i','me','my','myself','we','our','ours','ourselves','you','your','yours','yourself','yourselves','he','him','his','himself','she','her','hers','herself','it','its','itself','they','them','their','theirs','themselves','what','which','who','whom','this','that','these','those','am','is','are','was','were','be','been','being','have','has','had','having','do','does','did','doing','a','an','the','and','but','if','or','because','as','until','while','of','at','by','for','with','about','against','between','into','through','during','before','after','above','below','to','from','up','down','in','out','on','off','over','under','again','further','then','once','here','there','when','where','why','how','all','any','both','each','few','more','most','other','some','such','no','nor','not','only','own','same','so','than','too','very','s','t','can','will','just','don','should','now',]



class LsaSummarizer(AbstractSummarizer):
    MIN_DIMENSIONS = 3
    REDUCTION_RATIO = 1/1

    def __call__(self, doc, sent_count):

        dictionary = self._create_dictionary(doc)
        matrix = self._create_matrix(doc, dictionary)
        matrix = self._compute_term_frequency(matrix)
        u, sigma, v = singular_value_decomposition(matrix, full_matrices=False)

        ranks = iter(self._compute_ranks(sigma, v))
        return self._get_best_sentences(doc.sentences, sent_count,
            lambda s: next(ranks))

    def _create_dictionary(self, doc):
        words = map(self.normalize_word, doc.words)
        for w in words:
            if w not in stop_words:
                unique_words = set(self.stem_word(w))
        return dict((w, i) for i, w in enumerate(unique_words))

    def _create_matrix(self, doc, dictionary):
        sentences = doc.sentences
        words_count = len(dictionary)
        sent_count = len(sentences)
        matrix = numpy.zeros((words_count, sent_count))
        for col in range(sent_count):
            sentence=sentences[col]
            for word in map(self.stem_word, sentence.words):
                if word in dictionary:
                    row = dictionary[word]
                    matrix[row, col] += 1

        return matrix

    def _compute_term_frequency(self, matrix, smooth=0.4):
        max_frequencies = numpy.max(matrix, axis=0)
        rows, cols = matrix.shape
        for row in range(rows):
            for col in range(cols):
                word_f = max_frequencies[col]
                if word_f != 0:
                    frequency = matrix[row, col]/word_f
                    matrix[row, col] = smooth + (1.0 - smooth)*frequency

        return matrix

    def _compute_ranks(self, sigma, v_matrix):
        assert len(sigma) == v_matrix.shape[0], "Matrices should be multiplicable"

        dimensions = max(LsaSummarizer.MIN_DIMENSIONS,
            int(len(sigma)*LsaSummarizer.REDUCTION_RATIO))
        powered_sigma = tuple(s**2 if i < dimensions else 0.0
            for i, s in enumerate(sigma))

        ranks = []
        for column_vector in v_matrix.T:
            arr1=zip(powered_sigma, column_vector)
            rank = sum(s*v**2 for s, v in arr1)
            ranks.append(math.sqrt(rank))

        return ranks


