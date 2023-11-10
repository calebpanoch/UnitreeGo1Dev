#SSH into nx board to do person detection (with start_recognition and stream_capture)---------
# Set the SSH connection information
remote_server="192.168.123.15"
ssh_user="unitree"
ssh_password="123"

# Set the command you want to run remotely
remote_command="cd ~/Desktop/NodeJS-Test && node dance.js"

#python3 stream_capture.py"

# Use sshpass to execute the SSH command with a password
sshpass -p "$ssh_password" ssh -X "$ssh_user@$remote_server" "$remote_command"

