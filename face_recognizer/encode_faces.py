from pathlib import Path
import face_recognition

from collections import Counter
from PIL import Image, ImageDraw
import pickle

DEFAULT_ENCODINGS_PATH = Path("output/encodings.pkl")



import cv2
import numpy as np

UP_SAMPLE = 3



from PIL import Image

def resize_image(input_path, output_path, max_size=(800, 600)):
    try:
        with Image.open(input_path) as img:
            # Check if the image size exceeds the maximum size
            if img.size[0] > max_size[0] or img.size[1] > max_size[1]:
                img.thumbnail(max_size)
                img.save(output_path)
                print(f"Image resized and saved to {output_path}")
            else:
                print("Image is already within the specified size")

    except Exception as e:
        print(f"Error: {e}")






def encode_known_faces(
    model: str = "hog", path: str = "", encodings_location: Path = DEFAULT_ENCODINGS_PATH
) -> None:
    names = []
    encodings = []
    print('a')
    
    print(model)
    show_output = False
    for filepath in Path("new_appointment_faces/"+path).glob("*"):
        print("Training "+str(filepath))
        name = filepath.parent.name
        image = face_recognition.load_image_file(filepath)
        
        print("Encoding Original..")
        face_locations = face_recognition.face_locations(image, model=model, number_of_times_to_upsample=UP_SAMPLE)
        face_encodings = face_recognition.face_encodings(image, face_locations)
        print("Done.")
        
        filepath = str(filepath)
        for encoding in face_encodings:
            names.append(name)
            encodings.append(encoding)

        try:
            # Read image from the disk.
            img = cv2.imread(filepath)
            # Shape of image in terms of pixels.
            (rows, cols) = img.shape[:2]

            # getRotationMatrix2D creates a matrix needed for transformation.
            # We want matrix for rotation w.r.t center to 20 degree without scaling.
            M = cv2.getRotationMatrix2D((cols / 2, rows / 2), 20, 1)
            res = cv2.warpAffine(img, M, (cols, rows))
            print("Encoding Image rotated 20 degrees..")
            face_locations = face_recognition.face_locations(res, model=model, number_of_times_to_upsample=UP_SAMPLE)
            face_encodings = face_recognition.face_encodings(res, face_locations)
            print("Done.")
            for encoding in face_encodings:
                names.append(name)
                encodings.append(encoding)
            
            M = cv2.getRotationMatrix2D((cols / 2, rows / 2), 340, 1)
            res = cv2.warpAffine(img, M, (cols, rows))
            print("Encoding Image rotated -20 degrees..")
            face_locations = face_recognition.face_locations(res, model=model, number_of_times_to_upsample=UP_SAMPLE)
            face_encodings = face_recognition.face_encodings(res, face_locations)
            print("Done.")
            for encoding in face_encodings:
                names.append(name)
                encodings.append(encoding)
            
            input_pts = np.float32([[0,0], [cols-1,0], [0,rows-1]])
            output_pts = np.float32([[cols-1,0], [0,0], [cols-1,rows-1]])
            # Calculate the transformation matrix using cv2.getAffineTransform()
            M= cv2.getAffineTransform(input_pts , output_pts)
            # Apply the affine transformation using cv2.warpAffine()
            res = cv2.warpAffine(img, M, (cols,rows))
            print("Encoding Flipped Image..")
            face_locations = face_recognition.face_locations(res, model=model, number_of_times_to_upsample=UP_SAMPLE)
            face_encodings = face_recognition.face_encodings(res, face_locations)
            print("Done.")
            if not show_output:
                #show_output = True
                out = cv2.hconcat([img, res])
                cv2.imshow('Output', out)
                cv2.waitKey(0)
            for encoding in face_encodings:
                names.append(name)
                encodings.append(encoding)


            name_encodings = {"names": names, "encodings": encodings}
            with encodings_location.open(mode="ab") as f:
                pickle.dump(name_encodings, f)
            #IPython.display.clear_output()
        except Exception as e:
            print(f"An error occurred while processing image: {filepath}")
            print(f"Error message: {str(e)}")

import socket
import os
import requests
import time
import photoAPI

def check_appointments():

    for photo in photoAPI.get_photo_list('http://10.12.42.22:3000/photos'):
        client_name = photo['filename'][:-4]
        try:
        
            # Create a directory with the received string as its name
            folder_path = os.path.join(os.getcwd(), "new_appointment_faces", client_name)
            os.makedirs(folder_path, exist_ok=False)
        except:
            response = "User (folder) already exists!"
            continue

        try:
            # Send an HTTP GET request to the URL
            response = requests.get(photo['url'])
            # Check if the request was successful
            if response.status_code == 200:
                # Check if the response content is not empty
                if response.content:
                    file_path = os.path.join(folder_path, client_name+".jpg")
                    with open(file_path, 'wb') as f:
                        f.write(response.content)
                    resize_image(file_path, file_path)
                else:
                    print("The response content is empty. The image may not be available.")
                    return False
            else:
                print(f"Failed to fetch the image. Status code: {response.status_code}")
                return False
        except:
            print("Error saving image")

	# Encode face
        encode_known_faces(path=client_name)


if __name__ == "__main__":
    # Start the server
    while True:
        check_appointments()
        time.sleep(5)
