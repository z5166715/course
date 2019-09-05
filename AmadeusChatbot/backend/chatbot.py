# backend code for the chatbot,logic control also in this
# import flask.request as request
from flask import request
import backend.format_change as change
from backend.googlesearch.main import main


from flask import Flask
from flask_restplus import Resource, Api,fields
from api_demo.api_test import detect_intent_texts
from machine_learning.ir_model.model import inforetrival_model
import database.dao as dao
import pytesseract
from PIL import Image
import keras
import tensorflow as tf
from machine_learning.LSTM_model.lstm_model import AttentionWithContext
import os
from machine_learning.LSTM_model.preprocessing import prepocess
from machine_learning.LSTM_model.my_predict_model import required_processing

def after_request(response1):
    response1.headers['Access-Control-Allow-Origin'] = '*'
    response1.headers['Access-Control-Allow-Methods'] = 'PUT,GET,POST,DELETE'
    response1.headers['Access-Control-Allow-Headers'] = 'Content-Type,Authorization'
    return response1

app=Flask(__name__)
app.after_request(after_request)
api = Api(app)
ir_model=inforetrival_model()
db=dao.connectdb()
lstm_model=keras.models.load_model(os.path.dirname(os.path.dirname(os.path.abspath('my_predict_model.py')))+'/machine_learning/LSTM_model/LSTMmodel_alltraintest.h5', custom_objects={'AttentionWithContext': AttentionWithContext})
g = tf.get_default_graph()
context_flag=False
context=''

@api.route('/main/<session_id>/<user_input>')
@api.param('session_id','use for the contex of the dialog')
@api.param('user_input','what the user sent to the server')
class chatbot(Resource):
    def post(self,session_id,user_input):
        # OCR
        if user_input=='tar=1':
            f=request.files['avatar']
            image = Image.open(f)
            code = pytesseract.image_to_string(image)
            user_input=code
        response=detect_intent_texts(session_id,user_input)
        # IRMODEL
        if response.query_result.intent.display_name == 'Default Fallback Intent' :
            global context_flag, context
            if context_flag==False:
                qa_list = []
                top5=ir_model.get_the_topNans(5, user_input)
                if top5[0][1]<0.3:
                    context_flag=True
                    context=user_input
                    return 'I\'m quite confused,plz make your question clearer to me?', 200

                for each in top5:
                    temp = ir_model.df.loc[each[0]]
                    # print(temp.qapair)
                    qa_list.append(temp.qapair)
                raw_ans = dao.query_anser_top(db, qa_list)
                ans_list = [prepocess(i) for i in raw_ans]
                question_matrix, answer_matrix = required_processing(prepocess(user_input), ans_list)
                # support the multi thread of flask in tensorflow
                with g.as_default():
                    probs = lstm_model.predict([question_matrix, answer_matrix], verbose=1)
                print(probs)
                true_prob = []
                for each_prob in probs:
                    true_prob.append(each_prob[1])
                index = true_prob.index(max(true_prob))
                res = raw_ans[index]
                return res, 200
            else:
                # global parameters context_flag, context
                context_flag = False
                context=''
                qa_list = []
                user_input=user_input+context
                top5 = ir_model.get_the_topNans(5, user_input)
                if top5[0][1] < 0.3:

                    # google search
                    search_result = main(user_input)
                    return search_result,200

                for each in top5:
                    temp = ir_model.df.loc[each[0]]
                    qa_list.append(temp.qapair)
                raw_ans = dao.query_anser_top(db, qa_list)
                ans_list = [prepocess(i) for i in raw_ans]
                question_matrix, answer_matrix = required_processing(prepocess(user_input), ans_list)
                with g.as_default():
                    probs = lstm_model.predict([question_matrix, answer_matrix], verbose=1)
                print(probs)
                true_prob = []
                for each_prob in probs:
                    true_prob.append(each_prob[1])
                index = true_prob.index(max(true_prob))
                res = raw_ans[index]
                return res, 200


        elif response.query_result.intent.display_name[0] in ['K','k']:
            # match the question with the question body in dialogflow knowledgebase
            context_flag = False
            context = ''
            ans=response.query_result.knowledge_answers.answers
            temp=str(ans).split('\n')
            return temp[2], 200
            pass
        elif response.query_result.intent.display_name == 'course info':
            # handle course info question
            context_flag = False
            context = ''
            course_name = response.query_result.parameters.fields['course_name'].string_value
            course_number = response.query_result.parameters.fields['course_number'].string_value
            print(type(response.query_result.fulfillment_text))
            print(response.query_result.fulfillment_text)
            if course_name == '' and course_number == '':
                pass
            else:
                list = change.format_change(dao.query_of_user(db,course_name, course_number)[0])
                string = list.tostring()
                return string,200
        return response.query_result.fulfillment_text,200
        # pass


if __name__ == '__main__':
    app.run(debug=True)
