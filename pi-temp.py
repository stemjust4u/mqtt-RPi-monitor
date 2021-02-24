from vcgencmd import Vcgencmd

vcgm = Vcgencmd()
cpuTemp=vcgm.measure_temp()
print(cpuTemp)