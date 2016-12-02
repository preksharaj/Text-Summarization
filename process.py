import re
import os
import sys
import networkx as nx
import nltk.data
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer
stemmer = SnowballStemmer('english')
stop = set(stopwords.words('english'))
lang='english'
punctuations=['!','"','#','$','%','&','\'',',','(',')','*','+',',','-','.','/',':',';','<','=','>','?','@','[','\\',']','^','_','`','{','|','}','~']
num = re.compile(r'[0-9]+')

def reading(filename,lang='english'):
    f = open(filename, 'r', encoding="latin1")
    wordList = []
    listofsent = []
    finalList = []
    count=0
    for line in f:
        count+=1
        #print("line"+line)
        line = line.strip()
        line = line.lower()

        # line = line.split()
        listofsent=clean(line,listofsent)
    return listofsent,count


def clean(line,listofsent):
    try:
        tokenizer = nltk.data.load('tokenizers/punkt/' + lang + '.pickle')
        # print(tokenizer)
    except:
        print("try something else")
    tempList = tokenizer.tokenize(line)
    for i in tempList:
        if i not in punctuations:
            listofsent.append(i)
    return listofsent




#reading("1.txt")





