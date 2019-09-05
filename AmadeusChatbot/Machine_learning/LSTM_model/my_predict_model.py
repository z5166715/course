
from machine_learning.LSTM_model.preprocessing import get_word_matrix
from machine_learning.LSTM_model.lstm_model import AttentionWithContext
from keras.models import Model,load_model
import pickle
import numpy as np
import os


def required_processing(question, answers):  # question数量为1 ，answers是top5 的list
    path = os.path.dirname(
        os.path.dirname(os.path.abspath('my_predict_model.py'))) + '/machine_learning/LSTM_model/data/embedding'

    f = open(path, 'rb')
    embedding = pickle.load(f)
    embedding_matrix = embedding[1]
    question_matrix = []
    answer_matrix = []
    for i in range(len(answers)):
        question_matrix.append(get_word_matrix(question, embedding_matrix, 50))
    for each_answer in answers:
        answer_matrix.append(get_word_matrix(each_answer, embedding_matrix, 120))

    # 返回值为 question_matrix 和 answer_matrix的转置
    return np.asarray(question_matrix), np.transpose(np.asarray(answer_matrix), axes=(0, 2, 1))

    # 传入参数 user的question数量为1， IR model给出的top5 answers数量为5
def run_predict(question,answers):
    question_matrix,answer_matrix = required_processing(question, answers)
    model = load_model(os.path.dirname(os.path.dirname(os.path.abspath('my_predict_model.py')))+'/machine_learning/LSTM_model/LSTMmodel_alltraintest.h5', custom_objects={'AttentionWithContext': AttentionWithContext})
    probs = model.predict([question_matrix,answer_matrix],verbose=1)
    print(probs)
    true_prob = []
    for each_prob in probs:
        true_prob.append(each_prob[1])
    max_index_answer = true_prob.index(max(true_prob))
    the_best = answers[max_index_answer]
    print('the best answer is: the {}\n{}'.format(max_index_answer,the_best))
    return max_index_answer

if __name__ == '__main__':
    pass