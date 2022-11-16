
import threading
import socket
import json
from MP import MP
from Joint import joint


class Camera(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        # Create socket for client-server communication with Camera.py
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.server_address = ('localhost', 7000)
        self.sock.bind(self.server_address)
        print ("CAMERA INITIALIZATION")

    def get_skeleton_data(self):
        self.sock.settimeout(1)
        try:
            data, address = self.sock.recvfrom(4096)
            print('received {} bytes from {}'.format(len(data), address))
            data = json.loads(data.decode())

            data = data.split('/')
            jointsStr = []
            for i in data:
                joint_data = i.split(',')
                jointsStr.append(joint_data)
            jointsStr = jointsStr[:-1]  # remove the empty list at the end
            # change from string to float values
            joints = []  # joints data
            for j in jointsStr:
                joints.append(self.create_joint(j))
            return joints

            # print(joints)
        except socket.timeout:  # fail after 1 second of no activity
            print("Didn't receive data! [Timeout]")
            return None

    def create_joint(self, joint_as_list):
        # input - joint data list ; output - joint object
        try:
            new_joint = joint(joint_as_list[0], float(joint_as_list[1]), float(joint_as_list[2]), float(joint_as_list[3]))
            return new_joint
        except:
            print("could not create new joint: list index out of range")
            return None

    def run(self):
        print ("CAMERA START")
        medaip = MP()
        medaip.start()
        while (True):
            print(self.get_skeleton_data())


if __name__ == '__main__':
    print('HelloServer')
    c = Camera()
    c.start()




    #
    # # Create a UDP socket
    # sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    #
    # # Bind the socket to a specific port
    # server_address = ('localhost', 7000)
    # sock.bind(server_address)
    #
    # while True:
    #     print('Waiting for data...')
    #     sock.settimeout(1)  # to check
    #     try:
    #         data, address = sock.recvfrom(4096)
    #         print('received {} bytes from {}'.format(len(data), address))
    #         data = json.loads(data.decode())
    #
    #         data = data.split('/')
    #         jointsStr = []
    #         for i in data:
    #             joint_data = i.split(',')
    #             jointsStr.append(joint_data)
    #         jointsStr = jointsStr[:-1]  # remove the empty list at the end
    #         # change from string to float values
    #         joints = []  # joints data
    #         for j in jointsStr:
    #             joints.append(create_joint(j))
    #
    #         # print(joints)
    #     except socket.timeout:  # fail after 1 second of no activity
    #         print("Didn't receive data! [Timeout]")



