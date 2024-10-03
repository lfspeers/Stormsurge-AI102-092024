from azure.cognitiveservices.vision.customvision.training import CustomVisionTrainingClient
from azure.cognitiveservices.vision.customvision.prediction import CustomVisionPredictionClient
from azure.cognitiveservices.vision.customvision.training.models import ImageFileCreateBatch, ImageFileCreateEntry, Region
from msrest.authentication import ApiKeyCredentials
import os, time, uuid, datetime


key = os.environ['AI_MULTISERVICE_KEY']
base_url = os.environ['AI_MULTISERVICE_ENDPOINT']
prediction_id = os.environ['CUSTOMVISION_PREDICTION_ID']

credentials = ApiKeyCredentials(in_headers={"Training-key": key})
training_client = CustomVisionTrainingClient(base_url, credentials)
prediction_credentials = ApiKeyCredentials(in_headers={"Prediction-key": key})
prediction_client = CustomVisionPredictionClient(base_url, prediction_credentials)


# Create the project
print("Creating project...")
project_name = 'Lee Tree Classifier' # uuid.uuid4()
project = training_client.create_project(project_name)


# Create our two tags: Hemlock and Japenese Cherry
hemlock_tag = training_client.create_tag(project.id, "Hemlock")
cherry_tag = training_client.create_tag(project.id, "Japenese Cherry")

base_image_location = os.path.join(os.path.dirname(__file__), "Images")

print("Adding images...")

# Create a list of file paths to the images
image_list = []

for image_num in range(1, 11):
    file_name = "hemlock_{}.jpg".format(image_num)
    with open(os.path.join (base_image_location, "Hemlock", file_name), "rb") as image_contents:
        image_list.append(ImageFileCreateEntry(name=file_name, contents=image_contents.read(), tag_ids=[hemlock_tag.id]))

for image_num in range(1, 11):
    file_name = "japanese_cherry_{}.jpg".format(image_num)
    with open(os.path.join (base_image_location, "Japanese_Cherry", file_name), "rb") as image_contents:
        image_list.append(ImageFileCreateEntry(name=file_name, contents=image_contents.read(), tag_ids=[cherry_tag.id]))


# Upload the images
upload_result = training_client.create_images_from_files(project.id, ImageFileCreateBatch(images=image_list))
if not upload_result.is_batch_successful:
    print("Image batch upload failed.")
    for image in upload_result.images:
        print("Image status: ", image.status)
    exit(-1)


# Train the model
print("Training...")
iteration = training_client.train_project(project.id)
while (iteration.status != "Completed"):
    iteration = training_client.get_iteration(project.id, iteration.id)
    print ("Training status: " + iteration.status)
    print ("Waiting 10 seconds...")
    time.sleep(10)


# Publish the model/iteration
iteration_name = "TreeClassifierv1"
result = training_client.publish_iteration(project.id, iteration.id, iteration_name, prediction_id)
print("Done!")


# Make a prediction on a new image 
with open(os.path.join (base_image_location, "Test/test_image.jpg"), "rb") as image_contents:
    print(project.id, iteration_name)
    results = prediction_client.classify_image(project.id, iteration_name, image_contents.read())

    # Display the results.
    for prediction in results.predictions:
        print("\t" + prediction.tag_name +
              ": {0:.2f}%".format(prediction.probability * 100))

with open('published_model.txt', 'w') as f:
    f.write(f"{project.id}, {iteration.id}, {iteration_name}, {datetime.datetime.now()}")
