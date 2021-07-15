import csv

global time
t = 0
def read_file(filename):
        with open(filename, mode='r')as f:
            reader = csv.DictReader(f)
            rows = list(reader)
            for i, row in enumerate(rows):
                time  = row["Time"]
                key_pressed = row["Key pressed"]
                key_released = row["Key released"]
                print(key_released)
            for key_released == Key.backspace
read_file("log.csv")
