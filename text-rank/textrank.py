import os
import re
from collections import Counter
import math
import process
import operator


WORD = re.compile(r'\w+')

class Node:

    def __init__(self,sentence):
        self.sentence = sentence
        self.score = 0


class Graph:

    def __init__(self):
        self.graph = {}
        self.nodes = {}

    def add_node(self,sentence):
        if sentence in self.nodes:
            node = self.nodes[sentence]
        else:
            node = Node(sentence)
            self.nodes[sentence] = node

        return node

    def set_graph(self,words):

        graph = self.graph
        c =0
        c1 =0

        for i in words:
            c = c+1
            c_node = self.add_node(i)
            for j in words:
                c1=c1+1
                n_node = self.add_node(str(j))
                if c_node == n_node:
                    continue
                if c_node not in graph:
                    graph[c_node] = {}

                    sen1 = str(i)
                    sen2 = str(j)
                    #print("first "+sen1)
                    #print("second "+sen2)
                    graph[c_node][n_node] = self.get_similarity(sen1,sen2)

                else:
                    sen1 = str(i)
                    sen2 = str(j)
                    #print("im here")
                    graph[c_node][n_node] = self.get_similarity(sen1,sen2)
                #print(graph[c_node][n_node])



    def text_to_vector(self,sent1):

        w = WORD.findall(sent1)
        return Counter(w)

    def get_similarity(self,s1,s2):

        #print("s1"+s1)
        #print("s2"+s2)
        vec1 = self.text_to_vector(s1)
        vec2 = self.text_to_vector(s2)
        intersection = set(vec1.keys()) & set(vec2.keys())
        numerator = sum([vec1[x] * vec2[x] for x in intersection])

        sum1 = sum([vec1[x] ** 2 for x in vec1.keys()])
        #print("one"+str(sum1))
        sum2 = sum([vec2[x] ** 2 for x in vec2.keys()])
        #print("two"+str(sum2))
        denominator = math.sqrt(sum1) * math.sqrt(sum2)
        #print(denominator)


        return float(numerator) / denominator



    def pageRank(self,max_iter=10000):

        for i in range(0,max_iter):

            current_PR = {}

            for k in self.graph:
                if k in current_PR:
                    current_PR[k] = k.score
                else:
                    current_PR[k] = {}
                    current_PR[k] = k.score

            for j in self.graph:
                in_edges = []
                #print("j"+str(j.sentence))
                for k in self.graph:
                    for key in self.graph[k]:
                        if key.sentence != j.sentence:
                            in_edges.append(key)

                in_edges = set(in_edges)
                innerScore = 0
                for q in in_edges:
                    weightTot = 0
                    for r in self.graph[q]:

                        weightTot += self.graph[q][r]
                        #print("weight"+str(weightTot))
                    #print("first"+str(self.graph[q][j]))
                    #print("sec"+str(q.score))
                    try:
                        innerScore += (self.graph[q][j] * q.score) / weightTot
                        j.score = 0.15 + (0.85 * (innerScore))

                    except:
                        j.score= 0.15
                    delta = 0
                    for key in self.graph:
                        delta += abs(current_PR[key] - key.score)
                    if delta <= 0:
                        return
                #print("score" + str(j.score))


    def sort_nodes(self, num_lines):

        global sorted_PR, sorted_tag

        sorted_PR = sorted(self.graph.keys(), key=operator.attrgetter('score'), reverse=True)[:num_lines]
        #print(sorted_PR)
        sorted_tag = []
        for i in range(0,len(sorted_PR)):
            #print(str(sorted_PR[i].sentence)+''+str(sorted_PR[i].score))
            sorted_tag.append(sorted_PR[i].sentence)

        for i in sorted_tag:
            newsent=' '.join(sorted_tag)

        #print(newsent)
        return newsent

def summary_main(filename):
    global data, finalD, count

    finalD, count = process.reading(filename)
    #print(finalD)
    g=Graph()
    g.set_graph(finalD)
    g.pageRank()
    g.sort_nodes(5)

    sumsent = g.sort_nodes(5)
    return sumsent






