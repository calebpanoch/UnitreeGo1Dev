import subprocess
import argparse

parser = argparse.ArgumentParser()
#parser.add_argument('--weights', nargs='+', type=str, default='initiate.wav', help='model.pt path(s)')
parser.add_argument('--source', type=str, default='/initiate.wav', help='source')  # file/folder, 0 for webcam

opt = parser.parse_args()
#directory_path = opt.directory
print(opt.source)

# Get the process ID of the command using ps and grep
ps_command = "ps -aux | grep wsaudio"
output = subprocess.check_output(ps_command, shell=True).decode()

# Find the process ID line in the output
pid_line = next(line for line in output.split('\n') if 'wsaudio' in line)

# Extract the PID from the line
pid = pid_line.split()[1]

# Kill the process using sudo and the extracted PID
kill_command = f"echo '123' | sudo -S kill -9 {pid}"
subprocess.call(kill_command, shell=True)

# Execute the volume command
aplay_command = "amixer -c 2 set Speaker 20"
subprocess.call(aplay_command, shell=True)

# Execute the aplay command
aplay_command = "aplay -D plughw:2,0 /home/unitree/Unitree/sdk/UnitreecameraSDK-main/face_recognizer/Audios/"+opt.source
subprocess.call(aplay_command, shell=True)
