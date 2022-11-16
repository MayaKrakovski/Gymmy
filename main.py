import Settings as s
from Camera import Camera
from Poppy import Poppy


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


if __name__ == '__main__':
    s.camera = Camera()
    s.robot = Poppy()

    s.camera.start()
    s.robot.start()

