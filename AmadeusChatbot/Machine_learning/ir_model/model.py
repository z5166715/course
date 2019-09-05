# information retrival model class
from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd
import pymysql
import numpy as np
import heapq
from machine_learning.ir_model.config import Config
# import model.config as config
import warnings
from sklearn.metrics.pairwise import cosine_similarity
warnings.filterwarnings('ignore')
import database.dao as dao

import nltk
import math
import string
from nltk.corpus import stopwords
from collections import Counter
from nltk.stem.porter import *
import os
import pickle


class inforetrival_model:
    # init with call cal so we dont need more compuation on tfidf matrix
    def __init__(self):
        temp=self.cal_tfidfmatrix()
        self.vectorizer=temp[0]
        self.tfidf_mat=temp[1]
        self.df=temp[2]

    def prepocess(self,text):
        def tokenize(text):
            lowers=text.lower()
            remove_punctuation_map = dict((ord(char), None) for char in string.punctuation)
            no_punctuation = lowers.translate(remove_punctuation_map)
            return nltk.word_tokenize(no_punctuation)

        def del_stoppingword(tokens):
            return [x for x in tokens if not x in stopwords.words('english')]

        def stem_tokens(tokens, stemmer=PorterStemmer()):
            stemmed = []
            for item in tokens:
                stemmed.append(stemmer.stem(item))
            return stemmed

        p_res=stem_tokens(del_stoppingword(tokenize(text)))
        return ' '.join(p_res)

        pass

    def cal_tfidfmatrix(self):
        # if the model already in the dir dont need to re-compute
        try:
            f=open('ir_data','rb')
            l=pickle.load(f)
            return l
        except:
            print('no that file.')
        text = dao.query_all_qapair_title(dao.connectdb())
        text = np.asarray(text)
        for index in range(len(text)):
            text[index][1] = self.prepocess(text[index][1])
        df = pd.DataFrame(np.asarray(text), columns=['qapair', 'title'])
        vectorizer = TfidfVectorizer()
        corpus = df.loc[:, 'title']
        tfidf_mat = vectorizer.fit_transform(corpus).toarray()
        wf=open('ir_data','wb')
        data=[vectorizer,tfidf_mat,df]
        pickle.dump(data,wf)
        return data

    def get_the_topNans(self,n,text):
        question_metrix=self.vectorizer.transform([self.prepocess(text)]).toarray()
        matrix = np.dot(self.tfidf_mat, question_metrix.T)
        pair = []
        for i in range(len(matrix)):
            pair.append((i, matrix[i][0]))
        rec_list_for_user = heapq.nlargest(n, dict(pair).items(), key=lambda tup: tup[1])
        return rec_list_for_user

if __name__ == '__main__':
    model=inforetrival_model()
    res=model.get_the_topNans(5,'how to connect bilibili')
    for each in res:
        temp=model.df.loc[each[0]]
        print(temp.qapair)

