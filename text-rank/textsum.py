import editdistance
import networkx as nx
import itertools
import nltk

text = 'My name is Akshay Chopra. I am a graduate student at USC. My major is Computer Science. I am currently in my 2nd year. I will be graduating in May 2017.'
punctuations = ['!', '"', '#', '$', '%', '&', '\'', ',', '(', ')', '*', '+', ',', '-', '.', '/', ':', ';', '<', '=',
                '>', '?', '@', '[', '\\', ']', '^', '_', '`', '{', '|', '}', '~']
stop_words =['i','me','my','myself','we','our','ours','ourselves','you','your','yours','yourself','yourselves','he','him','his','himself','she','her','hers','herself','it','its','itself','they','them','their','theirs','themselves','what','which','who','whom','this','that','these','those','am','is','are','was','were','be','been','being','have','has','had','having','do','does','did','doing','a','an','the','and','but','if','or','because','as','until','while','of','at','by','for','with','about','against','between','into','through','during','before','after','above','below','to','from','up','down','in','out','on','off','over','under','again','further','then','once','here','there','when','where','why','how','all','any','both','each','few','more','most','other','some','such','no','nor','not','only','own','same','so','than','too','very','s','t','can','will','just','don','should','now',]



tempwordlist = []
finalWords =  []





def processDoc(filename):
    f = open(filename, 'r')
    file1 = f.read()
    file1 = file1.lower()
    words = nltk.tokenize.word_tokenize(file1)
    #print(words)
    for i in words:
        if i not in punctuations:
            if i not in stop_words:

                tempwordlist.append(i)

    posTags = nltk.pos_tag(tempwordlist)
    #print(posTags)

    for i in posTags:
        if i[1] in ['NN','ADJ']:
            finalWords.append(i[0])

    #print(finalWords)
    return finalWords

def getWordList():
    f = open('1.txt', 'r')
    file1 = f.read()
    file1 = file1.lower()
    words = nltk.tokenize.word_tokenize(file1)
    # print(words)
    for i in words:
        if i not in punctuations:
            tempwordlist.append(i)

    return tempwordlist

#print(num)
def getDistance(node1,node2):
    num = editdistance.eval(node1, node2)
    return num

def getKeywordGraph(node1):
    pairs = list(itertools.combinations(node1,2))
    #print(node1)
    G = nx.Graph()
    for i in node1:
        G.add_node(i)

    for j in pairs:
        a = j[0]
        b = j[1]
        dist = getDistance(a,b)
        #print(a,b,dist)
        G.add_edge(a,b, weight = dist)

        #print(G.get_edge_data(a,b))
    #print(G['My']['Akshay']['weight'])
    return G

def getKeywords(filename):

    words = processDoc(filename)
    filtered = []

    #g1 = nx.Graph()
    g1 = getKeywordGraph(words)
    page_rank_s = nx.pagerank(g1)
    page_rank_s = sorted(page_rank_s, reverse=True)
    #print(page_rank_s)

    for i in range(0,10):
        filtered.append(page_rank_s[i])

    finalKey = set([])
    tempKey = set([])
    #total_words = getWordList()

    prs = ",".join(filtered)

    return prs

    #i =0
    #j =1

    #while j<len(total_words):
        #one = total_words[i]
        #two = total_words[j]

        #if one in page_rank_s and two in page_rank_s:
            #finalKey.add(one + ' ' + two)
            #tempKey.add(one)
            #tempKey.add(two)

        #else:
            #if one in page_rank_s and one not in tempKey:
                #finalKey.add(one)
                #tempKey.add(one)

            #elif j == len(total_words) - 1 and two in page_rank_s and two not in tempKey:
                #finalKey.add(two)

        #i = i + 1
        #j = j + 1

    #print(finalKey)



#getKeywords()

