import csv
import pandas as pd

shifted = {'1': '!', '2': '@', '3': '#', 'a': 'A', 'b': 'B', 'c': 'C', 'p': 'P'}
unshifted = dict([reversed(i) for i in shifted.items()])

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

            def not_a_typo(key_pressed, key_released):
                pressed_key = key_pressed != 'None' and 'Key.' in key_pressed or key_pressed in shifted.keys() or key_pressed in unshifted.keys()
                released_key = key_released != 'None' and 'Key.' in key_released or key_released in shifted.keys() or key_released in unshifted.keys()
                return pressed_key or released_key

            #parsekeyfile starts here
            key_pressed_dict = {}
            last_pressed_time = 0
            # for up_up variable
            last_released_time = 0
            second_last_released_time = 0
            new_rows = []
            shift_is_pressed = False

            with open(filename, mode='r')as f:
                reader = csv.DictReader(f)
                rows = list(reader)
                for i, row in enumerate(rows):
                    row = rows[i]
                    time  = row["Time"]
                    Time.append(time)
                    key_pressed = row["Key pressed"]
                    Key_pressed.append(key_pressed)
                    key_released = row["Key released"]
                    Key_released.append(key_released)

                    if not_a_typo(key_pressed, key_released):
                        if key_pressed != 'None' and 'Key.' in key_pressed or key_pressed in shifted.keys() or key_pressed in unshifted.keys():
                            last_pressed_time = time
                            key_pressed_dict[key_pressed] = float(time)
                            if key_pressed == 'Key.shift':
                                shift_is_pressed = True
                        # Key Release event
                        elif key_released != 'None':
                            check_for_key = key_released
                            # Key released is uppercase or symbol
                            if shift_is_pressed:
                                # It was typed as uppercase
                                if key_released in key_pressed_dict.keys():
                                    check_for_key = key_released
                                # It was typed as lowercase
                                else:
                                    check_for_key = unshifted[key_released]
                            # Key released is lowercase or number
                            else:
                                # It was typed as lowercase
                                if key_released in key_pressed_dict.keys():
                                    check_for_key = key_released
                                # It was typed as uppercase
                                else:
                                    check_for_key = shifted[key_released]

                            # Check when this key was pressed
                            press_time = key_pressed_dict[check_for_key]
                            hold_time = float(time) - float(press_time)
                            Hold_time.append(hold_time)
                            print(len(hold_time))

                            # Time between last press and current release
                            press_release = float(time) - float(last_pressed_time)
                            CPR.append(press_release)

                            if key_released == 'Key.shift':
                                shift_is_pressed = False

                            if 'Key.' not in key_released:
                                if key_released in shifted.keys():
                                    # Lowercase release: delete the uppercase entry
                                    opposite_key = shifted[key_released]
                                    key_pressed_dict.pop(opposite_key, None)
                                else:
                                    # Uppercase release: delete lowercase entry
                                    opposite_key = unshifted[key_released]
                                    key_pressed_dict.pop(opposite_key, None)

                            # Delete entry from dictionary
                            key_pressed_dict.pop(key_released, None)
                    #parsekeyfile ends here

                    
                    if (key_pressed != 'None'):
                        Pressed.append(key_pressed)
                        press_time.append(time)
                    if (key_released != 'None') :
                        Released.append(key_released)
                        release_time.append(time)

                released_time_float = [float(i) for i in release_time]
                release_latency =  [released_time_float[i+1]-released_time_float[i] for i in range(len(released_time_float)-1)]
                print(len(Key_pressed))
                pressed_time_float = [float(i) for i in press_time]
                press_latency =  [pressed_time_float[i+1]-pressed_time_float[i] for i in range(len(pressed_time_float)-1)]
                maximum_released_time = max(released_time_float)
                maximum_pressed_time = max(pressed_time_float)
                maximum_upup_time = max(press_latency)
                maximum_downdown_time = max(release_latency)
                print(maximum_upup_time)
                print(maximum_downdown_time)


            new_file = {'Time': Time,'Key Pressed' : Key_pressed, 'Key Released' : Key_released, 'Hold Time': Hold_time,'Consecutive Press and Release': CPR, 'Press Latency': press_latency, 'Release Latency': release_latency}
            df = pd.DataFrame.from_dict(new_file, orient='index')
            df = df.transpose()
            df.to_csv('3.csv')
read_file("2.csv")
