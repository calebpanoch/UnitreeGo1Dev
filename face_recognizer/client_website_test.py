#This is a test client ran on the dog which acts as the website client.

import socket
import os

def send_data(host, port, client_name, image_path):
    # Create a socket object
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect to the server
    client_socket.connect((host, port))
    print(f"Connected to {host}:{port}")

    # Send the client name (string) to the server
    client_socket.send(client_name.encode('utf-8'))
    print(f"Sent client name: {client_name}")

    # Send the image to the server
    with open(image_path, 'rb') as image_file:
        image_data = image_file.read()
        client_socket.send(image_data)
        print("Sent image data")

    # Receive and print the server's response
    response = client_socket.recv(1024).decode('utf-8')
    print(f"Server response: {response}")

    # Close the connection
    client_socket.close()

if __name__ == "__main__":
    # Specify the host and port for the server
    server_host = "192.168.123.13"
    server_port = 4418

    # Specify the client name and image path
    client_name = "Caleb5"  # Change this to your desired client name
    image_path = "me.jpg"  # Change this to the path of your image file

    # Send data to the server
    send_data(server_host, server_port, client_name, image_path)
