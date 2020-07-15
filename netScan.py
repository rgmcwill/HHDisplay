import nmap
from device import device
from trace import Tracer

def rangeToRange(aRange):
    ranges = aRange.split('-')
    return list(range(int(ranges[0]), int(ranges[1])))

def getRoute(address):
    t = Tracer(address)
    return t.run()

def getAllClientsOnRoute(listOfIPs):
    allUpIPs = []
    for i in listOfIPs:
        print("Checking " + i + "/24")
        nm.scan(hosts= i + "/24", arguments='-sP') #gets all clients connected on specific network
        for j in nm.all_hosts():
            allUpIPs.append(device('',j))
    return allUpIPs

def getPortsFromAddressList(listofIPs):
    allPorts = {}
    for ip in listofIPs:
        nm.scan(hosts=ip.address, arguments='-sT')
        if len(nm[ip.address].all_protocols()) > 0:
            allPorts.update({ip.address: list(nm[ip.address]['tcp'].keys())})
    return allPorts

def getBaseSegmentIP(ip):
    character = '.'
    splitIP = ip.split(character)
    shortendSplitIP = splitIP[:-1]
    return character.join(shortendSplitIP)


def getIPsAtCurrentLevel(listOfAllDNSIPs, routedIpAddresss, curIP):
    badIPs = []
    for i in listOfAllDNSIPs:
        if getBaseSegmentIP(i) == getBaseSegmentIP(curIP):
            if routedIpAddresss.count(i) < 0:
                badIPs.append(i)
    return badIPs

global nm
nm = nmap.PortScanner()

baseAddress = '192.168.3.1'
routedIpAddresss = getRoute(baseAddress)
allIPs = getAllClientsOnRoute(routedIpAddresss)

print("Done getting live clients")

allIpPorts = getPortsFromAddressList(allIPs)

print('All devices with DNS server')

allIPsWithPort = []

for device in allIpPorts:
    if allIpPorts.get(device).count(53) != 0:
        allIPsWithPort.append(device)

import netifaces as ni

curIP = ni.ifaddresses('enp5s0')[ni.AF_INET][0]['addr']

print("Correct IP addesses")
print(list(set(allIPsWithPort)-set(getIPsAtCurrentLevel(allIPsWithPort, routedIpAddresss, curIP))))

# for address in nm.all_hosts():
#      if len(nm[address].all_protocols()) > 0:
#              nm[address]['tcp'].keys()
