from os import path
from pathlib import Path
import csv

# Initialize
logDir = path.dirname(__file__)
iFile = "input.txt"
oFile = "output.txt"
Path(path.join(logDir, oFile)).touch(exist_ok = True)

with open(path.join(logDir, oFile), "w") as outfile:
    with open(path.join(logDir, iFile), "r") as infile:
        reader = csv.reader(infile)
        for row in reader:
            for x in range(int(row[1])):
                outfile.write("{0}\n".format(row[0]))
                print(row[0])