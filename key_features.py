import csv
import statistics
import pandas as pd

shifted = {'1': '!', '2': '@', '3': '#', 'a': 'A', 'b': 'B', 'c': 'C', 'p': 'P'}
unshifted = dict([reversed(i) for i in shifted.items()])


def not_a_typo(key_pressed, key_released):
    pressed_key = key_pressed != 'None' and 'Key.' in key_pressed or key_pressed in shifted.keys() or key_pressed in unshifted.keys()
    released_key = key_released != 'None' and 'Key.' in key_released or key_released in shifted.keys() or key_released in unshifted.keys()
    return pressed_key or released_key


def parse_key_file():
    key_pressed_dict = {}
    last_pressed_time = 0
    # This is the new file containing the calculated features
    new_filename = 'new_key_feature_data.csv'
    features = '3.csv'
    shift_is_pressed = False
    # This is the file with 3 columns
    filename = 'example.csv'

    total_time_taken = 0
    hold_times = []
    cpr_times = []
    released_times = []
    pressed_times = []
    Time = []
    Key_released = []
    Key_pressed = []


    with open(filename) as csv_file:
        csv_reader = csv.DictReader(csv_file)
        rows = list(csv_reader)
        for i, row in enumerate(rows):
            row = rows[i]
            key_pressed = row['Key pressed']
            key_released = row['Key released'].replace("'", "")
            time = row['Time']
            Time.append(time)
            Key_released.append(key_released)
            Key_pressed.append(key_pressed)

            hold_time = ''
            press_release = ''
            released_key_time = ''
            pressed_key_time = ''

            # Key press event
            if not_a_typo(key_pressed, key_released):
                if key_pressed != 'None' and 'Key.' in key_pressed or key_pressed in shifted.keys() or key_pressed in unshifted.keys():
                    last_pressed_time = time
                    pressed_key_time = float(time)
                    key_pressed_dict[key_pressed] = float(time)
                    if key_pressed == 'Key.shift':
                        shift_is_pressed = True
                # Key Release event
                elif key_released != 'None':
                    check_for_key = key_released
                    released_key_time = float(time)
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

                    # Time between last press and current release
                    press_release = float(time) - float(last_pressed_time)

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

                if hold_time:
                    hold_times.append(hold_time)

                if press_release:
                    cpr_times.append(press_release)

                if pressed_key_time:
                    pressed_times.append(pressed_key_time)

                if released_key_time:
                    released_times.append(released_key_time)

                # Total time taken to type 10 words
                if i == len(rows) - 1:
                    total_time_taken = time
                print(total_time_taken)

                # new_row = [key_pressed, key_released, time, hold_time, press_release]
                # new_rows.append(new_row)

    release_latency = [released_times[i + 1] - released_times[i] for i in range(len(released_times) - 1)]
    press_latency = [pressed_times[i + 1] - pressed_times[i] for i in range(len(pressed_times) - 1)]

    # Average/Max/Min hold times
    avg_hold_time, max_hold_time, min_hold_time = statistics.mean(hold_times), max(hold_times), min(hold_times)
    # Average/Max/Min consecutive press release times
    avg_cpr_time, max_cpr_time, min_cpr_time = statistics.mean(cpr_times), max(cpr_times), min(cpr_times)
    # Average/Max/Min release latency (upup) times
    avg_released_time, max_released_time, min_released_time = statistics.mean(release_latency), max(
        release_latency), min(release_latency)
    # Average/Max/Min press latency (downdown) times
    avg_press_time, max_press_time, min_press_time = statistics.mean(press_latency), max(press_latency), min(
        press_latency)

    # Row with the feature headers that are written to new CSV
    header = ['Total time taken', 'Average hold time', 'Max hold time', 'Min hold time', 'Average CPR time',
              'Max CPR time', 'Min CPR time', 'Average Release Latency', 'Max Release Latency', 'Min Release Latency',
              'Average Press Latency', 'Max Press Latency', 'Min Press Latency']
    #header2 = ['Time','Key Released', 'Key Pressed', 'Hold Time','Consecutive press and release', 'Press Latency','Release Latency']
    #feature_row2 = zip(Time, Key_pressed, Key_released, hold_times, cpr_times,pressed_times, released_times)
    # Values of the features that are written to new CSV
    feature_row = [total_time_taken, avg_hold_time, max_hold_time, min_hold_time, avg_cpr_time, max_cpr_time, min_cpr_time,
                   avg_released_time, max_released_time, min_released_time, avg_press_time, max_press_time, min_press_time]


    with open(new_filename, 'w') as file:
        writer = csv.writer(file)
        writer.writerow(header)
        writer.writerow(feature_row)
    new_file = {'Time': Time,'Key Pressed' : Key_pressed, 'Key Released' : Key_released, 'Hold Time': hold_times,'Consecutive Press and Release': cpr_times, 'Press Latency': pressed_times, 'Release Latency': released_times}
    df = pd.DataFrame.from_dict(new_file, orient='index')
    df = df.transpose()
    df.to_csv('3.csv')

    print('done')


def extract_key_features():
    parse_key_file()
extract_key_features()
