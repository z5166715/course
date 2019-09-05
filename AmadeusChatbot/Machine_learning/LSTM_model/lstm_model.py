import pickle
import numpy as np
import pandas as pd
import keras
from keras import backend as K
from keras.models import Model, load_model
from keras import initializers
from keras import regularizers, constraints
import random
from keras.callbacks import TensorBoard
from keras.layers import Dense, Bidirectional, Activation, Input, LSTM, GRU, Multiply, dot, concatenate
from keras.engine.topology import Layer
from keras.utils.generic_utils import transpose_shape
from keras.optimizers import Adam


class AttentionWithContext(Layer):
    """
        Attention operation, with a context/query vector, for temporal data.
        Supports Masking.
        Follows the work of Yang et al. [https://www.cs.cmu.edu/~diyiy/docs/naacl16.pdf]
        "Hierarchical Attention Networks for Document Classification"
        by using a context vector to assist the attention
        # Input shape
            3D tensor with shape: `(samples, steps, features)`.
        # Output shape
            2D tensor with shape: `(samples, features)`.
        :param kwargs:
        Just put it on top of an RNN Layer (GRU/LSTM/SimpleRNN) with return_sequences=True.
        The dimensions are inferred based on the output shape of the RNN.
        Example:
            model.add(LSTM(64, return_sequences=True))
            model.add(AttentionWithContext())
        """

    def __init__(self, init='glorot_uniform', kernel_regularizer=None, bias_regularizer=None, kernel_constraint=None,
                 bias_constraint=None, **kwargs):
        self.supports_masking = True
        self.init = initializers.get(init)
        self.kernel_initializer = initializers.get('glorot_uniform')

        self.kernel_regularizer = regularizers.get(kernel_regularizer)
        self.bias_regularizer = regularizers.get(bias_regularizer)

        self.kernel_constraint = constraints.get(kernel_constraint)
        self.bias_constraint = constraints.get(bias_constraint)

        super(AttentionWithContext, self).__init__(**kwargs)

    def build(self, input_shape):
        self.kernel = self.add_weight((input_shape[-1], 1),
                                      initializer=self.kernel_initializer,
                                      name='{}_W'.format(self.name),
                                      regularizer=self.kernel_regularizer,
                                      constraint=self.kernel_constraint)
        self.b = self.add_weight((input_shape[1],),
                                 initializer='zero',
                                 name='{}_b'.format(self.name),
                                 regularizer=self.bias_regularizer,
                                 constraint=self.bias_constraint)

        self.u = self.add_weight((input_shape[1],),
                                 initializer=self.kernel_initializer,
                                 name='{}_u'.format(self.name),
                                 regularizer=self.kernel_regularizer,
                                 constraint=self.kernel_constraint)
        self.built = True

    def compute_mask(self, input, mask):
        return None

    def call(self, x, mask=None):
        # (x, 40, 300) x (300, 1)
        multData = K.dot(x, self.kernel)  # (x, 40, 1)
        multData = K.squeeze(multData, -1)  # (x, 40)
        multData = multData + self.b  # (x, 40) + (40,)

        multData = K.tanh(multData)  # (x, 40)

        multData = multData * self.u  # (x, 40) * (40, 1) => (x, 1)
        multData = K.exp(multData)  # (X, 1)

        # apply mask after the exp. will be re-normalized next
        if mask is not None:
            mask = K.cast(mask, K.floatx())  # (x, 40)
            multData = mask * multData  # (x, 40) * (x, 40, )

        # in some cases especially in the early stages of training the sum may be almost zero
        # and this results in NaN's. A workaround is to add a very small positive number ε to the sum.
        # a /= K.cast(K.sum(a, axis=1, keepdims=True), K.floatx())
        multData /= K.cast(K.sum(multData, axis=1, keepdims=True) + K.epsilon(), K.floatx())
        multData = K.expand_dims(multData)
        weighted_input = x * multData
        return K.sum(weighted_input, axis=1)

    def compute_output_shape(self, input_shape):
        return (input_shape[0], input_shape[-1],)


'''
LSTM_model is a Bidirectional LSTM model with attention layer 
input two vectors question(50,100) answer(100,120),
finally do the dense layer and output an binary classification

'''


def LSTMmodel():
    def dot_funxtion(x):
        return K.batch_dot(x[0], x[1])

    question_input = Input(shape=(50, 100))
    answer_input = Input(shape=(100, 120))

    # M = K.transpose(K.random_normal_variable(shape=(100, 100),dtype=float, mean=0, scale=1))
    # pred_response = keras.layers.Lambda(dot_T_functino,arguments={'M':M})(question_input)
    # print(pred_response.shape)
    # dot_embedding = concatenate([question_input,answer_input], axis=1)
    dot_embedding = keras.layers.Lambda(dot_funxtion)([question_input, answer_input])
    print(dot_embedding)
    x = Bidirectional(LSTM(16, return_sequences=True, dropout=0.1))(dot_embedding)
    print(x.shape)
    x = AttentionWithContext()(x)
    x = Dense(2, activation='softmax')(x)
    model = Model(inputs=[question_input, answer_input], outputs=x)
    adam = Adam(lr=0.01)
    model.compile(optimizer=adam, loss='categorical_crossentropy', metrics=['accuracy'])

    return model


if __name__ == '__main__':
    ''' 
    due to the memory of computer,we using the split file to train and test data,
    the train data using the unbalance data,set the class_weight as 1:3
    '''
    class_weight = {0: 3.,
                    1: 1.}
    model = LSTMmodel()
    for epoch in range(1000):
        for file_index in range(5):
            tarin = open('data/ks_train{}'.format(file_index), 'rb')
            ks_train = pickle.load(tarin)
            question_sequence = ks_train[0]
            answer_sequence = ks_train[1]
            target = keras.utils.to_categorical(ks_train[2], 2)
            print('=' * 50 + 'epoch: {}'.format(epoch) + '    ' + 'file-{}'.format(file_index))
            history_ft = model.fit([question_sequence, answer_sequence], target,
                                   epochs=1,
                                   batch_size=1000,
                                   verbose=1,
                                   class_weight=class_weight
                                   )

    model.save('LSTMmodel_alltraintest.h5')

    '''due to the memory of computer,we using the split file to train and test data'''

    model = load_model('LSTMmodel_alltraintest.h5', custom_objects={'AttentionWithContext': AttentionWithContext})

    for file_index in range(5):
        print('=' * 50 + 'test_file: {}'.format(file_index))
        test = open('data/ks_test{}'.format(file_index), 'rb')
        ks_test = pickle.load(test)
        test_question_sequence = ks_test[0]
        test_answer_sequence = ks_test[1]
        test_target = keras.utils.to_categorical(ks_test[2], 2)
        value = model.evaluate([test_question_sequence, test_answer_sequence], test_target)
        print(value)



