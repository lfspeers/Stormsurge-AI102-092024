from CLU import *


project_name = 'HomeAutomationAppDemo'
project_file = 'services/CLU/HomeAutomationDemo.json'

# import_location = import_project(project_name, project_file)
# print(import_location)
# import_location = "https://jm-ai102-language.cognitiveservices.azure.com/language/authoring/analyze-conversations/projects/HomeAutomationAppDemo/import/jobs/452c8e0e-eba6-4477-acff-4c80b9f3ae1a_638642016000000000?api-version=2023-04-01"
# check_status(import_location)


training_location = train_model(project_name)
check_status(training_location)