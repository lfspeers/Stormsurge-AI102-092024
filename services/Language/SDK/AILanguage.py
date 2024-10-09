import os
from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential
import datetime

def authenticate_client():
    key = os.environ['AI_MULTISERVICE_KEY']
    credential = AzureKeyCredential(key)
    endpoint = os.environ['AI_MULTISERVICE_ENDPOINT']

    client = TextAnalyticsClient(
        endpoint=endpoint,
        credential=credential
    )

    return client


def detect_language(text):
    client = authenticate_client()
    try:
        documents = []
        documents.append(text)
        response = client.detect_language(documents=documents, country_hint='us')[0]

        result = {}
        result['id'] = response.id # typically id is your database PK
        result['text'] = text
        result['language'] = response.primary_language.name
        result['language_code'] = response.primary_language.iso6391_name
        result['confidence_score'] = response.primary_language.confidence_score
        result['created_on'] = datetime.datetime.now()
        result['prediction_type'] = "Language Detection"
        result['raw_response'] = str(response)
        return result
    
    except Exception as e:
        print(f"Encountered exception: {e}.")


def analyze_sentiment(text):
    client = authenticate_client()
    documents = [text]
    response = client.analyze_sentiment(documents=documents)[0]

    result = {}
    result['id'] = response.id
    result['text'] = text
    result['sentiment'] = response.sentiment
    result['confidence'] = dict(response.confidence_scores)
    result['created_on'] = datetime.datetime.now()
    result['prediction_type'] = "Sentiment Analysis"
    result['raw_response'] = str(response)
    return result


def extract_key_phrases(text):
    client = authenticate_client()
    documents = [text]
    response = client.extract_key_phrases(documents=documents)[0]

    result = {}
    result['id'] = response.id
    result['text'] = text
    result['key_phrases'] = response.key_phrases
    result['created_on'] = datetime.datetime.now()
    result['prediction_type'] = "Key Phrase Extraction"
    result['raw_response'] = str(response)
    return result



def recognize_pii(text):
    client = authenticate_client()
    documents = [text]
    response = client.recognize_pii_entities(documents=documents)[0]

    result = {}
    result['id'] = response.id
    result['text'] = text
    result['entities'] = [dict(entity) for entity in response.entities]
    result['redacted_text'] = response.redacted_text
    result['created_on'] = datetime.datetime.now()
    result['prediction_type'] = "Recognize PII"
    result['raw_response'] = str(response)
    return result


def analyze_text(text, operations=[]):
    responses = []
    if "Language Detection" in operations:
        response = detect_language(text)
        responses.append(response)
    if "Sentiment Analysis" in operations:
        response = analyze_sentiment(text)
        responses.append(response)
    if "Key Phrase Extraction" in operations:
        response = extract_key_phrases(text)
        responses.append(response)
    if "Recognize PII" in operations:
        response = recognize_pii(text)
        responses.append(response)
   
    return responses
    


if __name__ == "__main__":
    text = "Great food and very friendly staff. We came with our dog and they accommodated us very well out on the patio and brought him his own water bowl too. The food we had was all great. It's neat to have a place so close where we can get to try handmade authentic foods from across the ocean."
    response = analyze_sentiment(text)
    print(response)

    # Database Table - ML Predictions
    # |id|table|column|operation_name|result|raw_response|

    # Prediction on a Customer Review
    # |X|CustomerReviews|ReviewText|"Language Detection"|
    # |X|CustomerReviews|ReviewText|"Sentiment Analysis"|result|response





    # Audit/History of AI Insights

    """
    Use Case

    Online Retailer
    500 reviews/day posted online
        reviews from google, yelp, etc...
    
    Queue of all reviews
    Write a script to process each review at the front of the queue
    Store the results in a database table/file
        Strategies
            AI Insights - All Predictions table
            Reviews Table -> Review Predictions Table
        Storing the predictions/response
            Parse the fields out that you need
            Store the entire SDK/API response
    """
