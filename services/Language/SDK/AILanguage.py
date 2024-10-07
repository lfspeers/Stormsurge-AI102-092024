import os
from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential

def authenticate_client():
    key = os.environ['AI_MULTISERVICE_KEY']
    credential = AzureKeyCredential(key)
    endpoint = os.environ['AI_MULTISERVICE_ENDPOINT']

    client = TextAnalyticsClient(
        endpoint=endpoint,
        credential=credential
    )

    return client
