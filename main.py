import time

import Settings as s
from Camera import Camera
from Poppy import Poppy
from Audio import Audio
from Training import Training
import Excel


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


if __name__ == '__main__':
    s.camera_num = 0  # 0 - webcam, 2 - second USB in maya's computer

    # Audio variables initialization
    language = 'Hebrew'
    gender = 'Female'
    s.audio_path = 'audio files/' + language + '/' + gender + '/'
    s.str_to_say = ""

    # Training variables initialization
    s.exercise_amount = 6
    s.rep = 8
    s.req_exercise = ""
    s.stop = False
    s.waved = False
    s.success_exercise = False

    # Create all components
    Excel.create_workbook()
    s.camera = Camera()
    s.training = Training()
    s.robot = Poppy()
    # TODO add screen

    # Start all threads
    s.camera.start()
    # time.sleep(10) #let the camera start
    s.training.start()
    s.robot.start()
    # TODO add screen

