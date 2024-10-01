import os
from azure.ai.vision.imageanalysis import ImageAnalysisClient
from azure.ai.vision.imageanalysis.models import VisualFeatures
from azure.core.credentials import AzureKeyCredential
import cv2


def analyze_image(img_path, draw=True, debug=False):
    """Given the file path to an image, calls the Analyze Image API to generate Captions and do OCR.
    Draw will use the coordinates from the reponse to draw rectangles on the image and save it.
    Debug will output the coordinates for the lines and words."""

    # Set the values of your computer vision endpoint and computer vision key
    # as environment variables:
    try:
        base_url = os.environ["AI_MULTISERVICE_ENDPOINT"]
        key = os.environ["AI_MULTISERVICE_KEY"]
    except KeyError:
        print("Missing environment variable 'AI_MULTISERVICE_ENDPOINT' or 'AI_MULTISERVICE_KEY'")
        print("Set them before running this sample.")
        exit()

    # Create an Image Analysis client
    client = ImageAnalysisClient(
        endpoint=base_url,
        credential=AzureKeyCredential(key)
    )

    # Load the image
    with open(img_path, 'rb') as f:
        img = f.read()

    # Get a caption for the image. This will be a synchronously (blocking) call.
    result = client.analyze(
        image_data=img,
        # image_url = "https://learn.microsoft.com/azure/ai-services/computer-vision/media/quickstarts/presentation.png",
        visual_features=[VisualFeatures.CAPTION, VisualFeatures.READ],
        gender_neutral_caption=True,  # Optional (default is False)
    )
    
    if debug:
        print("Image analysis results:")
        # Print caption results to the console
        print(" Caption:")
        if result.caption is not None:
            print(f"   '{result.caption.text}', Confidence {result.caption.confidence:.4f}")

        # Print text (OCR) analysis results to the console
        print(" Read:")
        if result.read is not None:
            for line in result.read.blocks[0].lines:
                print(f"   Line: '{line.text}', Bounding box {line.bounding_polygon}")
                for word in line.words:
                    print(f"     Word: '{word.text}', Bounding polygon {word.bounding_polygon}, Confidence {word.confidence:.4f}")
        

    if draw:
        img = cv2.imread(img_path)
        for line in result.read.blocks[0].lines:
            start_point = (line.bounding_polygon[0]['x'], line.bounding_polygon[0]['y'])
            end_point = (line.bounding_polygon[2]['x'], line.bounding_polygon[2]['y'])
            cv2.rectangle(img, start_point, end_point, color=(255, 0, 0), thickness=2)

        window_name = 'image'
        cv2.imshow(window_name, img)
        cv2.waitKey(0)

        # Save the image with bounding boxes drawn
        outpath = os.path.split(img_path)[0] + '\\analyze_image_presentation_boxes.png'
        cv2.imwrite(outpath, img)
        print(f'Image with Bounding Boxes Saved at: {outpath}')


if __name__ == '__main__':
    # Use a local copy of the image from the quickstart
    path = os.path.dirname(__file__)
    base_path = os.path.split(os.path.split(os.path.split(path)[0])[0])[0]
    file_path = os.path.join(base_path + '\\data\\analyze_image_presentation.png')

    analyze_image(file_path, draw=True, debug=True)
