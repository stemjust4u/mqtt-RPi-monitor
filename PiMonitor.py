from pitempOOP import PiTemp
from time import sleep

pi1 = PiTemp("temp-log.txt")
while True:
    cpuTemp = pi1.get_temp()
    pi1.update_log(cpuTemp)
    sleep(1)