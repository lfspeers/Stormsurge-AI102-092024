import requests, json, os, time

key = os.environ['AI_LANGUAGE_KEY']
base_url = os.environ['AI_LANGUAGE_ENDPOINT']
project_name = 'LoanAgreement'
API_VERSION = '2022-05-01'


# Steps
# Import the data (with labels)
# Train the model
# Deploy the model
# Make predicitons



def import_customner():

    endpoint = f"{base_url}language/authoring/analyze-text/projects/{project_name}/:import?api-version={API_VERSION}"

    headers = {
        'Content-Type': 'application/json',
        'Ocp-Apim-Subscription-Key': key
    }

    # Read the project file
    label_file = 'data/NER/CustomNER - LoanAgreements/LoanAgreements/loanAgreementsLabels.json'
    with open(label_file) as f:
        data = json.load(f)
    
    try:
        response = requests.post(url=endpoint, headers=headers, json=data)
        operation_location = response.headers['operation-location']
    except Exception as e:
        print(e)
    
    return operation_location


def check_status(operation_location, timeout=60):
    headers = {'Ocp-Apim-Subscription-Key': key}
    response = requests.get(url=operation_location, headers=headers)
    print(response.json()['status'])


def train_model(model_name):
    endpoint = f"{base_url}language/authoring/analyze-text/projects/{project_name}/:train"
    headers = {
        'Content-Type': 'application/json',
        'Ocp-Apim-Subscription-Key': key
    }
    params = {'api-version': API_VERSION}
    body = {
        "modelLabel": model_name,
        "trainingConfigVersion": "2022-05-01",
        "evaluationOptions": {
            "kind": "percentage",
            "trainingSplitPercentage": 80,
            "testingSplitPercentage": 20
        }
    }

    response = requests.post(url=endpoint, headers=headers, params=params, json=body)
    print(response.text)
    training_location = response.headers['operation-location']
    print(response.headers['operation-location'])
    return training_location


def check_training_status(training_location):
    endpoint = f"{base_url}/language/authoring/analyze-text/projects/{project_name}/train/jobs/{training_location}?api-version=2022-05-01"
    headers = {'Ocp-Apim-Subscription-Key': key}
    response = requests.get(url=endpoint, headers=headers)
    r = response.json()
    print(r['result']['trainingStatus'])
    return r['result']['trainingStatus']


def deploy_model(deployment_name, model_name):
    endpoint = f"{base_url}language/authoring/analyze-text/projects/{project_name}/deployments/{deployment_name}?api-version=2022-05-01"
    headers = {'Ocp-Apim-Subscription-Key': key, 'Content-Type': 'application/json'}
    body = {'trainedModelLabel': model_name}

    response = requests.put(url=endpoint, headers=headers, json=body)

    if 'operation-location' in response.headers:
        return response.headers['operation-location']
    else:
        return None


def extract_custom_entities(text, project_name, deployment_name):
    endpoint = f"{base_url}/language/analyze-text/jobs?api-version={API_VERSION}"
    headers = {'Ocp-Apim-Subscription-Key': key, 'Content-Type': 'application/json'}
    

    body = {
        "displayName": "Extracting Loan Entities",
        "analysisInput": {
            "documents": [
            {
                "id": "1", # Use your database PK if you have one
                "language": "en",
                "text": text
            }
            ]
        },
        "tasks": [
            {
            "kind": "CustomEntityRecognition",
            "taskName": "Entity Recognition",
            "parameters": {
                "projectName": project_name,
                "deploymentName": deployment_name
            }
            }
        ]
        }
    response = requests.post(url=endpoint, headers=headers, json=body)

    return response.headers['operation-location']


def get_customner_results(operation_location):
    headers = {'Ocp-Apim-Subscription-Key': key}
    response = requests.get(url=operation_location, headers=headers)
    r = response.json()
    return r


if __name__ == '__main__':
    # import_location = import_customner()
    # print(import_location)
    # import_location = "https://jm-ai102-language.cognitiveservices.azure.com/language/authoring/analyze-text/projects/LoanAgreement/import/jobs/bd38d061-064e-43b5-a239-e3e28105c994_638644608000000000?api-version=2022-05-01"
    # check_status(import_location)

    model_name = "LoanAgreementModel"
    # training_location = train_model(model_name)
    # training_location = "56440e5b-1da9-420f-b3b9-5a4d3a48d73f_638644608000000000"
    # check_training_status(training_location)

    deployment_name= 'LoanAgreementModelV1'
    # deployment_location = deploy_model(model_name=model_name, deployment_name=deployment_name)
    
    deployment_location = "https://jm-ai102-language.cognitiveservices.azure.com/language/authoring/analyze-text/projects/LoanAgreement/deployments/LoanAgreementModelV1/jobs/41e0fc1b-60d5-47b6-a292-1579bbab33cd_638644608000000000?api-version=2022-05-01"
    # check_status(deployment_location)


    with open("data/NER/CustomNER - LoanAgreements/LoanAgreements/Test 3.txt") as f:
        text = f.read()
    
    # operation_location = extract_custom_entities(text=text, project_name=project_name, deployment_name=deployment_name)
    # print(operation_location)
    operation_location = "https://jm-ai102-language.cognitiveservices.azure.com/language/analyze-text/jobs/e4dd7065-4d8c-44fc-8735-385afb454e8b?api-version=2022-05-01"
    check_status(operation_location)

    results = get_customner_results(operation_location)
    print(results)