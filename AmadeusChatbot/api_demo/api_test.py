# the dialogflow api in the project
# all the operation related to dialogflow should be there
import dialogflow_v2beta1 as dialogflow
import os
import re


def detect_intent_texts(session_id, texts, language_code='en-US',project_id='amadeus-wsxhty'):
    """Returns the result of detect intent with texts as inputs.

    Using the same `session_id` between requests allows continuation
    of the conversation."""
    path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath('api_test.py'))),
                        'api_demo/amadeus-wsxhty-d827a1efaa20.json')
    print(path)
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = path
    session_client = dialogflow.SessionsClient()

    session = session_client.session_path(project_id, session_id)
    print('Session path: {}\n'.format(session))
    text_input = dialogflow.types.TextInput(
        text=texts, language_code=language_code)

    query_input = dialogflow.types.QueryInput(text=text_input)

    response = session_client.detect_intent(
        session=session, query_input=query_input)

    # 'Query text: {}'.format(response.query_result.query_text)
    # 'Detected intent: {} (confidence: {})\n'.format(
    #     response.query_result.intent.display_name,
    #     response.query_result.intent_detection_confidence)
    # 'Fulfillment text: {}\n'.format(
    #     response.query_result.fulfillment_text)
    return response



def print_res(response):
    print('=' * 20)
    print('Query text: {}'.format(response.query_result.query_text))
    print('Detected intent: {} (confidence: {})\n'.format(
        response.query_result.intent.display_name,
        response.query_result.intent_detection_confidence))
    print('Fulfillment text: {}\n'.format(
        response.query_result.fulfillment_text))

if __name__ == '__main__':
    res=detect_intent_texts('1', 'hi', 'en-US','amadeus-wsxhty')
    print_res(res)
