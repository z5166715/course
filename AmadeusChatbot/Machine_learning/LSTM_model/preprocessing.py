import pickle
import numpy as np
import pandas as pd
import nltk
import string
import pymysql
import keras
import re
from gensim.models import Word2Vec, KeyedVectors

EACH_FILE_SIZE = 2000  # set the total number of data,pull from the database
TRAIN_SIZE = int(EACH_FILE_SIZE)


def connectdb():
    print('连接到mysql服务器...')
    # 打开数据库连接
    # 用户名:root, 密码:zh123123
    db = pymysql.connect("127.0.0.1", "root", "666666",
                         "comp9900")  # my local database,should change to aws online database
    print('连接上了!')
    return db


def query_all_qabody(db):
    cursor = db.cursor()
    sql = "select question_title,question_body,answer_body from questionAndanswer"
    try:
        cursor.execute(sql)
        result = cursor.fetchall()
        db.close()

        pass
    except:
        print('crash on query_all_qabody')

    return result


def prepocess(text):
    def tokenize(text):
        lowers = text.lower()
        # remove_code = re.sub('<code>.*</code>','',lowers)
        remove_tag = re.sub('</p>|</li>|<p>|<li>|</ol>|<ol>|<pre>|</pre>|<code>|</code>|<ul>|</ul>|&gt|&lt|<hr>|</hr>'
                            '|<h[0-9]*]>|</h[0-9]*]>', '', lowers)
        remove_punctuation_map = dict((ord(char), ' ') for char in string.punctuation)
        no_punctuation = remove_tag.translate(remove_punctuation_map)
        # print(no_punctuation)
        return nltk.word_tokenize(no_punctuation)

    return ' '.join(tokenize(text))


'''
train_data size is 0.8 * total_size
train_csv_data function return a pandas dataframe 'train.csv':

'question' 'answer_body' 'label'
    ...         ...        ...  
    ...         ...        ...   

    question is (title + question)
    (question answer) is mixed with wrong answer.if input size is (100,3) , output size is (400,3)
'''


def train_csv_data(raw_data, data_index):
    question_list = np.array(raw_data.loc[:, 'question'][:TRAIN_SIZE])
    answer_list = np.array(raw_data.loc[:, 'answer_body'])
    wrong_match = []
    # np.random.seed(5)
    for que_index in range(len(question_list)):
        # if que_index<len(question_list):
        answer = np.random.choice(np.hstack((answer_list[:que_index], answer_list[que_index + 1:])), 3)
        # else:
        # answer = np.random.choice(answer_list[:que_index],3)
        wrong_match.append([question_list[que_index], answer[0], 0])
        wrong_match.append([question_list[que_index], answer[1], 0])
        wrong_match.append([question_list[que_index], answer[2], 0])
        # wrong_match.append([question_list[que_index], answer[3], 0])
    df = pd.DataFrame(wrong_match, columns=['question', 'answer_body', 'label'])
    df.index = [x for x in range(TRAIN_SIZE, TRAIN_SIZE * 4)]
    new_df = pd.concat([raw_data[:TRAIN_SIZE], df], axis=0)
    new_df = new_df.sample(frac=1).reset_index(drop=True)
    print(new_df)
    new_df.to_csv('data/train{}.csv'.format(data_index))
    pass


'''
test_data size is 0.2 * total_size
test_csv_data function return a pandas dataframe 'test.csv' with distractor0 as right answer:

'question' 'distractor0' 'distractor1' 'distractor2' 'distractor3' 'distractor4' 'distractor5'
    ...         ...           ...           ...           ...           ...           ...
    ...         ...           ...           ...           ...           ...           ...

    question is (title + question)
'''


def test_csv_data(raw_data, index):  # 正确答案为anser【0】
    question_list = np.array(raw_data.loc[:, 'question'][1600:])
    answer_list = np.array(raw_data.loc[:, 'answer_body'])
    wrong_match = []
    # np.random.seed(5)
    for que_index in range(len(question_list)):
        # if que_index<len(question_list):
        answer = np.random.choice(np.hstack((answer_list[:1600 + que_index], answer_list[que_index + 1601:])), 5)
        # else:
        #     answer = np.random.choice(answer_list[:que_index],5)
        answer = np.append(answer, answer_list[1600 + que_index])
        # random.shuffle(answer)
        wrong_match.append([question_list[que_index], answer[5], answer[1], answer[2], answer[3], answer[4], answer[0]])
    df = pd.DataFrame(wrong_match,
                      columns=['question', 'distractor0', 'distractor1', 'distractor2', 'distractor3', 'distractor4',
                               'distractor5'])
    print(df)
    df.to_csv('data/test{}.csv'.format(index))
    pass


'''
data_processing() function return 3 dimension 'raw_data':


question(title + question_body)    answer_body    label
   ......                              ...          ...
   ......                              ...          ...


'''


def data_processing():
    db = connectdb()
    cursor = db.cursor()
    sql = "select question_title,question_body,answer_body from questionAndanswer"
    cursor.execute(sql)

    datalist = []
    file_index = 0
    for i in range(10000):
        each = []
        result = cursor.fetchone()
        each.append(prepocess(result[0]))
        each.append(prepocess(result[1]))
        each.append(prepocess(result[2]))
        datalist.append(each)
        if (i + 1) % 2000 == 0:
            print(file_index)
            text = np.asarray(datalist)
            df = pd.DataFrame(text, columns=['title', 'question_body', 'answer_body'])
            df['label'] = 1
            # newdf = df.loc[:,['title','question_body']]
            # newdf['question'] = newdf.apply(lambda x:x[0] + ' ' + x[1], axis=1)
            # right_df = pd.concat([newdf.loc[:,'question'],df.loc[:,['answer_body','label']]],axis=1)
            right_df = df.loc[:, ['title', 'answer_body', 'label']]
            # print(right_df)
            right_df.columns = ['question', 'answer_body', 'label']
            print(right_df)
            with open('data/raw_data_{}'.format(file_index), 'wb') as file:
                pickle.dump(right_df, file)

            file_index += 1
            datalist = []
            pass
    db.close()


'''
save 4 parts of train data as pickle(sequence means each different word embedding as a number in a 200size list)

vocab   : all unique words
question_sequence : [12,15,76,30.........,0,0] 200size list save question words(not fullfill should pad with 0)
distractor0  :[13,53,44,66..........,0,0] 200size list save answer words (distractor0 is right answer)
distractor1  :[23,63,4244,46..........,0,0] 200size list save answer words
distractor2  :[313,43,44,646..........,0,0] 200size list save answer words
distractor3  :[43,553,424,636..........,0,0] 200size list save answer words
distractor4  :[263,1113,444,616..........,0,0] 200size list save answer words
distractor5  :[333,223,44,66..........,0,0] 200size list save answer words

this is used to test model

'''


def cal_matrix_test(file_index):
    f = open('data/embedding', 'rb')
    embedding = pickle.load(f)
    # file_index = 4
    file = pd.read_csv('data/test{}.csv'.format(file_index), index_col=0)

    question_matrix = []
    answer_matrix = []
    target = []
    embedding_matrix = embedding[1]

    for index in range(0, len(file)):
        each_question = file.iloc[index, 0]
        each_answer0 = file.iloc[index, 1]
        each_answer1 = file.iloc[index, 2]
        each_answer2 = file.iloc[index, 3]
        each_answer3 = file.iloc[index, 4]
        each_answer4 = file.iloc[index, 5]
        each_answer5 = file.iloc[index, 6]
        question_words1 = get_word_matrix(each_question, embedding_matrix, 50)
        answer_words0 = get_word_matrix(each_answer0, embedding_matrix, 120)
        answer_words1 = get_word_matrix(each_answer1, embedding_matrix, 120)
        answer_words2 = get_word_matrix(each_answer2, embedding_matrix, 120)
        answer_words3 = get_word_matrix(each_answer3, embedding_matrix, 120)
        answer_words4 = get_word_matrix(each_answer4, embedding_matrix, 120)
        answer_words5 = get_word_matrix(each_answer5, embedding_matrix, 120)
        for i in range(6):
            question_matrix.append(question_words1)
        answer_matrix.append(answer_words0)
        target.append(1)
        answer_matrix.append(answer_words1)
        target.append(0)
        answer_matrix.append(answer_words2)
        target.append(0)
        answer_matrix.append(answer_words3)
        target.append(0)
        answer_matrix.append(answer_words4)
        target.append(0)
        answer_matrix.append(answer_words5)
        target.append(0)

    print(np.asarray(answer_matrix).shape)

    wf = open('data/ks_test{}'.format(file_index), 'wb')

    ks_model = [np.asarray(question_matrix), np.transpose(np.asarray(answer_matrix), axes=(0, 2, 1)), target]
    pickle.dump(ks_model, wf)

    return ks_model


'''
make a sentence as a matrix
'''


def get_word_matrix(string, embedding, rope):
    word_list = string.split(' ')
    centence_matrix = []
    padding = rope - len(word_list)
    if padding >= 0:
        for word in word_list:
            try:
                centence_matrix.append(embedding[word])
            except:
                centence_matrix.append(embedding['zero'])
        for zero in range(padding):
            centence_matrix.append(embedding['zero'])
    else:
        for index in range(rope):
            try:
                centence_matrix.append(embedding[word_list[index]])
            except:
                centence_matrix.append(embedding['zero'])
    return np.asarray(centence_matrix)


'''
save 4 parts of train data as pickle(sequence means each different word embedding as a number in a 200size list)

vocab   : all unique words
question_sequence : [12,15,76,30.........,0,0] 200size list save question words(if not fullfill should pad with 0)
answer_sequence  :[23,53,44,66..........,0,0] 3 200size lists save answer words(1 right 2 wrong)
target : show the question and answer pair is right or wrong


'''


def cal_matrix_train(file_index):
    f = open('data/embedding', 'rb')
    embedding = pickle.load(f)
    file = pd.read_csv('data/train{}.csv'.format(file_index), index_col=0)
    # print(file)

    vocab = embedding[0]
    question_matrix = []
    answer_matrix = []
    embedding_matrix = embedding[1]
    # question_words = get_word_matrix(file.iloc[0,0], embedding_matrix)
    # answer_words = get_word_matrix(file.iloc[0,1], embedding_matrix)
    for index in range(0, len(file)):
        each_question = file.iloc[index, 0]
        each_answer = file.iloc[index, 1]
        question_words1 = get_word_matrix(each_question, embedding_matrix, 50)
        answer_words1 = get_word_matrix(each_answer, embedding_matrix, 120)
        question_matrix.append(question_words1)
        answer_matrix.append(answer_words1)
        # break
    print(np.asarray(question_matrix).shape)

    target = file['label']

    with open('data/ks_train{}'.format(file_index), 'wb') as wf:
        ks_model = [np.asarray(question_matrix), np.transpose(np.asarray(answer_matrix), axes=(0, 2, 1)), target]
        pickle.dump(ks_model, wf)


'''
create a new embedding matrix from the vetors_matrix that we trained (check 'zero' vector ,and unknown vector)
'''


def create_embedding_metrix():
    embeddings_index = KeyedVectors.load('vector.wv', mmap='r')

    with open('data/raw_data_0', 'rb') as f:
        text = pickle.load(f)
    for index in range(1, 5):
        with open('data/raw_data_{}'.format(index), 'rb') as rawfile:
            text1 = pickle.load(rawfile)
            text = pd.concat([text, text1], axis=0, ignore_index=True)
            print(text.shape)

    string = text.apply(lambda x: x[0] + ' ' + x[1], axis=1)
    ks = keras.preprocessing.text.Tokenizer(lower=True, split=" ")
    ks.fit_on_texts(string)
    vocab = list(ks.word_docs.keys())

    account = 0

    for i in vocab:
        try:
            embeddings_index[i]
        except:
            # print(i)
            embeddings_index[i] = np.random.normal(loc=0.0, scale=1.0, size=100)
            account += 1

    embeddings_index['zero'] = np.asarray([0.0 for x in range(100)], dtype='float32')

    print(len(vocab))
    print(account)

    file = open('data/embedding', 'wb')
    embeddings = [vocab, embeddings_index]
    pickle.dump(embeddings, file)


if __name__ == '__main__':
    data_processing()
    for index in range(5):
        f = open('data/raw_data_{}'.format(index), 'rb')
        raw_data = pickle.load(f)
        train_csv_data(raw_data,index)
        test_csv_data(raw_data,index)
    create_embedding_metrix()
    for i in range(5):
        cal_matrix_train(i)
        cal_matrix_test(i)



