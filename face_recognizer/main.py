from pathlib import Path
import os
import time
import face_recognition
import trio

from collections import Counter
from PIL import Image, ImageDraw
import pickle

DEFAULT_ENCODINGS_PATH = Path("output/encodings.pkl")

import cv2
import numpy as np

UP_SAMPLE = 1
showImage = False
detectedPerson = None
guesses = []

#SEVER STUFF
import socket

# Create a socket object
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Define the server address (host and port)
host = '0.0.0.0'  # Change this to the IP address of your server
port = 50349       # Change this to the port you want to use

# Bind the socket to the server address
server_socket.bind((host, port))


#server_socket.close()

#FACELIGHT STUFF
import subprocess
# Replace 'your_command_here' with the actual command you want to run
command = 'cd /home/unitree/Unitree/sdk/faceLightSDK_Nano && ./bin/faceLightBlue'
command2 = 'cd /home/unitree/Unitree/sdk/faceLightSDK_Nano && ./bin/faceLightOff'
command3 = 'cd /home/unitree/Unitree/sdk/faceLightSDK_Nano && ./bin/faceLightRed'
command_yellow = 'cd /home/unitree/Unitree/sdk/faceLightSDK_Nano && ./bin/faceLightYellow'
command_talk = 'cd /home/unitree/Unitree/sdk/UnitreecameraSDK-main/face_recognizer && python3 audio.py --source '

async def run_talk(cmd):
	result = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

async def run_light(cmd):
	result = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	await trio.sleep(2)
	result = subprocess.run(command2, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

def _recognize_face(unknown_encoding, loaded_encodings):
    boolean_matches = face_recognition.compare_faces(
        loaded_encodings["encodings"], unknown_encoding, tolerance=.6
    )
    votes = Counter(
        name
        for match, name in zip(boolean_matches, loaded_encodings["names"])
        if match
    )

    if votes:
        guessedName = votes.most_common(1)[0][0]
        rightGuesses = 0
        wrongGuesses = 0
        for match, name in zip(boolean_matches, loaded_encodings["names"]):
            if not match and name != guessedName:
                rightGuesses += 1
            elif match and name == guessedName:
                rightGuesses += 1
            else:
                wrongGuesses += 1


    # Calculate the total number of guesses
        totalGuesses = rightGuesses + wrongGuesses

    # Calculate the accuracy
        accuracy = rightGuesses / totalGuesses

        accuracy_percentage = accuracy * 100  # If you want it as a percentage

        print(f"{guessedName}, Confidence: {accuracy_percentage:.2f}%")


    #print(face_recognition.face_distance(loaded_encodings["encodings"], unknown_encoding)) #HERE FOR ACCURACY!!!??
    if votes:
        return votes.most_common(1)[0][0],int(accuracy_percentage)
   

#pilowImage = 0


def recognize_faces(
    image_location: str,
    model: str = "cnn",
    #i: int = 0,
    encodings_location: Path = DEFAULT_ENCODINGS_PATH,
) -> None:

	with encodings_location.open(mode="rb") as f:
	    loaded_encodings = pickle.load(f)

	try:
		input_image = face_recognition.load_image_file(image_location)
	except:
		print("Couldn't Open Image!")
		return

	height, width, channels = input_image.shape
	input_image = input_image[0:int(height/2), int(width/2):width] #this line crops to one camera and top half of it
	
	#crops 25 percent from left & right & top
	height, width, channels = input_image.shape
	input_image = input_image[int(height/4):, int(0+width/4):int(width-(width/4))]
	# Define the zoom factor
	zoom_factor = 2  # You can adjust this value as needed

	# Resize the image to make it bigger
	input_image = cv2.resize(input_image, None, fx=zoom_factor, fy=zoom_factor, interpolation=cv2.INTER_LINEAR)


	input_face_locations = face_recognition.face_locations(
	    input_image, model=model
	)
	input_face_encodings = face_recognition.face_encodings(
	    input_image, input_face_locations
	)

	for bounding_box, unknown_encoding in zip(
		input_face_locations, input_face_encodings
	):

		result = _recognize_face(unknown_encoding, loaded_encodings)


		if result is not None:
			name, confidence = result
			# Now you can safely use name and confidence
		else:
			# Handle the case when _recognize_face returns None
			print("Face recognition failed.")
			return
		
		#name,confidence = _recognize_face(unknown_encoding, loaded_encodings)
		if confidence > 80:
			guesses.append(name)
			if len(guesses) == 1:
				trio.run(run_talk,command_talk+"first.wav")
				
			elif len(guesses) == 2:
				trio.run(run_talk,command_talk+"second.wav")
			elif len(guesses) == 3:
				pass
			print(guesses)
		if not name:
			name = "Unknown"
		elif name == "Caleb" and confidence > 80:
			#trio.run(run_light,command)

			pillowImage = Image.fromarray(input_image)
			if showImage == True:
				pillowImage.show()
		elif name == "Endian" and confidence > 80:
			#trio.run(run_light,command3)
			pass

	    # Removed print(name, bounding_box)
		#_display_face(draw, bounding_box, name)
		print("Found face: "+name)

	#del draw
	if 2 == 8:
		pillowImage = Image.fromarray(input_image)
		if showImage == True:
			pillowImage.show()



def validate(model: str = "hog"):
	for filepath in Path("validation").rglob("*"):
		if filepath.is_file():
			recognize_faces(
				image_location=str(filepath.absolute()), model=model
			)

# Removed recognize_faces("unknown.jpg")
#validate()


count = 1
while True:
	server_socket.listen(1)

	print("Waiting for a client to connect...")

	# Accept a connection from a client
	client_socket, client_address = server_socket.accept()

	print("Connected to", client_address)
	# Receive data from the client
	data = client_socket.recv(1024).decode('utf-8')
	    
	if not data:
	    break
	    
	print("Received:", data)

	result = subprocess.run(command_talk+"initiate.wav", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
#	time.sleep(5)

	detectedPerson = None
	guesses = []

	while detectedPerson == None:
		#count = count + 1
		try:
			recognize_faces(
			image_location="/home/unitree/Unitree/sdk/UnitreecameraSDK-main/MyImage.jpg", 				model="hog"#,
				#i=count
			)
			#if pillowImage:
				#pillowImage.close()
		except KeyboardInterrupt:
			print('Interrupted')
			sys.exit()
		#if count == 8:
		#	count = 0
		#print('check image')
		if len(guesses) >= 3:
			string_counts = Counter(guesses)

			# Find the most common string and its count
			most_common_string, count = string_counts.most_common(1)[0]
			if count >= 2:
				detectedPerson = most_common_string
				break

	response = detectedPerson
	if response == "Caleb":
		result = subprocess.run(command_talk+"caleb.wav", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	print("Sending response: "+detectedPerson)
	client_socket.send(response.encode('utf-8'))

	trio.run(run_light,command_yellow)
