import threading
from pypot.creatures import PoppyTorso
import time
import Settings as s
from Audio import say


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
        self.poppy.head_y.goto_position(-20, 1, wait=True)
        self.poppy.r_elbow_y.goto_position(90, 1, wait=True)
        self.poppy.l_elbow_y.goto_position(90, 1, wait=True)

    def run(self):
        print("ROBOT START")
        while not s.finish_workout:
            time.sleep(0.00000001)  # Prevents the MP to stuck
            if s.req_exercise != "":
                time.sleep(1)
                print("ROBOT: Exercise ", s.req_exercise, " start")
                self.exercise_demo(s.req_exercise)
                print("ROBOT: Exercise ", s.req_exercise, " done")
                while not s.waved:
                    time.sleep(0.01)  # for hello_waiting exercise, wait until user wave
                s.req_exercise = ""
                s.poppy_done = True
        print("Robot Done")

    def exercise_demo(self, ex):
        if ex == "hello_waving":
            self.hello_waving()
        else:
            for i in range(s.rep):
                getattr(self, ex)(i)
                if s.success_exercise:
                    break

    def hello_waving(self):
        self.poppy.r_shoulder_x.goto_position(-90, 1.5, wait=False)
        self.poppy.r_elbow_y.goto_position(-20, 1.5, wait=False)
        self.poppy.r_arm_z.goto_position(-80, 1.5, wait=False)
        for i in range(3):
            self.poppy.r_arm[3].goto_position(-35, 0.6, wait=True)
            self.poppy.r_arm[3].goto_position(35, 0.6, wait=True)
        self.finish_waving()

    def finish_waving(self):
        self.poppy.r_shoulder_x.goto_position(0, 1.5, wait=False)
        self.poppy.r_elbow_y.goto_position(90, 1.5, wait=False)
        self.poppy.r_arm_z.goto_position(0, 1.5, wait=False)

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
        if s.robot_count:
            say(str(counter + 1))
        time.sleep(2)

    # EX2 - Bend Elbows
    def bend_elbows(self, counter):
        self.poppy.r_arm[3].goto_position(-60, 1.5, wait=False)
        self.poppy.l_arm[3].goto_position(-60, 1.5, wait=True)
        time.sleep(2)
        self.poppy.r_arm[3].goto_position(85, 1.5, wait=False)
        self.poppy.l_arm[3].goto_position(85, 1.5, wait=True)
        if s.robot_count:
            say(str(counter + 1))
        time.sleep(2)

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
        time.sleep(2)
        self.poppy.r_shoulder_x.goto_position(-85, 1.5, wait=False)
        self.poppy.l_shoulder_x.goto_position(95, 1.5, wait=False)
        self.poppy.r_elbow_y.goto_position(90, 1.5, wait=False)
        self.poppy.l_elbow_y.goto_position(90, 1.5, wait=True)
        if s.robot_count:
            say(str(counter + 1))
        time.sleep(2)
        if counter >= s.rep-1 or s.success_exercise:  # TODO - Change to something that works if it finished before 8 repetitions.
            # return to init position
            self.poppy.l_arm_z.goto_position(0, 1.5, wait=False)
            self.poppy.r_arm_z.goto_position(0, 1.5, wait=False)
            self.poppy.l_shoulder_y.goto_position(0, 1.5, wait=False)
            self.poppy.r_shoulder_y.goto_position(0, 1.5, wait=True)
            self.poppy.l_shoulder_x.goto_position(0, 1.5, wait=False)
            self.poppy.r_shoulder_x.goto_position(0, 1.5, wait=False)

    # Ex4 - open and close arms
    def open_and_close_arms(self, counter):
        if counter == 0:
            self.poppy.l_shoulder_y.goto_position(-90, 2, wait=False)
            self.poppy.r_shoulder_y.goto_position(-90, 2, wait=False)
        self.poppy.r_shoulder_x.goto_position(-85, 1.5, wait=False)
        self.poppy.l_shoulder_x.goto_position(95, 1.5, wait=False)
        # self.poppy.r_elbow_y.goto_position(90, 1.5, wait=False)
        # self.poppy.l_elbow_y.goto_position(90, 1.5, wait=True)
        time.sleep(2)
        self.poppy.l_shoulder_x.goto_position(0, 2, wait=False)
        self.poppy.r_shoulder_x.goto_position(0, 2, wait=True)
        if s.robot_count:
            say(str(counter + 1))
        time.sleep(2)
        if counter >= s.rep-1 or s.success_exercise:  # TODO - Change to something that works if it finished before 8 repetitions.
            self.poppy.l_shoulder_y.goto_position(0, 2, wait=False)
            self.poppy.r_shoulder_y.goto_position(0, 2, wait=False)
            self.poppy.l_shoulder_x.goto_position(0, 2, wait=False)
            self.poppy.r_shoulder_x.goto_position(0, 2, wait=True)

    # EX5 - open and close arms 90
    def open_and_close_arms_90(self, counter):
        if counter == 0:
            self.poppy.l_shoulder_y.goto_position(-90, 1.5, wait=False)
            self.poppy.r_shoulder_y.goto_position(-90, 1.5, wait=True)
            self.poppy.l_elbow_y.goto_position(0, 1.5, wait=False)
            self.poppy.r_elbow_y.goto_position(0, 1.5, wait=True)
        self.poppy.l_shoulder_x.goto_position(90, 1, wait=False)
        self.poppy.r_shoulder_x.goto_position(-90, 1, wait=True)
        time.sleep(2)
        self.poppy.l_shoulder_x.goto_position(0, 1, wait=False)
        self.poppy.r_shoulder_x.goto_position(0, 1, wait=True)
        if s.robot_count:
            say(str(counter + 1))
        time.sleep(2)
        if counter >= s.rep-1 or s.success_exercise:  # TODO - Change to something that works if it finished before 8 repetitions.
            self.poppy.r_elbow_y.goto_position(90, 1.5, wait=False)
            self.poppy.l_elbow_y.goto_position(90, 1.5, wait=True)
            self.poppy.l_shoulder_y.goto_position(0, 1.5, wait=False)
            self.poppy.r_shoulder_y.goto_position(0, 1.5, wait=True)
            self.poppy.l_shoulder_x.goto_position(0, 1.5, wait=False)
            self.poppy.r_shoulder_x.goto_position(0, 1.5, wait=False)

    # EX 6 raise_arms_forward
    def raise_arms_forward(self, counter):
            self.poppy.l_shoulder_y.goto_position(-90, 1.5, wait=False)
            self.poppy.r_shoulder_y.goto_position(-90, 1.5, wait=False)
            self.poppy.l_arm_z.goto_position(-90, 1.5, wait=False)
            self.poppy.r_arm_z.goto_position(90, 1.5, wait=False)
            time.sleep(2)
            self.poppy.l_arm_z.goto_position(0, 1.5, wait=False)
            self.poppy.r_arm_z.goto_position(0, 1.5, wait=False)
            self.poppy.l_shoulder_y.goto_position(0, 1.5, wait=False)
            self.poppy.r_shoulder_y.goto_position(0, 1.5, wait=True)
            if s.robot_count:
                say(str(counter + 1))
            time.sleep(2)


if __name__ == "__main__":
    s.rep = 3
    s.robot_count = True
    s.success_exercise = False
    s.finish_workout = False
    language = 'Hebrew'
    gender = 'Male'
    s.audio_path = 'audio files/' + language + '/' + gender + '/'

    robot = Poppy()

    # robot.exercise_demo("open_and_close_arms_90")
    robot.exercise_demo("raise_arms_forward")
    # robot.start()
    time.sleep(10)

    # robot.poppy.l_shoulder_y.goto_position(-90, 1.5, wait=False)
    # robot.poppy.r_shoulder_y.goto_position(-90, 1.5, wait=True)
    # robot.poppy.l_shoulder_x.goto_position(90, 1, wait=False)
    # # robot.poppy.r_shoulder_x.goto_position(-90, 1, wait=True)
    # robot.poppy.l_elbow_y.goto_position(0, 1.5, wait=False)
    # robot.poppy.r_elbow_y.goto_position(0, 1.5, wait=True)

