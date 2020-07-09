# TODOS
#--------------------------------------
# imports
import emoji
import math
import os
import random
import re
import time
import unicodedata
from atalaia import strings
from collections import Counter
from nltk.stem.snowball import SnowballStemmer
from atalaia.assets.stopwords import stopwords_pt_br, stopwords_en
from atalaia.assets.contractions import contractions_en, contractions_pt_br, contractions_fr
from tqdm import tqdm
from random import choice
from collections import Counter
import requests
import json


class Atalaia:
    """Atalaia is a collection of methods that can be used for simple NLP tasks.
    It can be used for tasks involving text preprocessing for machine learning.
    Atalaia works mainly with text strings and lists of strings. 
    """
    
    def __init__(self, language:str):
        """
        Parameters
        ----------
        language : str
            The language used to initialize Atalaia. Accepts 'pt-br', 'en' and 'fr'
        lg_config : str
            The language used for NLTK, generated by the method language_for_nltk
        vocab : Counter()
            The number of unique tokens found on the text
        sentences
            The tokenizer for tokenizing sentences 
        """ 
        self.stopwords = {}
        self.contractions = contractions_en
        self.language = language
        self.lg_config = self.__lg_config()
        self.vocab = Counter()

    def __lg_config(self):
        """ Converts the language inputed during Atalaia init to a format that can be used by NLTK"""
        if self.language == 'pt-br':
            self.stopwords.update(stopwords_pt_br)
            self.contractions = contractions_pt_br
            return 'portuguese'
        if self.language == 'en':
            self.stopwords.update(stopwords_en)
            self.contractions = contractions_en
            return 'english'
        if self.language == 'fr':
            self.contractions = contractions_fr
            return 'french'
        if self.language == 'custom':
            return 'portuguese'

    def remove_html_tags(self, text:str):
        """Removes html tags from text

        >>> remove_html_tags('<h1><strong>Hello world!</strong></h1>')
        'Hello world!'

        Parameters
        ----------
        text : str
            The string that will be transformed
        """
        text = re.sub(r'<[^>]*>', '', text)
        return text

    def expand_contractions(self, text):
        '''Expands contracted tokens. Doesn't ignore the case '''

        # check the patterns
        for pattern, replacement in self.contractions.items():
            text = re.sub(pattern, replacement, text)

        return text

    def replace_html_tags(self, text:str, placeholder:str):
        """Replaces html tags from text by a given placeholder
        
        >>> replace_html_tags('<h1><strong>Hello world!</strong></h1>', 'HTML')
        'HTML HTML Hello world! HTML HTML'

        Parameters
        ----------
        text : str
            The string that will be transformed
        placeholder : str
            The string that will replace the html tag
        """
        text = re.sub(r'<[^>]*>', ' ' + placeholder + ' ', text)
        text = self.remove_excessive_spaces(text)
        return text

    def remove_urls(self, text:str):
        """Removes urls from text

        >>> remove_urls('You can go to the page http://homepage.com to see the content.')
        'You can go to the page to see the content.'
        
        Parameters
        ----------
        text : str
            The string that will be transformed
        """
        text = re.sub(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', '', text)
        text = self.remove_excessive_spaces(text)
        return text

    def replace_urls(self, text:str, placeholder:str):
        """Replaces links from text by a given placeholder
        
        >>> replace_urls('You can go to the page http://homepage.com to see the content.', 'URL')
        'You can go to the page URL to see the content.'

        Parameters
        ----------
        text : str
            The string that will be transformed
        placeholder : str
            The string that will replace the url
        """
        text = re.sub(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', placeholder, text)
        return text

    def see_on_context(self, pattern, corpus, align=True, length=34):
        """See all sentences where a token or a regex pattern appear"""
        if align == True:
            sentences = []
            compiler = re.compile(pattern)

            # iterate over corpus
            for c in corpus:
                for result in compiler.finditer(c):
                    # get the start and the end of a sentence as defined by the length. 
                    # this will be the sentence boundaries
                    start = result.start()-length
                    end = result.start()+len(result.group())+length
                    # get sentence itself
                    sentence = c[start:end]
                    # sometimes the regex will pick sentences that were part of a longer
                    # sentence, but that don't have the term. Let's keep only the ones
                    # where the term appears.
                    if re.search(pattern, sentence) != None:
                        sentences.append(sentence)

            # kep unique sentences
            sentences = list(set(sentences))
            return sentences
                        
            #return list(set([c[result.start()-length:result.start()+len(result.group())+length] for c in corpus for result in compiler.finditer(c)]))
        else:
            return list(set([c for c in corpus if re.search(pattern, c) != None]))

    def similar(self, pattern, corpus, mode='single'):
        '''Retuns the closest tokens to a given word or pattern'''
        # build tuples of three, where the middleelement is the pattern
        print('Tokenizing')
        corpus = [['START'] + self.tokenize(c) + ['END'] for c in corpus]
        # start getting tuples
        print('Building trigrams')
        trigrams = [trigram for c in corpus for trigram in self.__trigrams(c)]
        # get all tuples where the pattern is present. If no pattern is given, return all
        if pattern != '':
            print('Getting gold grams')
            gold_grams = [trigram for trigram in trigrams if re.search(pattern, trigram[1]) != None]
        else:
            print('Returning all the trigrams')
            gold_grams = trigrams
        # now, look for all trigrams where t[0] and t[2] match the gold_grams
        print('Getting similars...')
        if mode == 'single':
            similars = [trigram[1] for trigram in trigrams for gold in gold_grams if trigram[0] == gold[0] and trigram[2] == gold[2]]
        if mode == 'trigram':
            similars = [trigram for trigram in trigrams for gold in gold_grams if trigram[0] == gold[0] and trigram[2] == gold[2]]

        return list(set(similars))

    def __trigrams(self, tokens):
        '''Get all possible trigrams on a 3 tokens window'''
        
        return [(tokens[i-1], tokens[i], tokens[i+1]) for i in range(1,len(tokens)-1)]
            
            
    def remove_hashtags(self, text:str):
        """Removes hashtags from text
        
        >>> remove_hashtags('I wish you all #love and #peanceandlove')
        'I wish you all and !'

        Parameters
        ----------
        text : str
            The string that will be transformed
        """
        text = re.sub(r'\B(\#[a-zA-Z]+\b)(?!;)', '', text)
        text = self.remove_excessive_spaces(text)
        return text

    def replace_hashtags(self, text:str, placeholder:str):
        """Replaces hashtags from text by a given placeholder

        >>> replace_hashtags('I wish you all #love and #peace', 'HASHTAG')
        'I wish you all HASHTAG and HASHTAG'
        
        Parameters
        ----------
        text : str
            The string that will be transformed
        placeholder : str
            The string that will replace the hashtag
        """
        text = re.sub(r'\B(\#[a-zA-Z]+\b)(?!;)', placeholder, text)
        return text

    def remove_ips(self, text:str):
        """Removes ips from text

        >>> remove_ips('This can be accessed on the address 198.162.0.1.')
        'This can be accessed on the address .'

        Parameters
        ----------
        text : str
            The string that will be transformed
        """
        text = re.sub(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', '', text)
        text = self.remove_excessive_spaces(text)
        return text

    def replace_ips(self, text:str, placeholder:str):
        """Replaces ips from text by a given placeholder

        >>> replace_ips('This can be accessed on the address 198.162.0.1.', 'IP')
        'This can be accessed on the address IP.'

        Parameters
        ----------
        text : str
            The string that will be transformed
        placeholder : str
            The string that will replace the ip
        """
        text = re.sub(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', placeholder, text)
        return text

    def remove_handles(self, text:str):
        """Removes handles from text

        >>> remove_handles('Can you come tonight, @alice?')
        'Can you come tonight, ?'

        Parameters
        ----------
        text : str
            The string that will be transformed
        """
        text = re.sub(r'\B(\@[a-zA-Z_0-9]+\b)(?!;)', '', text)
        text = self.remove_excessive_spaces(text)
        return text

    def replace_handles(self, text:str, placeholder:str):
        """Replaces handles from text by a given placeholder

        >>> replace_handles('Can you come tonight, @alice?', 'USERNAME')
        'Can you come tonight, USERNAME?'

        Parameters
        ----------
        text : str
            The string that will be transformed
        placeholder : str
            The string that will replace the handle
        """
        text = re.sub(r'\B(\@[a-zA-Z_0-9]+\b)(?!;)', placeholder, text)
        return text

    def strip_accents(self, text:str):
        """Strip accents from tokens

        >>> strip_accents('Mamãe me disse: você é o menino mais ágil do time.')
        'Mamae me disse: voce e o menino mais agil do time.'
        
        Parameters
        ----------
        text : str
            The string that will be transformed
        """
        try:
            text = unicode(text, 'utf-8')
        except NameError: 
            pass

        text = unicodedata.normalize('NFD', text)\
            .encode('ascii', 'ignore')\
            .decode("utf-8")

        return str(text)

    def replace_quotes(self, text:str, placeholder:str):
        """Replaces quotes by a placeholder

        >>> replace_quotes('She told me: "you are a confident and strong woman".', 'QUOTED')
        'She told me: QUOTED you are a confident and strong woman QUOTED .'

        Parameters
        ----------
        text : str
            The string that will be transformed
        placeholder : str
            The string that will replace the quote sign
        """
        text = re.sub(r'"', ' ' + placeholder + ' ', text)
        text = re.sub(r"'", ' ' + placeholder + ' ', text)
        text = self.remove_excessive_spaces(text)
        return text

    def remove_punctuation(self, text:str):
        """Removes ponctuation and special chars

        >>> remove_punctuation('Hey, are you here??? I really need your help!')
        'Hey are you here I really need your help'
        
        Parameters
        ----------
        text : str
            The string that will be transformed
        placeholder : str
            The string that will replace the punctuation and the special chars found
        """
        text = re.sub(r'[^\w\s&]', ' ', text)
        text = self.remove_excessive_spaces(text)
        return text

    def replace_punctuation(self, text:str, sign='', placeholder=''):
        """Replaces punctuation by a placeholder.

        >>> replace_punctuation('Hey, are you here??? I really need your help!', sign='?', placeholder='QUESTION')
        'Hey, are you here QUESTION QUESTION QUESTION I really need your help!'
        
        Parameters
        ----------
        text : str
            The string that will be transformed
        sign : str
            The symbol you want to replace. If no symbol is provided, will replace all special chars and punctuation by the placeholder
        placeholder : str
            The string that will replace the punctuation and the special chars found
        """
        if sign is '':
            text = re.sub(r'[^\w\s]', ' ' + placeholder + ' ', text)    
        else:
            text = text.replace(sign, ' ' + placeholder + ' ')
        
        text = self.remove_excessive_spaces(text)
        return text

    def remove_numbers(self, text:str):
        """Removes all numbers

        >>> remove_numbers('I told him 1,2,3,4 times that he could not do that!')
        'I told him ,,, times that he could not do that!'

        Parameters
        ----------
        text : str
            The string that will be transformed
        """
        text = re.sub(r'[0-9]', '', text)
        text = self.remove_excessive_spaces(text)
        return text

    def replace_numbers(self, text:str):
        """Replaces all numbers for string

        >>> replace_numbers('I told him 1,2,3,4 times that he could not do that!')
        'I told him one, two, three, four times that he could not do that!'. 
        Attention: It does NOT convert numbers like 20 to twenty, but to
        two zero.

        Parameters
        ----------
        text : str
            The string that will be transformed
        """
        if self.language == 'pt-br':
            text = text.replace('0', ' zero ')
            text = text.replace('1', ' um ')
            text = text.replace('2', ' dois ')
            text = text.replace('3', ' três ')
            text = text.replace('4', ' quatro ')
            text = text.replace('5', ' cinco ')
            text = text.replace('6', ' seis ')
            text = text.replace('7', ' sete ')
            text = text.replace('8', ' oito ')
            text = text.replace('9', ' nove ')
        if self.language == 'fr':
            text = text.replace('0', ' zéro ')
            text = text.replace('1', ' un ')
            text = text.replace('2', ' deux ')
            text = text.replace('3', ' trois ')
            text = text.replace('4', ' quatre ')
            text = text.replace('5', ' cinc ')
            text = text.replace('6', ' six ')
            text = text.replace('7', ' sept ')
            text = text.replace('8', ' huit ')
            text = text.replace('9', ' neuf ')
        if self.language == 'en':
            text = text.replace('0', ' zero ')
            text = text.replace('1', ' one ')
            text = text.replace('2', ' two ')
            text = text.replace('3', ' three ')
            text = text.replace('4', ' four ')
            text = text.replace('5', ' five ')
            text = text.replace('6', ' six ')
            text = text.replace('7', ' seven ')
            text = text.replace('8', ' eight ')
            text = text.replace('9', ' nine ')
            
        text = self.remove_excessive_spaces(text)
        return text

    def stem_sentence(self, text:str, sep='_'):
        """Uses NLTK stemmer to stem tokens

        >>> stem_sentence('I love to go shopping with my mother and friends')
        'i love to go shop with my mother and friend'

        Parameters
        ----------
        text : str
            The string that will be transformed
        sep : str
            Here you can inform wich separator was used to merge the word to the tag
        """
        stemmer = SnowballStemmer(self.lg_config)
        sentence = []
        words_tags = []
        words = []
        tags = []

        # removes more than one whitespace 
        text = re.sub(r'\s{2,}', ' ', text)
        
        for word in self.tokenize(text):
            word = stemmer.stem(str(word))
            sentence.append(word)

        text = ' '.join(sentence)
        
        return text

    def remove_stopwords(self, text:str, custom_list=[], extend_set=False):
        '''Removes stopwords'''

        # check in stopwords
        for pattern, replacement in self.stopwords.items():
            text = re.sub(pattern, replacement, text, flags=re.I | re.M)
            text = self.remove_excessive_spaces(text)
            # run second time to match chars that could not me matched at first
            text = re.sub(pattern, replacement, text, flags=re.I | re.M)
 
        return text

        '''
        """ Removes stopwords

        >>> remove_stopwords('I love to go shopping with my mother and friends')
        'love go shopping mother friends'

        Parameters
        ----------
        text : str
            The string that will be transformed
        custom_list : list
            A list with the custom stopwords list
        extend_set : boolean
            Use this option to extend the stopwords of a given language with your custom list 
        """
        # define the stopwords set to use
        if self.language == 'pt-br':
            stop_words = stopwords.portuguese
        elif self.language == 'en':
            stop_words = stopwords.english
        elif self.language == 'fr':
            stop_words = stopwords.french
        elif self.language == 'custom':
            stop_words = custom_list
        else:
            print('This set is not available. No stopword will be removed!')
            stop_words = []

        # extend with a list of custom words
        if extend_set == True:
            stop_words = stop_words + custom_list

        # add spaces to the beginning and to the end of the sentence, 
        # so stopwords on these locations can be spotted
        text = ' ' + text + ' '

        for word in stop_words:
            text = re.sub(r'\s' + word + r'\s', ' ', text, flags=re.I)
            if self.language == 'fr':
                text = re.sub(re.escape('j\''), ' ', text, flags=re.I)
                text = re.sub(re.escape('d\''), ' ', text, flags=re.I)
                text = re.sub(re.escape('l\''), ' ', text, flags=re.I)
                text = re.sub(re.escape('m\''), ' ', text, flags=re.I)
                text = re.sub(re.escape('s\''), ' ', text, flags=re.I)
                text = re.sub(re.escape('t\''), ' ', text, flags=re.I)
            
        # strip adititonal the spaces
        text = text.strip()
        text = self.remove_excessive_spaces(text)
        return text
        '''

    def reduce_words_with_repeated_chars(self, text:str):
        """Reduces words with chars repeated more than 3 times to a single char. 
        Useful to replace words such as loooooooong by long. Be careful, 
        as it can change abreviations such as AAA to single A 

        >>> reduce_words_with_repeated_chars('I loooooooooooooove pizza so muuuchhhh')
        'I love pizza so much'

        Parameters
        ----------
        text : str
            The string that will be transformed
        """
        
        text = re.sub(r'(\w)\1{2,}', '\\1', text, flags=re.IGNORECASE)
        return self.remove_excessive_spaces(text)


        '''
        findings = re.findall(r'(\w)\1{2,}', text)
        for char in findings:
            find = char + '{3,}'
            #replace = char + '\1' + '???'
            replace = '???' + char + '???'
            text = re.sub(find, repr(replace), text)

        # Now we can remove the placeholders    
        text = text.replace('\'???','')
        text = text.replace('???\'','')

        text = self.remove_excessive_spaces(text)
        return text
        '''
        
    def remove_excessive_spaces(self, text:str):
        """Removes excessive space from text

        >>> remove_excessive_spaces('I  can\'t     stop looking at  you')
        'I can't stop looking at you'

        Parameters
        ----------
        text : str
            The string that will be transformed
        """
        # replace \xa0 by true spaces
        text = text.replace(u'\xa0', u' ').replace('\x0b', u' ')
        # remove more than one space
        text = re.sub(r'\s{2,}', ' ', text)
        # remove spaces in the beginning and in the end of the string
        text = text.strip()
        return text

    def replace_newline(self, text:str, replacement='. ', consider_punctuation=True):
        """ Use it to replace newline \n
        
        >>> replace_newline("- Mary is coming! \n- When? \n- Today!")
        '- mary is coming!  - when?  - today!'

        Parameters
        ----------
        text : str
            The string that will be transformed
        replacement : str
            The replacement to the newline char
        consider_punctuation : bool
            If True, sentences ending with ?.!,:;= will only be trimmed. Replacement won't be applied
        """
        if consider_punctuation:
            if re.search(r'[?.!,:;=]\n', text):
                # match all punct newline patterns and replace them by the punct only
                text = re.sub(r'([?.!,:;=])\n', '\\1 ', text )
                # then, do other replacements with newline
                text = text.replace('\n', replacement )
            else: 
                text = text.replace('\n', replacement )
        else:
            # then, do other replacements with newline
            text = text.replace('\n', replacement )

        return text

    def lower_remove_white(self, text:str):
        """ Use it to lower text and to remove trailing whitespaces
        
        >>> lower_remove_white("- Mary is coming! \n- When? \n- Today!")
        '- mary is coming!  - when?  - today!'

        Parameters
        ----------
        text : str
            The string that will be transformed
        """
        
        # lower text
        text = text.lower()
        # strip trailing whitespaces
        text = re.sub(r'\n', ' ', text)

        return text

    def preprocess(self, text:str, tokenize=True, stem=True, remove_stopwords=False, replace_numbers=False, remove_numbers=False, remove_punct=True, strip_accs = True, expand_contractions=False, replace_newline=False):
        """Preprocess text before data handling with most common settings.
        Text is processed in the following order:

            - lower text
            - replace newline
            - expand contractions
            - strip trailing whitespaces
            - convert emojis to text
            - replace urls
            - remove tags
            - replace hashtags
            - replace ips
            - remove social media handles
            - replace numbers
            - reduce loooooong words
            - remove punctuation
            - remove excessive spaces     
            - tag text if True
            - remove stopwords if True
            - remove accents
            - remove excessive spaces
            - stem text if True
            - tokenize text (if True, will return a list of tokens)

        >>> preprocess("At the end of the day, you're solely responsible for your success and your failure. And the sooner you realize that, you accept that, and integrate that into your work ethic, you will start being successful. As long as you blame others for the reason you aren't where you want to be, you will always be a failure.")
        '['end', 'day', 'sole', 'respons', 'success', 'failur', 'sooner', 'realiz', 'that', 'accept', 'that', 'integr', 'work', 'ethic', 'start', 'success', 'long', 'blame', 'other', 'reason', 'want', 'be', 'alway', 'failur']'
        
        Parameters
        ----------
        text : str
            The string that will be transformed
        tokenize : bool
            Defines if the text should be tokenized or not
        stem : bool
            Defines if the tokens should be stemmed or not
        remove_stopwords : bool
            Defines if stopwords should be removed.
        replace_numbers : bool
            Defines if numbers should be interpreted as strings (Eg.: 1 -> 'one')
        """
        text = str(text)
        # should newlines be replaced? Standard config will be applied
        if replace_newline == True:
            text = self.replace_newline(text)
        # expand contractions
        if expand_contractions == True:
            text = self.expand_contractions(text)
        # remove stopwords
        if remove_stopwords:
            text = self.remove_stopwords(text)
        # lowers text and removes trailing spaces
        text = self.lower_remove_white(text)
        # emoji to text
        text = emoji.demojize(text)
        # replace urls
        text = self.replace_urls(text, 'URL')
        # remove tags
        text = self.remove_html_tags(text)
        # replace hashtags
        text = self.replace_hashtags(text, 'HASHTAG')
        # replace ips
        text = self.replace_ips(text, 'IP')
        # remove social media handles
        text = self.remove_handles(text)
        # replace numbers
        if replace_numbers == True:
            text = self.replace_numbers(text)
        if remove_numbers == True:
            text = self.remove_numbers(text) 
        # reduce loooooong words
        text = self.reduce_words_with_repeated_chars(text)
        # remove punctuation    
        if remove_punct == True:
            text = self.remove_punctuation(text)
        # remove excessive spaces
        text = self.remove_excessive_spaces(text)
        # remove accents     
        if strip_accs == True:
            text = self.strip_accents(text)
        # remove excessive spaces
        text = self.remove_excessive_spaces(text)
        # stem text
        if stem:
            text = self.stem_sentence(text)
        # tokenize
        if tokenize == True:
            text = self.tokenize(text)
            self.vocab.update(text)
        if tokenize == False:
            # updates list of words
            self.vocab.update(self.tokenize(text))
        # return text
        return text
            
    def preprocess_list(self, text_list:list, tokenize=True, stem=True, remove_stopwords=False, replace_numbers=False, remove_numbers=False, remove_punct=True, strip_accs=True, expand_contractions=False, replace_newline=False):
        """Preprocess every text in a list of strings

        >>> list_of_strings = [
        'I love you',
        'Please, never leave me alone',
        'If you go, I will die',
        'I am watching a lot of romantic comedy lately',
        'I have to eat icecream'
        ]

        >>> list_processed = atalaia_en.preprocess_list(list_of_strings, stem=False)
        '['end', 'day', 'sole', 'respons', 'success', 'failur', 'sooner', 'realiz', 'that', 'accept', 'that', 'integr', 'work', 'ethic', 'start', 'success', 'long', 'blame', 'other', 'reason', 'want', 'be', 'alway', 'failur']'

        Parameters
        ----------
        text : list
            The list of strings to be transformed
        tokenize : boolean
            Defines if the text should be tokenized or not
        stem : boolean
            Defines if the tokens should be stemmed or not
        remove_stopwords : boolean
            Defines if stopwords should be removed.
        """
        texts = []
        for text in text_list:
            # preprocess
            text = self.preprocess(text, tokenize=tokenize, stem=stem, remove_stopwords=remove_stopwords, replace_numbers=replace_numbers, remove_numbers=remove_numbers, remove_punct=remove_punct, strip_accs = strip_accs, expand_contractions=expand_contractions)
            texts.append(text)
        return texts

    def create_corpus(self, text_list:list):
        """Receives a list of strings and returns a single string with all the text

        >>> list_of_strings = ['I love you', 'Please, never leave me alone', 'If you go, I will die', 'I am watching a lot of romantic comedy lately', 'I have to eat icecream']
        >>> create_corpus(list_of_strings)
        'I love you Please, never leave me alone If you go, I will die I am watching a lot of romantic comedy lately I have to eat icecream'

        Parameters
        ----------
        text : list
            The list of strings that will be used to return the corpus
        """
        return ' '.join(text_list)

    def vocab_size(self, corpus:str):
        """Returns the number of unique tokens found on the corpus

        >>> vocab_size('  I love you Please, never leave me alone If you go, I will die I am watching a lot of romantic comedy lately I have to eat icecream')
        24

        Parameters
        ----------
        corpus : str
            The string that holds the entire corpus
        """
        words_map_dict = Counter(corpus.split())
        unique_words = len(words_map_dict.keys())
        vocab_size = int(unique_words)

        return vocab_size

    def lexical_diversity(self, corpus_slice:str, corpus:str):
        """Counts the vocab of one part of the corpus and compares it to the entire corpus

        >>> lexical_diversity(list_of_strings[0], corpus)
        0.125

        Parameters
        ----------
        corpus_slice : str
            The string that you want to analyse
        corpus : str
            The string that holds the entire corpus
        """
        # count vocab for slice 
        slice_vocab = self.vocab_size(corpus_slice)

        # count vocab for entire corpus
        all_vocab = self.vocab_size(corpus)

        # calculate diversity
        diversity = slice_vocab/all_vocab
        return diversity

    def random_classification(self, list_to_classify:list, classes:list, balanced=True):
        '''Receives a list of sentences and assigns randomly a label for each item
        on the list. Returns a list with all the random labels.
        
        >>> random_classification(['A sentence', 'Another sentence'][0,1])
            [1,1]

        Parameters
        ----------
        list_to_classify : list
            A list that holds all the text that needs to be randomly labelized
                
        classes : list
            A list that holds the possible classes

        balanced : boolean
            If True, resulting labels will have an equal or near equal number of examples
        '''
        
        labels = []

        if balanced == False:
            # iterates over the list and picks a random label
            for sentence in list_to_classify:
                labels.append(random.choice(classes))
        else:
            examples_len = len(list_to_classify)
            classes_len = len(classes)
            examples_per_class = math.ceil(examples_len/classes_len)

            # initializes counter 
            class_counter = {}
            for available_label in classes:
                class_counter[available_label] = 0

            # iterates over the list and picks a random label
            for sentence in list_to_classify:
                random_class = random.choice(classes)
                # check if class is already completed
                if class_counter[random_class] <= examples_per_class:
                    # adds label to labels list
                    labels.append(random_class)
                    # updates counter
                    class_counter[random_class] += 1
                else:
                    # remove classwih enough values from list
                    classes.remove(random_class)
                    # picks a new random value and adds to final labels list
                    labels.append(random.choice(classes))

            # print final number of examples
            for k, v in class_counter.items():
                print('Class {}: {} values'.format(k, v))

        return labels

    def replace_with_blob(self, list_of_texts:list):
        '''Receives a list of sentences and creates blobs with the same 
        vocabulary found on corpus.
        
        >>> random_classification(['A sentence', 'Another sentence'][0,1])
            ['sentence Another', 'A Another']

        Parameters
        ----------
        list_of_texts : list
            A list that holds all the text that needs to become blob
        '''
        
        # create vocab list
        vocab = list(self.create_corpus(list_of_texts).split(' '))

        # create lists that will hold the sentences
        sentence = []
        sentences = []
        
        for text in list_of_texts:
            # get the lenght for each text on the list
            text_len = len(str(text).split(' ')) 
            
            # iterate over each text and replace token by a token from vocab
            for x in range(text_len):
                sentence.append(random.choice(vocab))

            # recreate sentence and clean sentence list
            text = ' '.join(sentence)
            sentence = []

            # append recreated sentence to list
            sentences.append(text)

        return sentences

    def tokenize(self, text:str):
        '''Receives a string and splits it into tokens.
        Returns a list with all the tokens found.

        >>> tokenize('I want to eat mow.")
            ['I', 'want', 'to', 'eat', 'now', '.']

        Parameters
        ----------
        text : str
            The text that will be tokenized
        '''
        #convert emojis to protect them
        text = emoji.demojize(text)
        #keep words with '-' together
        #results= re.finditer(r'(\w+[\'-]\w+)|(\w+)(\s?[&]\s?)(\w+)|(?:[A-Z]\.)+|:(\w+):|http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+|#(\w+)|@(\w+)|(\w+)|([°/\<\>\-.:*\[\],!?+"§$%&()])', text, re.MULTILINE)
        #don't keep words with '-' together
        #results = re.finditer(r'(\w+[\']\w+)|(\w+)(\s?[&]\s?)(\w+)|(?:[A-Z]\.)+|:(\w+):|http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+|#(\w+)|@(\w+)|(\w+)|([°/\<\>\-.:*\[\],!?+"§$%&()])', text, re.MULTILINE)
        #don't keep &
        results = re.finditer(r'(\w+[\']\w+)|(?:[A-Z]\.)+|:(\w+):|http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+|#(\w+)|@(\w+)|(\w+)|([°/\<\>\-.:*\[\],!?+"§$%&()])', text, re.MULTILINE)


        # get individual tokens and get emojis back
        tokens = [emoji.emojize(text[r.start():r.end()]) for r in results]
        
        return tokens

    def remove_ner_training_labels(self, text):
        """Removes NER training labels"""
        for tag in vocab.possible_tags:
            text = text.replace('_'+ tag + '__', '')
        
        text = text.replace('__','')

        return text

    def random_pick(self, corpus, n):
        '''Picks n elements from a list'''

        def in_choices(choosed, choices):
            if choosed not in choices:
                return False
            else:
                return True
        
        choices = []
        for i in range(n):
            choosed = choice(corpus)
            # if already choosen...
            while in_choices(choosed, choices) == True:
                choosed = choice(corpus)
            #if new, append to choices
            choices.append(choosed)

        return choices

    def hapaxes(self, corpus):
        '''Looks for tokens that ocurred only once in the whole corpus'''
        cnt = Counter()
        corpus = ' '.join(corpus)
        # tokenize the corpus
        for token in tqdm(self.tokenize(corpus)):
            cnt[token] += 1
        cnt = dict(cnt)

        hapaxes = []
        for k, v in cnt.items():
            if v == 1:
                hapaxes.append(k)

        return hapaxes
                
    def get_average_sentence_length(self, sentences:list, mode='mean'):

        '''Calculates the average size of a sentence in a list of sentences. Use mode
        to decide if you want the mean or the median'''

        sizes = [len(self.tokenize(s)) for s in sentences]

        if mode == 'mean':
            return sum(sizes) / len(sizes) 
        if mode == 'median':
            n = len(sizes) 
            sizes.sort() 
            
            if n % 2 == 0: 
                median1 = sizes[n//2] 
                median2 = sizes[n//2 - 1] 
                median = (median1 + median2)/2
            else: 
                median = sizes[n//2] 
            
            return median

    def representative_tokens(self, percentage:float, corpus:str, reverse=False):

        '''Given a corpus and a percentage, get the tokens responsible for this percentage on the corpus'''

        #tokenize corpus
        tokens = self.tokenize(corpus)
        
        # count them
        tokens_counter = dict(Counter(tokens))

        # get the percentage of each token in corpus
        total_tokens   = len(tokens)
        tokens_counter = {k: v/total_tokens for k, v in tokens_counter.items()}

        if reverse == False:
            # sort so highest tokens come first
            tokens_counter = {k: v for k, v in sorted(tokens_counter.items(), reverse=True, key=lambda item: item[1])}
        elif reverse == True:
            # sort so lowest tokens come first
            tokens_counter = {k: v for k, v in sorted(tokens_counter.items(), key=lambda item: item[1])}

        # iterate until the sum corresponds to the given percentage
        main_tokens = {}
        count       = 0
        for k, v in tokens_counter.items():
            if count <= percentage:
                main_tokens[k] = v       
                count += v

        return main_tokens


    def from_json(self, url:str, payload={}, dump=False):

        '''Fetches a json response given an url and a dict of params'''

        # Fetch data from a REST API
        r = requests.get(url, params=payload)
        res = r.json()

        if dump == False:
            return res
        elif dump == True:
            return json.dumps(res, indent=4)
