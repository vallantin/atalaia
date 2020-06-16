"""
Handles the vector tasks
"""
# imports
from gensim.models import Word2Vec
from gensim.models.keyedvectors import KeyedVectors
from atalaia.files import save_file
from atalaia.files import open_file

def vectorize(sentences:list, 
              size=300,
              min_count=5,
              window=5,
              workers=8,
              sg=1,
              path='../models/keyla/word_vector_',
              model_version='0_0_1',
              save_txt=True):

    """Uses Gensim to train word vectors for different languages
            
    Parameters
    ----------
    language : str  
        The language you want to use to train the model
    sentences : list
        A list with the texts you want to use to train your model
    size : int
        Dimensionality of the word vectors
    min_count : int
        The number of times that a token has to appear on the corpus. Useful to ignore low frequency tokens.
    window : int
        Maximum distance between the current and predicted token within a sentence.
    workers : int
        Number of worker threads to train the model
    sg : int
        Training algorithm: 1 for skip-gram; otherwise CBOW.
    path : str
        Where to save the model. 
    model_version : str
        The version of the vector you want to train. 
    """

    print('Training model. Wait!')
    model = Word2Vec(sentences=sentences, size=size, window=window, min_count=min_count, workers=workers, sg=sg)

    # save keyed vectors
    print('Saving word2vec classic model format')
    model.save(path + model_version)
    if save_txt == True:
        print('Saving txt format')
        model.wv.save_word2vec_format(path + model_version + '.txt', binary=False)

    print('Vectors saved')


    return model

def update_model(sentences:list,
                 path='../models/keyla/word_vector_',
                 model_version='0_0_1'):

    """Continue to train an already saved model with more sentences
            
    Parameters
    ----------
    language : str  
        The language you want to use to train the model
    sentences : list
        A list with the new texts you want to use to train your model
    path : str
        Where to save the model. Default value is Atalaia workspace
    model_version : str
        The version of the vector you want to train. Must be in format x_x_x
    """

    model = _load_vectors(path, model_version)
    model.train(sentences, 
                total_examples=model.corpus_count,
                epochs=model.epochs)

    # save keyed vectors
    model.save(path + model_version)
    print('Vectors saved')

    return model


def _load_vectors(path='../models/keyla/',
                  model_version='0_0_1'):

    """Loads an already trained model
            
    Parameters
    ----------
    language : str  
        The language you want to use to train the model
    path : str
        Where to save the model. Default value is Atalaia workspace
    model_type : list
        The name of the vector. Default is 'word_vector'
    model_version : list
        The version of the vector you want to train. Must be in format x_x_x
    """

    #model = Word2Vec.load(path + 'word_vectors_' + model_version)
    model = KeyedVectors.load(path + model_version, mmap='r')
    return model

def convert2glove(path, model_version):
    model_txt = open_file('{}{}.txt'.format(path, model_version))
    model_txt = model_txt.split('\n')
    model_txt = '\n'.join(model_txt[1:])
    save_file(model_txt, '{}{}_glove.txt'.format(path, model_version), 'w+')




