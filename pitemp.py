from vcgencmd import Vcgencmd
from time import sleep, strftime, time
from os import path
from pathlib import Path

# Initialize
vcgm = Vcgencmd()
logDir = path.dirname(__file__)
logFile = "temp-log.txt"
Path(path.join(logDir, logFile)).touch(exist_ok = True)

# Main Loop
while True:
    cpuTemp = vcgm.measure_temp()
    with open(path.join(logDir, logFile), "a") as log:
        log.write("{0},{1}\n".format(strftime("%Y-%m-%d %H:%M:%S"),str(cpuTemp)))
    sleep(1)