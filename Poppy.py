import threading
from pypot.creatures import PoppyTorso
import time
import Settings as s


class Poppy(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        # self.poppy = PoppyTorso()  # for real robot
        self.poppy = PoppyTorso(simulator='vrep')  # for simulator
        print("ROBOT INITIALIZATION")
        for m in self.poppy.motors:  # motors need to be initialized, False=stiff, True=loose
            m.compliant = False
        self.init_robot()

    def init_robot(self):
        for m in self.poppy.motors:
            if not m.name == 'r_elbow_y' and not m.name == 'l_elbow_y' and not m.name == 'head_y':
                m.goto_position(0, 1, wait=True)
        self.poppy.head_y.goto_position(-20,1,wait=True)
        self.poppy.r_elbow_y.goto_position(90, 1, wait=True)
        self.poppy.l_elbow_y.goto_position(90, 1, wait=True)

    def run(self):
        print("ROBOT START")
        while not s.stop:
            if s.req_exercise != "":
                print("ROBOT: Exercise ", s.req_exercise, " start")
                self.exercise_demo(s.req_exercise)
                print("ROBOT: Exercise ", s.req_exercise, " done")
                s.req_exercise = ""

    def exercise_demo(self, ex):
        for i in range(s.rep):
            getattr(self, ex)(i)

    # EX1 - Raise arms horizontally
    def raise_arms_horizontally(self, counter):
        hands_up = [self.poppy.l_shoulder_x.goto_position(90, 1.5, wait=False),
                    self.poppy.l_elbow_y.goto_position(90, 1.5, wait=False),
                    self.poppy.r_shoulder_x.goto_position(-90, 1.5, wait=False),
                    self.poppy.r_elbow_y.goto_position(90, 1.5, wait=False)]
        time.sleep(2)
        hands_down = [self.poppy.l_shoulder_x.goto_position(0, 1.5, wait=False),
                      self.poppy.l_elbow_y.goto_position(90, 1.5, wait=False),
                      self.poppy.r_shoulder_x.goto_position(0, 1.5, wait=False),
                      self.poppy.r_elbow_y.goto_position(90, 1.5, wait=False)]
        time.sleep(2)

    # EX2 - Bend Elbows
    def bend_elbows(self, counter):
        self.poppy.r_arm[3].goto_position(-60, 1.5, wait=False)
        self.poppy.l_arm[3].goto_position(-60, 1.5, wait=True)
        time.sleep(0.5)
        self.poppy.r_arm[3].goto_position(85, 1.5, wait=False)
        self.poppy.l_arm[3].goto_position(85, 1.5, wait=True)

    # EX3 - Raise Arms Bend Elbows
    def raise_arms_bend_elbows(self, counter):
        l_hand = [self.poppy.l_shoulder_y.goto_position(-90, 2, wait=False),
                  self.poppy.l_arm_z.goto_position(-90, 2, wait=False),
                  self.poppy.l_shoulder_x.goto_position(50, 2, wait=False),
                  self.poppy.l_elbow_y.goto_position(-50, 2, wait=False)]
        r_hand = [self.poppy.r_shoulder_y.goto_position(-90, 2, wait=False),
                  self.poppy.r_arm_z.goto_position(90, 2, wait=False),
                  self.poppy.r_shoulder_x.goto_position(-50, 2, wait=False),
                  self.poppy.r_elbow_y.goto_position(-50, 2, wait=False)]
        time.sleep(3)
        self.poppy.r_shoulder_x.goto_position(-85, 1.5, wait=False)
        self.poppy.l_shoulder_x.goto_position(95, 1.5, wait=False)
        self.poppy.r_elbow_y.goto_position(90, 1.5, wait=False)
        self.poppy.l_elbow_y.goto_position(90, 1.5, wait=True)
        if counter == s.rep-1:
            # init
            self.poppy.l_arm_z.goto_position(0, 1.5, wait=False)
            self.poppy.r_arm_z.goto_position(0, 1.5, wait=False)
            self.poppy.l_shoulder_y.goto_position(0, 1.5, wait=False)
            self.poppy.r_shoulder_y.goto_position(0, 1.5, wait=True)
            self.poppy.l_shoulder_x.goto_position(0, 1.5, wait=False)
            self.poppy.r_shoulder_x.goto_position(0, 1.5, wait=False)
            time.sleep(2)

if __name__ == "__main__":
    s.rep = 8
    s.stop = False
    robot = Poppy()
    robot.start()