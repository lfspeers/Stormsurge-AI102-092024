import requests, json, os, uuid

base_url = "https://api.cognitive.microsofttranslator.com"
endpoint = '/translate'
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
    'from': 'en',
    'to': ['fr', 'es', 'zh'],
    'profanityAction': 'Marked',
    'profanityMarker': 'Tag',
    'includeSentenceLength': True
}


body = [
    {'text': 'I would really like to drive your car around the fucking block a few times!'}
]

response = requests.post(url=url, headers=headers, params=params, json=body)
print(response.json())