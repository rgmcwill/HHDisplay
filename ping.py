import pprint, operator, sys, signal
import matplotlib.pyplot as plt
from device import device
from datetime import datetime
from time import sleep
from pythonping import ping

class que:
    def __init__(self, size):
        self.size = size
        self.l = []

    def print(self):
        return self.l

    def avg(self):
        return sum(self.l) / len(self.l)

    def add(self, val):
        toReturn = None
        if len(self.l) <= self.size - 1:
            self.l.append(val)
        else:
            toReturn = self.l[0]
            del self.l[0]
            self.l.append(val)
        return toReturn

class pingedDevice:
    def __init__(self, name, address, file):
        self.aDevice = device(name, address)
        self.pings = que(30)
        self.file = file

    def addPing(self, ping):
        self.pings.add(ping)
        timeStamp = datetime.now()

        self.file.write(str(timeStamp) + " | " + self.aDevice.name + " " + str(ping) + "\n")

def signal_handler(sig, frame):
    print("Closing files and exiting program")
    file.close()
    sys.exit(0)

def main():
    global file 
    file = open("log.txt", "a")

    devices = [
        pingedDevice("McWilliams", "192.168.1.1", file),
        pingedDevice("EnGenius2", "192.168.3.6", file),
        pingedDevice("EnGenius1", "192.168.3.5", file),
        pingedDevice("DoorRouter", "192.168.3.4", file),
        pingedDevice("JetPack", "192.168.3.1", file),
    ]

    queueSize = 30

    count = 1000

    for i in range(count):
        sleep(5)
        for d in devices:
            curPing = ping(d.aDevice.address, count=1).rtt_avg_ms
            d.addPing(curPing)
            print(d.aDevice.name + " AVG: " + str(round(d.pings.avg(), 3)) + " CUR: " + str(curPing))
        print('-----------------------')

    file.close()

signal.signal(signal.SIGINT, signal_handler)
print('Press Ctrl+C')

main()

signal.pause()
