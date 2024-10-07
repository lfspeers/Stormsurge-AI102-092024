from AILanguage import authenticate_client
from azure.ai.textanalytics import TextAnalyticsClient

def detect_language(client, text):
    try:
        documents = []
        documents.append(text)
        response = client.detect_language(documents=documents, country_hint='us')
        return response
    except Exception as e:
        print(f"Encountered exception: {e}.")



if __name__ == "__main__":
    client = authenticate_client()
    text = "Hello! Ce document est rédigé en Français."
    response = detect_language(client, text)
    print(response)