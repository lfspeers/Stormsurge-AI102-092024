import requests, json, os, uuid

base_url = "https://api.cognitive.microsofttranslator.com"
endpoint = '/transliterate'
url = base_url + endpoint
api_version = '3.0'

region = os.environ['AI_MULTISERVICE_REGION']
key = os.environ['AI_MULTISERVICE_KEY']


headers = {
    'Ocp-Apim-Subscription-Key': key,
    'Ocp-Apim-Subscription-Region': region,
    'Content-Type': 'application/json',
    'X-ClientTraceId': str(uuid.uuid4())
}

params = {
    'api-version': api_version,
    'language': 'ja',
    'fromScript': 'Jpan',
    'toScript': "Latn"
    }


body = [
    {"Text":"こんにちは"},
    {"Text":"さようなら"}
]


response = requests.post(url=url, headers=headers, params=params, json=body)
print(response.json())