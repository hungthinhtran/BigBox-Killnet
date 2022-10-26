# BigBox-Killnet
 ____  _       ____              _  ___ _ _            _   
| __ )(_) __ _| __ )  _____  __ | |/ (_) | |_ __   ___| |_ 
|  _ \| |/ _` |  _ \ / _ \ \/ / | ' /| | | | '_ \ / _ \ __|
| |_) | | (_| | |_) | (_) >  <  | . \| | | | | | |  __/ |_ 
|____/|_|\__, |____/ \___/_/\_\ |_|\_\_|_|_|_| |_|\___|\__|
         |___/                                           

# This tool can use for:
  + cutting down the Internet of the target that is in the same network as you
  + change your MAC address
  + cutting down the Internet of all devices in any router you want

# Require: 
   
   sudo python3 -m pip install subprocess.run
   
   sudo apt-get update
   
   sudo apt-get install python3-pip
   
   sudo python3 -m pip install --pre scapy[complete]
   
   sudo python3 -m pip install optparse-pretty
   
# Usage:

1. Network scanner (see targets in the same network)

   python3 BigBox-Killnet.py -I <IP_range>
   
   Ex: python3 BigBox-Killnet.py -i 192.168.1.0/24

2. Turn ON or OFF network killer mode
   
   python3 BigBox-Killnet.py -s <0 or 1>
  
   Ex: python3 BigBox-Killnet.py -s 0
  
   0: turn on network killer mode
   
   1: turn off network killer mode

3. Kill network
   
   python3 BigBox-Killnet.py -t <target's IPv4> -m <target's MAC> -M <router's MAC> -r <router's IPv4>
   
   Ex: python3 BigBox-Killnet.py -t 192.168.1.167 -m 28:d0:ea:ca:7c:d6 -M c0:94:ad:df:ed:a0 -r 192.168.1.1
   
4. One turn kill command 
   
   python3 BigBox-Killnet.py -s 0 -t <target's IPv4> -m <target's MAC> -M <router's MAC> -r <router's IPv4>

5. MAC changer
   
   python3 BigBox-Killnet.py -i <interface> -a <New MAC address>
   
6. Overkill mode
   
   python3 BigBox-Killnet.py -R <set time to Hunting the targets (second)>
   
   python3 BigBox-Killnet.py -O <Target's BSSID>
   
