import threading
import time
import Settings as s
import Excel
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
        say('lets start')
        time.sleep(2)
        print("Training: finish waving")
        self.training_session()

    def training_session(self):
        print ("Training: start exercises")
        exercise_names = ["raise_arms_horizontally", "bend_elbows", "raise_arms_bend_elbows"]
        for e in exercise_names:
            self.run_exercise(e)
            time.sleep(1)

        s.stop = True
        Excel.close_workbook()
        print("TRAINING DONE")

    def run_exercise(self, name):
        print("TRAINING: Exercise ", name, " start")
        s.req_exercise = name
        say(name)
        while s.req_exercise == name:
            time.sleep(0.00000001)  # Prevents the MP to stuck
        print("TRAINING: Exercise ", name, " done")


if __name__ == "__main__":
    t = Training()
