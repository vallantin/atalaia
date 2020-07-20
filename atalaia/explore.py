# TODOS
#--------------------------------------
# imports
import matplotlib.pyplot as plt
from atalaia.atalaia import Atalaia
import numpy as np
import networkx as nx


class Explore:
    """Explore is used for text exploratory tasks. 
    """
    
    def __init__(self, language:str):
        """
        Parameters
        ----------
        language : str
            The language of the corpus 
        """ 
        self.language = language
        self.atalaia  = self.__start_atalaia()

    def __start_atalaia(self):
        """ Starts an instance of Atalaia"""
        return Atalaia(self.language)

    def describe(self, corpus:list):
        """ Gets the lengths of the sentences present in the corpus, based on the number of tokens. 
        Returns the lengths, the shortest value and the longest value and the average sentence size."""

        # tokenize sentences
        tokenized_sentences = [self.atalaia.tokenize(sentence) for sentence in corpus]
        
        # get the lengths
        lengths = [len(sentence) for sentence in tokenized_sentences]

        # get the percentiles
        a = np.array(lengths)
        percentiles = (np.percentile(a,0), np.percentile(a,25), np.percentile(a,50), np.percentile(a,75), np.percentile(a,100))

        # get shortest, longest and average sentence size using the percentiles values
        shortest = percentiles[0] # 0%
        longest  = percentiles[4] # 100%
        average  = percentiles[2] # 50%

        return lengths, shortest, longest, average, percentiles

    def plot_sentences_size_histogram(self, corpus:list, bins = 30, xlabel = 'Number of tokens', ylabel = 'Frequency'):
        """ Plots the tokens distribution """
        
        # get sentences sizes
        sentences_sizes, shortest, longest, average, percentiles = self.describe(corpus)

        # plot
        plt.hist(sentences_sizes, bins = bins)
        plt.xlabel(xlabel)
        plt.xlabel(ylabel)
        plt.show()

        # return sizes, shortest and longest values and average
        return sentences_sizes, shortest, longest, average, percentiles

    def plot_sentences_size_boxplot(self, corpus:list):

        # get sentences sizes
        sentences_sizes, shortest, longest, average, percentiles = self.describe(corpus)

        # plot boxplot
        plt.boxplot(sentences_sizes)
        plt.show()

        # return sizes, shortest and longest values and average
        return sentences_sizes, shortest, longest, average, percentiles
    
    def plot_representative_tokens(self, corpus:list, percentage=0.3):  
        #create corpus
        corpus      = self.atalaia.create_corpus(corpus)
        # let's lowercase everything first
        texts_lower = self.atalaia.lower_remove_white(corpus)
        # plot
        token_data  = self.atalaia.representative_tokens(percentage, 
                                                         texts_lower,
                                                         reverse=False)

        token_data     = token_data.items()
        token_data     = list(token_data)[:10]
        tokens, counts = zip(*token_data)

        # plot
        plt.figure(figsize=(20,10))
        plt.bar(tokens, 
                counts, 
                color='b')
        plt.xlabel('Tokens');
        plt.ylabel('Counts');
            
    
