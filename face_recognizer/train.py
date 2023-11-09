from pathlib import Path
import face_recognition

from collections import Counter
from PIL import Image, ImageDraw
import pickle

DEFAULT_ENCODINGS_PATH = Path("output/encodings.pkl")



import cv2
import numpy as np

UP_SAMPLE = 3



def encode_known_faces(
    model: str = "hog", encodings_location: Path = DEFAULT_ENCODINGS_PATH
) -> None:
    names = []
    encodings = []
    print('a')
    
    print(model)
    show_output = False
    for filepath in Path("training").glob("*/*"):
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
                show_output = True
                out = cv2.hconcat([img, res])
                cv2.imshow('Output', out)
                cv2.waitKey(0)
            for encoding in face_encodings:
                names.append(name)
                encodings.append(encoding)


            name_encodings = {"names": names, "encodings": encodings}
            with encodings_location.open(mode="wb") as f:
                pickle.dump(name_encodings, f)
            #IPython.display.clear_output()
        except Exception as e:
            print(f"An error occurred while processing image: {filepath}")
            print(f"Error message: {str(e)}")
              
print('a')
encode_known_faces()
print("Done Encoding")

