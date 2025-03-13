
import string
import re
from nltk.tokenize import word_tokenize
import numpy as np
from tensorflow.keras.preprocessing.sequence import pad_sequences

from dataset import *


def countDig(string):
  digit_pattern = re.compile(r'\d')
  digit_matches = digit_pattern.findall(string)
  return len(digit_matches)



partialLookupDrugs = {}
fullLookupDrugs = {}
with open("drive/MyDrive/clases/MUD/DEL4+5-7.06/NERC-nn/lab_resources/DDI/resources/DrugBank.txt", encoding="utf-8") as f:
  for line in f.readlines():
      name,val=line.strip().lower().split("|")

      if name not in fullLookupDrugs:
         fullLookupDrugs[name]={}
      
      if val not in fullLookupDrugs[name]:
         fullLookupDrugs[name][val]=0
      fullLookupDrugs[name][val]+=1

      tokens = word_tokenize(name)
      for token in tokens:
         if token not in partialLookupDrugs:
            partialLookupDrugs[token]={}
      
         if val not in partialLookupDrugs[token]:
            partialLookupDrugs[token][val]=0
         partialLookupDrugs[token][val]+=1

with open("drive/MyDrive/clases/MUD/DEL4+5-7.06/NERC-nn/lab_resources/DDI/resources/HSDB.txt", encoding="utf-8") as f: 
   for line in f.readlines():
      name=line.strip().lower()
      val="drug"
      if name not in fullLookupDrugs:
         fullLookupDrugs[name]={}
      if val not in fullLookupDrugs[name]:
         fullLookupDrugs[name][val]=0
      fullLookupDrugs[name][val]+=1

      tokens = word_tokenize(name)
      for token in tokens:
         if token not in partialLookupDrugs:
            partialLookupDrugs[token]={}
      
         if val not in partialLookupDrugs[token]:
            partialLookupDrugs[token][val]=0
         partialLookupDrugs[token][val]+=1

def countLook(s):
  if s not in partialLookupDrugs:
    return 0
  res=0
  for i,val in enumerate(partialLookupDrugs[s]):
    res+=1<<i
  return res



class Codemaps :
    # --- constructor, create mapper either from training data, or
    # --- loading codemaps from given file
    def __init__(self, data, maxlen=None, suflen=None, prelen= None) :

        if isinstance(data,Dataset) and maxlen is not None and suflen is not None:
            self.__create_indexs(data, maxlen, suflen)

        elif type(data) == str and maxlen is None and suflen is None:
            self.__load(data)

        else:
            print('codemaps: Invalid or missing parameters in constructor')
            exit()

            
    # --------- Create indexs from training data
    # Extract all words and labels in given sentences and 
    # create indexes to encode them as numbers when needed
    def __create_indexs(self, data, maxlen, suflen, prelen=None) :

        self.maxlen = maxlen
        self.suflen = suflen
        self.prelen=prelen if prelen is not None else suflen
        words = set([])
        lc_words = set([])
        sufs = set([])
        labels = set([])
        lens = set([])
        pres = set([])
        dshs = set([])
        nums = set([])
        loks = set([])
        
        for s in data.sentences() :
            for t in s :
                words.add(t['form'])
                sufs.add(t['lc_form'][-self.suflen:])
                labels.add(t['tag'])
                lens.add(len(t['form']))
                pres.add(t['lc_form'][:self.prelen])
                dshs.add(t['lc_form'].count("-"))
                nums.add(countDig(t['lc_form']))
                loks.add(countLook(t['lc_form']))

        self.word_index = {w: i+2 for i,w in enumerate(list(words))}
        self.word_index['PAD'] = 0 # Padding
        self.word_index['UNK'] = 1 # Unknown words

        self.suf_index = {s: i+2 for i,s in enumerate(list(sufs))}
        self.suf_index['PAD'] = 0  # Padding
        self.suf_index['UNK'] = 1  # Unknown suffixes

        self.label_index = {t: i+1 for i,t in enumerate(list(labels))}
        self.label_index['PAD'] = 0 # Padding
  
        self.len_index = {s: i+2 for i,s in enumerate(list(lens))}
        self.len_index['PAD'] = 0  # Padding
        self.len_index['UNK'] = 1  # Unknown suffixes

        self.pre_index = {s: i+2 for i,s in enumerate(list(pres))}
        self.pre_index['PAD'] = 0  # Padding
        self.pre_index['UNK'] = 1  # Unknown suffixes

        self.dsh_index = {s: i+2 for i,s in enumerate(list(dshs))}
        self.dsh_index['PAD'] = 0  # Padding
        self.dsh_index['UNK'] = 1  # Unknown suffixes

        self.num_index = {s: i+2 for i,s in enumerate(list(nums))}
        self.num_index['PAD'] = 0  # Padding
        self.num_index['UNK'] = 1  # Unknown suffixes

        self.lok_index = {s: i+2 for i,s in enumerate(list(loks))}
        self.lok_index['PAD'] = 0  # Padding
        self.lok_index['UNK'] = 1  # Unknown suffixes
        
    ## --------- load indexs ----------- 
    def __load(self, name) : 
        self.maxlen = 0
        self.suflen = 0
        self.word_index = {}
        self.suf_index = {}
        self.label_index = {}
        self.len_index = {}
        self.pre_index = {}
        self.dsh_index = {}
        self.num_index = {}
        self.lok_index = {}

        with open(name+".idx") as f :
            for line in f.readlines(): 
                (t,k,i) = line.split()
                if t == 'MAXLEN' : self.maxlen = int(k)
                elif t == 'SUFLEN' : self.suflen = int(k)                
                elif t == 'WORD': self.word_index[k] = int(i)
                elif t == 'SUF': self.suf_index[k] = int(i)
                elif t == 'LABEL': self.label_index[k] = int(i)
                elif t == 'LEN': self.len_index[k] = int(i)
                elif t == 'PRE': self.pre_index[k] = int(i)
                elif t == 'DSH': self.dsh_index[k] = int(i)
                elif t == 'NUM': self.num_index[k] = int(i)
                elif t == 'LOK': self.lok_index[k] = int(i)
                            
    
    ## ---------- Save model and indexs ---------------
    def save(self, name) :
        # save indexes
        with open(name+".idx","w") as f :
            print ('MAXLEN', self.maxlen, "-", file=f)
            print ('SUFLEN', self.suflen, "-", file=f)
            for key in self.label_index : print('LABEL', key, self.label_index[key], file=f)
            for key in self.word_index : print('WORD', key, self.word_index[key], file=f)
            for key in self.suf_index : print('SUF', key, self.suf_index[key], file=f)
            for key in self.len_index : print('LEN', key, self.len_index[key], file=f)
            for key in self.pre_index : print('PRE', key, self.pre_index[key], file=f)
            for key in self.dsh_index : print('DSH', key, self.dsh_index[key], file=f)
            for key in self.num_index : print('NUM', key, self.num_index[key], file=f)
            for key in self.lok_index : print('LOK', key, self.lok_index[key], file=f)


    ## --------- encode X from given data ----------- 
    def encode_words(self, data) :        
        # encode and pad sentence words
        Xw = [[self.word_index[w['form']] if w['form'] in self.word_index else self.word_index['UNK'] for w in s] for s in data.sentences()]
        Xw = pad_sequences(maxlen=self.maxlen, sequences=Xw, padding="post", value=self.word_index['PAD'])
        # encode and pad suffixes
        Xs = [[self.suf_index[w['lc_form'][-self.suflen:]] if w['lc_form'][-self.suflen:] in self.suf_index else self.suf_index['UNK'] for w in s] for s in data.sentences()]
        Xs = pad_sequences(maxlen=self.maxlen, sequences=Xs, padding="post", value=self.suf_index['PAD'])
        # encode and pad length
        Xl = [[self.len_index[len(w['form'])] if len(w['form']) in self.len_index else self.len_index['UNK'] for w in s] for s in data.sentences()]
        Xl = pad_sequences(maxlen=self.maxlen, sequences=Xl, padding="post", value=self.len_index['PAD'])
        # encode and pad prefixes
        Xp = [[self.pre_index[w['lc_form'][:self.prelen]] if w['lc_form'][:self.prelen] in self.pre_index else self.pre_index['UNK'] for w in s] for s in data.sentences()]
        Xp = pad_sequences(maxlen=self.maxlen, sequences=Xp, padding="post", value=self.pre_index['PAD'])
        # encode and pad dashes
        Xd = [[self.dsh_index[w['lc_form'].count("-")] if w['lc_form'].count("-") in self.dsh_index else self.dsh_index['UNK'] for w in s] for s in data.sentences()]
        Xd = pad_sequences(maxlen=self.maxlen, sequences=Xd, padding="post", value=self.dsh_index['PAD'])
        # encode and pad digits
        Xn = [[self.num_index[countDig(w['lc_form'])] if countDig(w['lc_form']) in self.num_index else self.num_index['UNK'] for w in s] for s in data.sentences()]
        Xn = pad_sequences(maxlen=self.maxlen, sequences=Xn, padding="post", value=self.num_index['PAD'])
        # encode and pad digits
        Xk = [[self.lok_index[countLook(w['lc_form'])] if countLook(w['lc_form']) in self.lok_index else self.lok_index['UNK'] for w in s] for s in data.sentences()]
        Xk = pad_sequences(maxlen=self.maxlen, sequences=Xk, padding="post", value=self.lok_index['PAD'])
                

        # return encoded sequences
        return [Xw,Xs,Xl,Xp,Xd,Xn,Xk]

    
    ## --------- encode Y from given data ----------- 
    def encode_labels(self, data) :
        # encode and pad sentence labels 
        Y = [[self.label_index[w['tag']] for w in s] for s in data.sentences()]
        Y = pad_sequences(maxlen=self.maxlen, sequences=Y, padding="post", value=self.label_index["PAD"])
        return np.array(Y)

    ## -------- get word index size ---------
    def get_n_words(self) :
        return len(self.word_index)
    ## -------- get suf index size ---------
    def get_n_sufs(self) :
        return len(self.suf_index)
    ## -------- get len index size ---------
    def get_n_lens(self) :
        return len(self.len_index)
    ## -------- get pre index size ---------
    def get_n_pres(self) :
        return len(self.pre_index)
    ## -------- get dsh index size ---------
    def get_n_dshs(self) :
        return len(self.dsh_index)
    ## -------- get num index size ---------
    def get_n_nums(self) :
        return len(self.num_index)
    ## -------- get lookups index size ---------
    def get_n_loks(self) :
        return len(self.lok_index)
    ## -------- get label index size ---------
    def get_n_labels(self) :
        return len(self.label_index)

    ## -------- get index for given word ---------
    def word2idx(self, w) :
        return self.word_index[w]
    ## -------- get index for given suffix --------
    def suff2idx(self, s) :
        return self.suff_index[s]
    ## -------- get index for given label --------
    def label2idx(self, l) :
        return self.label_index[l]
    ## -------- get label name for given index --------
    def idx2label(self, i) :
        for l in self.label_index :
            if self.label_index[l] == i:
                return l
        raise KeyError

