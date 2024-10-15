import requests, json, os, time

key = os.environ['AI_LANGUAGE_KEY']
base_url = os.environ['AI_LANGUAGE_ENDPOINT']


def import_project(project_name, project_file):
    url = f"{base_url}/language/authoring/analyze-conversations/projects/{project_name}/:import"

    headers = {
        'Ocp-Apim-Subscription-Key': key,
        'Content-Type': 'application/json'
    }
    params = {'api-version': '2023-04-01'}

    
    with open(project_file) as f:
        body = json.load(f)

    r = requests.post(url=url, headers=headers, params=params, json=body)
    print(r)
    operation_location = r.headers['operation-location']
    print(operation_location)

    return operation_location


def check_status(operation_location, timeout=120):
    headers = {'Ocp-Apim-Subscription-Key': key}

    start_time = time.time()

    while True:
        response = requests.get(url=operation_location, headers=headers)
        r = response.json()

        if r['status'] == 'succeeded':
            print("Completed")
            break
        
        print(f"Status: {r['status']}")

        current_time = time.time()
        if current_time - start_time >= timeout:
            print('Maximum timeout reached. Exiting...')
            break

        print(f"Checking again in 10 seconds...")
        time.sleep(10)



def train_model(project_name):
    url = f"{base_url}/language/authoring/analyze-conversations/projects/{project_name}/:train"
    headers = {
        'Ocp-Apim-Subscription-Key': key,
        'Content-Type': 'application/json'
    }
    params = {'api-version': '2022-05-01'}
    
    body = {
        'modelLabel': 'HomeAutomationModel',
        'trainingMode': 'standard',
        'evaluationOptions': {
            'kind': 'percentage',
            'testingSplitPercentage': 20,
            'trainingSplitPercentage': 80
        }
    }

    r = requests.post(url=url, headers=headers, params=params, json=body)

    if r.status_code == 202:
        print(r.headers['operation-location'])
        return r.headers['operation-location']
    else:
        print(r)


def deploy_model(project_name, deployment_name):
    url = f"{base_url}/language/authoring/analyze-conversations/projects/{project_name}/deployments/{deployment_name}"
    headers = {
        'Ocp-Apim-Subscription-Key': key,
        'Content-Type': 'application/json'
    }
    params = {'api-version': '2022-05-01'}

    body = {'trainedModelLabel': 'HomeAutomationModel'}

    r = requests.put(url=url, headers=headers, params=params, json=body)

    if r.status_code == 202:
        return r.headers['operation-location']
    else:
        print(r)


def query_model(text):
    """Reads the CLUDemoInfo.json file for the project and deployment, and then passes the text to the inference endpoint."""
    url = f"{base_url}/language/:analyze-conversations"
    headers = {
        'Ocp-Apim-Subscription-Key': key,
        'Content-Type': 'application/json'
        }      
    params = {'api-version': '2022-05-01'}

    with open("code/Language/API/CLU/CLUDemoInfo.json") as f:
        info = json.load(f)

    body = {
        "kind": "Conversation",
        "analysisInput": {
            "conversationItem": {
                "id": "1",
                "participantId": "1",
                "text": text
            }
        },
        "parameters": {
            "projectName": info['project_name'],
            "deploymentName": info['deployment_name'],
            "stringIndexType": "TextElement_V8"
        }
    }

    response = requests.post(url=url, headers=headers, params=params, json=body)
    r = response.json()

    intent = r['result']['prediction']['intents'][0]
    entities = r['result']['prediction']['entities']

    return intent, entities


def delete_project():
    with open('code/Language/API/CLU/CLUDemoInfo.json') as f:
        project_name = json.load(f)['project_name']

    url = f"{base_url}/language/authoring/analyze-conversations/projects/{project_name}"
    headers = {'Ocp-Apim-Subscription-Key': key}
    params = {'api-version': '2022-05-01'}

    r = requests.delete(url=url, headers=headers, params=params)

    if r.status_code == 202:
        print(f"Project {project_name} was successfully deleted.")
    else:
        print(r.status_code)



