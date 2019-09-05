'''

train our own vector_matrix
and save it as 'data/embedding'

'''

from gensim.models import Word2Vec,KeyedVectors
import pickle



def word2vector():

    words_list = []
    for file_index in range(5):
        with open('data/raw_data_{}'.format(file_index),'rb') as file:
            sentence = pickle.load(file)
        question_sentence = sentence.loc[:,'question']
        answer_sentence = sentence.loc[:,'answer_body']
        # words_list = []
        for index in range(len(question_sentence)):
            words_list.append(question_sentence[index].split(' '))
            words_list.append(answer_sentence[index].split(' '))
    model = Word2Vec(words_list,size= 100,window = 5,min_count =1,max_vocab_size=None)
    model.save('project_embedding.model')

if __name__ == '__main__':
    word2vector()
    model = Word2Vec.load('project_embedding.model')
    model.wv.save('vector.wv')
    wv = KeyedVectors.load('vector.wv',mmap='r')
    print(len(wv.vocab))
    print(wv['python'])