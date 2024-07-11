#!/usr/bin/env python3
import subprocess
import re
import time
import sys


def run_chronyc_tracking():
    try:
        # Run the 'chronyc tracking' command and capture the output
        result = subprocess.run(['chronyc', 'tracking'], capture_output=True, text=True, check=True)

        # Return the standard output (stdout) of the command as a string
        return result.stdout
    except subprocess.CalledProcessError as e:
        # If there was an error running the command, print the error message
        print(f"Error running 'chronyc tracking': {e}")
        return None

def save_output_to_file(output, filename):
    try:
        # Save the output to a file
        with open(filename, 'a+') as file:
            pattern = r'Reference ID    : (\w*\d*).*System time     : (\d*.\d*) seconds (.*) of NTP time.*Last offset     : ([+-]?\d*.\d*).*'
            results = re.search(pattern, "".join(output.split("\n")))
            if results[3] == "slow":
              file.write('\n')
              file.write("{},-{},{}".format(results[1], results[2], results[4]))
            else:
              file.write('\n')
              file.write("{},+{},{}".format(results[1], results[2], results[4]))
            file.close()
    except Exception as e:
        print(f"Error saving output to file: {e}")

def run_back(duration, turn):
    for i in range(turn):
        output = run_chronyc_tracking()
        if output:
            save_output_to_file(output, 'Time_diff.txt')
        time.sleep(duration)

# if __name__ == "__main__":
    # Run chronyc tracking and store the output
    # output = run_chronyc_tracking()
duration = sys.argv[1]
turn = sys.argv[2]
run_back(float(duration), int(turn))
