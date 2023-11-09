import requests
from PIL import Image
import os
import time

# URL of the image
url = "http://192.168.123.13:5000/image"

# Directory where you want to save the image
save_directory = "/home/unitree/Desktop/objectDetection/content/yolov7/StreamImages"

# Ensure the save directory exists
os.makedirs(save_directory, exist_ok=True)

def grabImageFromStream():
    try:
        # Send an HTTP GET request to the URL
        response = requests.get(url)

        # Check if the request was successful
        if response.status_code == 200:
            # Check if the response content is not empty
            if response.content:
                # Open the response content as an image
                image = Image.open(requests.get(url, stream=True).raw)

                # Check if the image is valid and not truncated
                if image:
                    # Generate a unique filename (e.g., using the current timestamp)
                    # timestamp = time.strftime("%Y%m%d%H%M%S")
                    filename = "saved_image.png"

                    # Specify the absolute path for saving the image
                    save_path = os.path.join(save_directory, filename)
                    
                    # Save the image
                    image.save(save_path)
                    #print(f"Image saved successfully as {save_path}")
                    return True
                else:
                    print("The image is not valid or is truncated.")
                    return False
            else:
                print("The response content is empty. The image may not be available.")
                return False
        else:
            print(f"Failed to fetch the image. Status code: {response.status_code}")
            return False


    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return False
    except OSError as e:
        print(f"An error occurred while saving the image: {e}")
        return False

    # Continue with the next iteration of the while loop
