import threading
import time
import Settings as s
import Excel
import random
from Audio import say


class Training(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        print("TRAINING START")
        self.run_exercise("hello_waving")
        print("Training: start waving")
        while not s.waved:
            time.sleep(0.00000001)  # Prevents the MP to stuck
            continue
        print("Training: Calibration")
        s.camera.init_position()
        while not s.calibration:
            time.sleep(0.00000001)
            continue
        time.sleep(3)
        say('lets start')
        time.sleep(2)
        print("Training: finish waving")

        if s.adaptive:
            self.adatpive_training_session()
        else:
            self.training_session()

        self.finish_workout()

    def adatpive_training_session(self):
        self.training_session()
        # exercise_names = ["raise_arms_horizontally", "bend_elbows"]
        # for e in exercise_names:
        #     self.run_exercise(e)
        #     time.sleep(5)

    def training_session(self):
        print("Training: start exercises")
        # TODO - adding random choice of exercises.
        exercise_names = ["raise_arms_horizontally", "bend_elbows", "raise_arms_bend_elbows", "open_and_close_arms",
                          "open_and_close_arms_90"]
        for e in exercise_names:
            self.run_exercise(e)
            time.sleep(5)

    def finish_workout(self):
        say('goodbye')
        s.finish_workout = True
        Excel.success_worksheet()
        Excel.close_workbook()
        time.sleep(10)
        s.screen.quit()
        print("TRAINING DONE")

    def run_exercise(self, name):
        s.success_exercise = False
        print("TRAINING: Exercise ", name, " start")
        s.req_exercise = name
        say(name)
        time.sleep(10)  # Delay the robot movement after the audio is played
        while s.req_exercise == name:
            time.sleep(0.00000001)  # Prevents the MP to stuck
        if s.success_exercise: # TODO change for adaptive training
            say(self.random_encouragement())
        print("TRAINING: Exercise ", name, " done")

    def random_encouragement(self):
        enco = ["well done", "very good", "excellent"]
        return random.choice(enco)


if __name__ == "__main__":
    t = Training()
