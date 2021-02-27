from vcgencmd import Vcgencmd
from time import sleep, strftime, time
from os import path
from pathlib import Path

class PiMonitor():                                       # Pi Monitor object
    def __init__(self, logFile):
    # Initialize
        self.logDir = path.dirname(__file__)             # Setup log file
        self.logFile = logFile
        Path(path.join(self.logDir, self.logFile)).touch(exist_ok = True)
        self.vcgm = Vcgencmd()                           # Create vcgm object

    # Update log with date and temperature
    def update_log(self, temp):
        with open(path.join(self.logDir, self.logFile), "a") as log:
            log.write("{0},{1}\n".format(strftime("%Y-%m-%d %H:%M:%S"),str(temp)))

    # Get temperature using vcgm
    def get_temp(self):
        temp = self.vcgm.measure_temp()
        return temp

# Main Loop
if __name__ == "__main__":
    pi1 = PiMonitor("temp-log.txt")          # Create pi monitor object and pass the name of our log file
    while True:                              # Main loop
        cpuTemp = pi1.get_temp()             # Get the temperature
        pi1.update_log(cpuTemp)              # Call update_log function
        sleep(5)                           
