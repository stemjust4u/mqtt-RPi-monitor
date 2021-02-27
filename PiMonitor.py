from MpiMonitor import PiMonitor
from time import sleep

pi1 = PiMonitor("temp-log.txt")
while True:
    cpuTemp = pi1.get_temp()
    pi1.update_log(cpuTemp)
    sleep(5)