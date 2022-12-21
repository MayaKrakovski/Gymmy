import threading
import socket
import json
import math
import time

import numpy as np
from statistics import mean, stdev

# internal imports
from MP import MP
from Joint import Joint
import Settings as s
import Excel
from Audio import say


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
            # print('received {} bytes from {}'.format(len(data), address))
            data = json.loads(data.decode())
            data = data.split('/')
            joints_str = []
            for i in data:
                joint_data = i.split(',')
                joints_str.append(joint_data)
            joints_str = joints_str[:-1]  # remove the empty list at the end
            # change from string to float values
            joints = {}  # joints dict data
            for j in joints_str:
                joints[j[0]] = Joint(j[0], float(j[1]), float(j[2]), float(j[3]))
            return joints
        except socket.timeout:  # fail after 1 second of no activity
            print("Didn't receive data! [Timeout]")
            return None

    def init_position(self):
        # Check user position - so all joints all visible, and all exercise will be able to be recognized.
        init_pos = False
        say("calibration")
        print("CAMERA: init position - please stand in front of the camera with hands to the sides")
        while not init_pos:
            jd = self.get_skeleton_data()
            if jd is not None:
                count = 0
                for j in jd.values():
                    print(j)
                    if j.visible:
                        count += 1
                angle_right = self.calc_angle(jd["R_Shoulder"], jd["R_Hip"], jd["R_Wrist"])
                angle_left = self.calc_angle(jd["L_Shoulder"], jd["L_Hip"], jd["L_Wrist"])
                if count == len(jd) and angle_right > 80 and angle_left > 80:
                    init_pos = True  # all joints are visible + arms are raised to the sides - position initialized.
            else:  # skeleton is not recognized in frame
                print("user is not recognized")
        say("calibration_complete")
        s.calibration = True
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
            # pass
            print("could not calculate the angle")

    def calc_angle2(self, joint1, joint2, joint3):
        a = np.array([joint1.x, joint1.y]) # First
        b = np.array([joint2.x, joint2.y]) # Mid
        c = np.array([joint3.x, joint3.y]) # End

        radians = np.arctan2(c[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])
        angle = np.abs(radians*180.0/np.pi)

        if angle >180.0:
            angle = 360-angle

        return round(angle,2)

    def calc_dist(self, joint1, joint2):
            distance = math.hypot(joint1.x - joint2.x,
                                  joint1.y - joint2.y)
            return distance

    def exercise_two_angles(self, exercise_name, joint1, joint2, joint3, up_lb, up_ub, down_lb, down_ub,
                            joint4, joint5, joint6, up_lb2, up_ub2, down_lb2, down_ub2):
        flag = True
        counter = 0
        list_joints = []
        while s.req_exercise == exercise_name:
            joints = self.get_skeleton_data()
            if joints is not None:
                right_angle = self.calc_angle(joints[str("R_"+joint1)], joints[str("R_"+joint2)],
                                              joints[str("R_"+joint3)])
                left_angle = self.calc_angle(joints[str("L_"+joint1)], joints[str("L_"+joint2)],
                                             joints[str("L_"+joint3)])
                right_angle2 = self.calc_angle(joints[str("R_"+joint4)], joints[str("R_"+joint5)],
                                              joints[str("R_"+joint6)])
                left_angle2 = self.calc_angle(joints[str("L_"+joint4)], joints[str("L_"+joint5)],
                                             joints[str("L_"+joint6)])
                new_entry = [joints[str("R_"+joint1)], joints[str("R_"+joint2)], joints[str("R_"+joint3)],
                             joints[str("L_"+joint1)], joints[str("L_"+joint2)], joints[str("L_"+joint3)],
                             joints[str("R_"+joint4)], joints[str("R_"+joint5)], joints[str("R_"+joint6)],
                             joints[str("L_"+joint4)], joints[str("L_"+joint5)], joints[str("L_"+joint6)],
                             right_angle, left_angle, right_angle2, left_angle2]
                list_joints.append(new_entry)
                if right_angle is not None and left_angle is not None:
                    if (up_lb < right_angle < up_ub) & (up_lb < left_angle < up_ub) & \
                            (up_lb2 < right_angle2 < up_ub2) & (up_lb2 < left_angle2 < up_ub2) & (not flag):
                        flag = True
                        counter += 1
                        print(counter)
                        say(str(counter))
                    if (down_lb < right_angle < down_ub) & (down_lb < left_angle < down_ub) & \
                            (down_lb2 < right_angle2 < down_ub2) & (down_lb2 < left_angle2 < down_ub2) &(flag):
                        flag = False
            if counter == s.rep:
                s.req_exercise = ""
                s.success_exercise = True
                break

        Excel.wf_joints("ex", list_joints)

    def exercise_one_angle(self, exercise_name, joint1, joint2, joint3, up_lb, up_ub, down_lb, down_ub):
        flag = True
        counter = 0
        list_joints = []
        while s.req_exercise == exercise_name:
            joints = self.get_skeleton_data()
            if joints is not None:
                right_angle = self.calc_angle(joints[str("R_"+joint1)], joints[str("R_"+joint2)],
                                              joints[str("R_"+joint3)])
                left_angle = self.calc_angle(joints[str("L_"+joint1)], joints[str("L_"+joint2)],
                                             joints[str("L_"+joint3)])
                new_entry = [joints[str("R_"+joint1)], joints[str("R_"+joint2)], joints[str("R_"+joint3)],
                             joints[str("L_"+joint1)], joints[str("L_"+joint2)], joints[str("L_"+joint3)],
                             right_angle, left_angle]
                list_joints.append(new_entry)
                if right_angle is not None and left_angle is not None:
                    if (up_lb < right_angle < up_ub) & (up_lb < left_angle < up_ub) & (not flag):
                        flag = True
                        counter += 1
                        print(counter)
                        say(str(counter))
                    if (down_lb < right_angle < down_ub) & (down_lb < left_angle < down_ub) & (flag):
                        flag = False
            if counter == s.rep:
                s.req_exercise = ""
                s.success_exercise = True
                break
        s.ex_list.append([exercise_name, counter])

        Excel.wf_joints("ex", list_joints)

    def raise_arms_horizontally(self):
        self.exercise_one_angle("raise_arms_horizontally", "Shoulder", "Hip", "Wrist", 80, 105, 5, 30)

    def bend_elbows(self):
        self.exercise_one_angle("bend_elbows", "Elbow", "Shoulder", "Wrist", 165, 180, 1, 20)

    def raise_arms_bend_elbows(self):
        self.exercise_two_angles("raise_arms_bend_elbows", "Elbow", "Shoulder", "Wrist", 130, 180, 5, 35,
                                 "Shoulder", "Hip", "Elbow", 70, 120, 70, 120)

    def hello_waving(self): # check if the participant waved
        time.sleep(8)
        say('ready wave')
        while s.req_exercise == "hello_waving":
            joints = self.get_skeleton_data()
            if joints is not None:
                right_shoulder = joints[str("R_Shoulder")]
                right_wrist = joints[str("R_Wrist")]
                if right_shoulder.y < right_wrist.y != 0:
                    print(right_shoulder.y)
                    print(right_wrist.y)
                    s.waved = True
                    s.req_exercise = ""

    def check_angle_range(self, joint1, joint2, joint3):
        # just for coding and understanding angle boundaries
        list_joints = []
        while not s.finish_workout:
            joints = self.get_skeleton_data()
            if joints is not None:
                right_angle = self.calc_angle(joints[str("R_"+joint1)], joints[str("R_"+joint2)],
                                              joints[str("R_"+joint3)])
                left_angle = self.calc_angle(joints[str("L_"+joint1)], joints[str("L_"+joint2)],
                                             joints[str("L_"+joint3)])
                if right_angle is not None and left_angle is not None:
                    list_joints.append(right_angle)
                    list_joints.append(left_angle)
        print(list_joints)
        print(mean(list_joints))
        print(stdev(list_joints))

    def run(self):
        print ("CAMERA START")
        medaip = MP()
        medaip.start()

        while not s.finish_workout:
            time.sleep(0.00000001)  # Prevents the MP to stuck
            if s.req_exercise != "":
                print("CAMERA: Exercise ", s.req_exercise, " start")
                getattr(self, s.req_exercise)()
                print("CAMERA: Exercise ", s.req_exercise, " done")
                s.req_exercise = ""


if __name__ == '__main__':
    s.finish_workout = False
    s.req_exercise = ""
    print('HelloServer')
    c = Camera()
    c.start()