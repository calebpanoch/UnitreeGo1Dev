# This script is to encode incoming appointment faces from the website.

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

import socket
import os

def start_server(host, port):
    # Create a socket object
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind the socket to a specific address and port
    server_socket.bind((host, port))

    # Listen for incoming connections
    server_socket.listen(5)
    print(f"Server listening on {host}:{port}")

    while True:
        # Wait for a connection from a client
        print("Waiting for new connection...")
        client_socket, client_address = server_socket.accept()
        print(f"Connection from {client_address}")

        # Receive string data from the client
        client_name = client_socket.recv(1024).decode('utf-8')
        print(f"Received string data: {client_name}")

        try:
        # Create a directory with the received string as its name
            folder_path = os.path.join(os.getcwd(), "new_appointment_faces", client_name)
            os.makedirs(folder_path, exist_ok=False)
        except:
            response = "User (folder) already exists!"
            client_socket.send(response.encode('utf-8'))
            client_socket.close()
            continue

        # Add a debug print statement
        print("Waiting to receive image data...")
        client_socket.settimeout(2)  # Set a timeout of 10 seconds
        # Receive image data from the client
        image_data = b""
        try:
            while True:
                chunk = client_socket.recv(1024)
                if not chunk:
                    print("Received no more data from the client.")
                    break
                image_data += chunk

        except socket.timeout:
            print("Timeout: No data received within the specified timeout.")


        # Add a debug print statement
        print("Image data received successfully.")

        # Save the received image to a file inside the directory
        image_filename = os.path.join(folder_path, client_name+".jpg")
        with open(image_filename, "wb") as image_file:
            image_file.write(image_data)
            print(f"Image received and saved as {image_filename}")

	# Encode face
        encode_known_faces(path=client_name)

        # Send a response back to the client
        response = f"Successfully encoded {client_name}."
        client_socket.send(response.encode('utf-8'))

        # Close the connection with the client
        client_socket.close()

if __name__ == "__main__":
    # Specify the host and port for the server
    host = "0.0.0.0"  # Use "0.0.0.0" to accept connections from any IP
    port = 4418

    # Start the server
    start_server(host, port)

