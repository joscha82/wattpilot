import wattpilot
from time import sleep
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("ip", help = "IP of Wattpilot Device")
parser.add_argument("password", help = "Password of Wattpilot")


args = parser.parse_args()

ip = args.ip
password = args.password


solarwatt = wattpilot.Wattpilot(ip,password)
solarwatt.connect()

c=0
while not solarwatt.connected and c<10:
    sleep(1)
    c=c+1

##Print Status
print(solarwatt)

##Update arbitary property
#solarwatt.send_update("cae",False) 

## Set output power
#solarwatt.set_power(16)

## Set Mode to Eco
#solarwatt.set_mode(wattpilot.LoadMode.ECO)



