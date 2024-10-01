import requests
import json
import os

base_url = os.environ['AI_MULTISERVICE_ENDPOINT']
endpoint = 'computervision/imageanalysis:analyze?api-version=2023-04-01-preview'
url = base_url + endpoint
key = os.environ['AI_MULTISERVICE_KEY']

headers = {
    'Ocp-Apim-Subscription-Key': key,
    'Content-Type': 'image/jpeg' # MIME Type
}

params = {
    'features': 'caption',
    'language': 'en'
}

# Retrieve the image contents
path = os.path.dirname(__file__)
base_path = os.path.split(os.path.split(os.path.split(path)[0])[0])[0]
file_path = os.path.join(base_path + '\\data\\violent_image.jpg')

with open(file_path, 'rb') as f:
    image = f.read()

try:
    response = requests.post(url, headers=headers, params=params, data=image)
    data = response.json()
    print(json.dumps(data, indent=2))
except Exception as e:
    print(e)
