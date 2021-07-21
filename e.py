import csv
import pandas as pd


def pre_process():
    file = "example.csv"
    df = pd.read_csv(file)
    no_enter_pressed = df[ df['Key pressed'] == "Key.enter"].index
    df.drop(no_enter_pressed, inplace =True)
    no_enter_released = df[ df['Key released'] == "Key.enter"].index
    df.drop(no_enter_released, inplace =True)
    df.to_csv("2.csv")

pre_process()

def read_file(filename):

            Time = []
            Key_released = []
            Key_pressed = []
            Hold_time = []
            CPR = []
            Pressed = []
            Released = []
            press_time = []
            release_time = []

            with open(filename, mode='r')as f:
                reader = csv.DictReader(f)
                rows = list(reader)
                for i, row in enumerate(rows):
                    time  = row["Time"]
                    Time.append(time)
                    key_pressed = row["Key pressed"]
                    Key_pressed.append(key_pressed)
                    key_released = row["Key released"]
                    Key_released.append(key_released)
                    hold_time = row["Hold Time"]
                    Hold_time.append(hold_time)
                    cpr = row["Consecutive Press Release"]
                    CPR.append(cpr)

                    if (key_pressed != 'None'):
                        Pressed.append(key_pressed)
                        press_time.append(time)
                    if (key_released != 'None') :
                        Released.append(key_released)
                        release_time.append(time)

                released_time_float = [float(i) for i in release_time]
                release_latency =  [released_time_float[i+1]-released_time_float[i] for i in range(len(released_time_float)-1)]
                print(len(release_latency))
                print(len(Key_pressed))
                pressed_time_float = [float(i) for i in press_time]
                press_latency =  [pressed_time_float[i+1]-pressed_time_float[i] for i in range(len(pressed_time_float)-1)]
                maximum_released_time = max(released_time_float)
                maximum_pressed_time = max(pressed_time_float)
                maximum_upup_time = max(press_latency)
                maximum_downdown_time = max(release_latency)
                print(maximum_upup_time)
                print(maximum_downdown_time)

            def create_new_file():
                with open('hello.csv', mode='w')as f:
                    writer = csv.writer(f)
                    writer.writerow(["Timestamp","Key Pressed", "Key Released", "Hold Time", "Consecutive Press and Release"])
                    rows = zip(Time,Key_pressed,Key_released,Hold_time,CPR)
                    writer.writerows(rows)
            create_new_file()
read_file("2.csv")
