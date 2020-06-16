# files are helper functions used to open files, get corpuses and save them back
import pandas as pd
import glob

def open_file(path:str):
    # get content from txt file
    f=open(path, "r")
    if f.mode == 'r':
        content=f.read()

    return content

def open_many_files(path:str, filetype="/*.csv"):
    # get all files on folder
    all_files = glob.glob(path + filetype)

    li = []

    for filename in all_files:
        df = pd.read_csv(filename, index_col=None, header=0)
        li.append(df)

    data = pd.concat(li, axis=0, ignore_index=True)
    
    return data

def save_file(content, path:str, mode:str):
    f = open(path , mode)
    f.write(content)
    f.close()

def get_corpus(corpus_path:str, ispandas:False, text_column='text'): 
    ''' Get corpus from a file'''

    if ispandas == True:
        return list(pd.read_csv(corpus_path)[text_column])
    else:
        # get corpus from txt file
        corpus = open_file(corpus_path)
            
        return [corpus]
