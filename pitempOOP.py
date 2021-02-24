from vcgencmd import Vcgencmd
from time import sleep, strftime, time
from os import path
from pathlib import Path

class PiTemp():
    def __init__(self, logFile):
        # Initialize
        self.logDir = path.dirname(__file__)
        self.logFile = logFile
        Path(path.join(self.logDir, self.logFile)).touch(exist_ok = True)
        self.vcgm = Vcgencmd()

    # Update log
    def update_log(self, temp):
        with open(path.join(self.logDir, self.logFile), "a") as log:
            log.write("{0},{1}\n".format(strftime("%Y-%m-%d %H:%M:%S"),str(temp)))

    # Get temperature
    def get_temp(self):
        temp = self.vcgm.measure_temp()
        return temp

# Main Loop
if __name__ == "__main__":
    pi1 = PiTemp("temp-log.txt")
    while True:
        cpuTemp = pi1.get_temp()
        pi1.update_log(cpuTemp)
        sleep(1)