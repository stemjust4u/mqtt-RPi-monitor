from vcgencmd import Vcgencmd
from time import sleep, strftime, time
from os import path
from pathlib import Path

# Initialize
logDir = path.dirname(__file__)
logFile = "temp-log.txt"
Path(path.join(logDir, logFile)).touch(exist_ok = True)
vcgm = Vcgencmd()

# Function to update log
def update_log(dirName, fileName, temp):
    with open(path.join(dirName, fileName), "a") as log:
        log.write("{0},{1}\n".format(strftime("%Y-%m-%d %H:%M:%S"),str(temp)))

# Main Loop
while True:
    cpuTemp = vcgm.measure_temp()
    update_log(logDir, logFile, cpuTemp)
    sleep(1)