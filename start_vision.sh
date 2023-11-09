#!/bin/bash

#open terminal in head nano for start_capture.sh-----------------------------------
gnome-terminal -- bash -c "cd /home/unitree/Unitree/sdk/UnitreecameraSDK-main && sh start_capture.sh"

#open terminal in head nano for stream.py--------------------------------------------
gnome-terminal -- bash -c "cd /home/unitree/Unitree/sdk/UnitreecameraSDK-main && python3 stream.py"

sleep 5

#SSH into nx board to do person detection (with start_recognition and stream_capture)---------
# Set the SSH connection information
remote_server="192.168.123.15"
ssh_user="unitree"
ssh_password="123"

# Set the command you want to run remotely
remote_command="cd ~/Desktop/objectDetection/content/yolov7 && sh start_recognition.sh"

#python3 stream_capture.py"

# Use sshpass to execute the SSH command with a password
sshpass -p "$ssh_password" ssh -X "$ssh_user@$remote_server" "$remote_command"


#SSH back into head nano to do face recognition----------------------------------------
# Set the SSH connection information
remote_server1="192.168.123.13"
ssh_user1="unitree"
ssh_password1="123"

# Set the command you want to run remotely
remote_command1="cd ~/Unitree/sdk/UnitreecameraSDK-main/face_recognizer && python3 main.py"

# Use sshpass to execute the SSH command with a password
gnome-terminal -- bash -c "cd ~/Unitree/sdk/UnitreecameraSDK-main/face_recognizer && python3 main.py"