import threading
import socket
import json
import math
# internal imports
from MP import MP
from Joint import Joint
import Settings as s
import Excel


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
            joints_str = []
            for i in data:
                joint_data = i.split(',')
                joints_str.append(joint_data)
            joints_str = joints_str[:-1]  # remove the empty list at the end
            # change from string to float values
            joints = []  # joints data
            for j in joints_str:
                joints.append(self.create_joint(j))
            return joints
            # print(joints)
        except socket.timeout:  # fail after 1 second of no activity
            print("Didn't receive data! [Timeout]")
            return None

    def create_joint(self, joint_as_list):
        # input - joint data list ; output - joint object
        # try:
        new_joint = Joint(joint_as_list[0], float(joint_as_list[1]), float(joint_as_list[2]), float(joint_as_list[3]))
        return new_joint
        # except:
        #     print("could not create new joint: list index out of range")
        #     return None

    def init_position(self):
        init_pos = False
        print("CAMERA: init position - please stand in front of the camera with hands to the sides")
        while not init_pos:
            jd = self.get_skeleton_data()
            if jd is not None:
                count = 0
                for j in jd:
                    print(j)
                    if j.visible:
                        count += 1
                if count == len(jd):  # all joints are visible - position initialized.
                    init_pos = True
            else:  # skeleton is not recognized in frame
                print("user is not recognized")
        print("CAMERA: init position verified")

    def calc_angle(self, joint1, joint2, joint3):
        a = self.calc_dist(joint1, joint2)
        b = self.calc_dist(joint1, joint3)
        c = self.calc_dist(joint2, joint3)
        try:
            rad_angle = math.acos((a ** 2 + b ** 2 - c ** 2) / (2 * a * b))
            deg_angle = (rad_angle * 180) / math.pi
            return round(deg_angle, 2)
        except:
            print("could not calculate the angle")

    def run(self):
        print ("CAMERA START")
        medaip = MP()
        medaip.start()
        joint_data_excel = []
        self.init_position()
        while not s.stop:
            joint_data_excel.append(self.get_skeleton_data())
            print(self.get_skeleton_data())

        Excel.wf_joints("try", joint_data_excel)


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



