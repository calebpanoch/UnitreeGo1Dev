import speech_recognition as sr


from ctypes import *
import pyaudio
import subprocess
import threading
import time

# Lock for synchronization
global_variable_lock = threading.Lock()


command = 'sh dance.sh'

# From alsa-lib Git 3fd4ab9be0db7c7430ebd258f2717a976381715d
# $ grep -rn snd_lib_error_handler_t
# include/error.h:59:typedef void (*snd_lib_error_handler_t)(const char *file, int line, const char *function, int err, const char *fmt, ...) /* __attribute__ ((format (printf, 5, 6))) */;
# Define our error handler type
ERROR_HANDLER_FUNC = CFUNCTYPE(None, c_char_p, c_int, c_char_p, c_int, c_char_p)
def py_error_handler(filename, line, function, err, fmt):
  #print('messages are yummy')
  pass
c_error_handler = ERROR_HANDLER_FUNC(py_error_handler)

asound = cdll.LoadLibrary('libasound.so')
# Set error handler
asound.snd_lib_error_set_handler(c_error_handler)



r = sr.Recognizer()
m = sr.Microphone()

lock = threading.Lock()

def recognize_audio(audio):
    print("a")
    try:
        # recognize speech using Google Speech Recognition
        value = r.recognize_google(audio)

        print("You said {}".format(value))

        if value == "hey robot dance" or value == "play robot dance" or value == "a robot dance":
            lock_acquired = global_variable_lock.acquire(blocking = False)
            if lock_acquired:
                print("DANCING!")
                process = subprocess.Popen(command, shell=True)
                time.sleep(20)
                print("DONE DANCING!")
                global_variable_lock.release()
            else:
                print("ALREADY DANCING!!")
    except sr.UnknownValueError:
        print("Oops! Didn't catch that")
    except sr.RequestError as e:
        print("Uh oh! Couldn't request results from Google Speech Recognition service; {0}".format(e))

try:
    print("A moment of silence, please...")
    with m as source: r.adjust_for_ambient_noise(source)
    print("Set minimum energy threshold to {}".format(r.energy_threshold))
    while True:
        print("Say something!")
        with m as source: audio = r.listen(source)
        print("Got it! Now to recognize it...")
        thread1 = threading.Thread(target=recognize_audio, args=(audio,))
        thread1.start()
except KeyboardInterrupt:
    pass
