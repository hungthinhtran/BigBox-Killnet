# BigBox-Killnet
# This tool can use for cutting down the Internet of the target that is in the same network as you
# Usage:

1. Network scanner (see targets in the same network)

   python3 BigBox-Killnet.py -i <IP range>
   
   Ex: python3 BigBox-Killnet.py -i 192.168.1.0/24

2. Turn ON or OFF network killer mode
   
   python3 BigBox-Killnet.py -s <0 or 1>
  
   Ex: python3 BigBox-Killnet.py -s 0
  
   0: turn on network killer mode
   
   1: turn off network killer mode

3. Kill network
   
   python3 Killnet.py -t <target's IPv4> -m <target's MAC> -M <router's MAC> -r <router's IPv4>
   
   Ex: python3 Killnet.py -t 192.168.1.167 -m 28:d0:ea:ca:7c:d6 -M c0:94:ad:df:ed:a0 -r 192.168.1.1
   
4. One turn kill command 
   
   python3 Killnet.py -s 0 -t <target's IPv4> -m <target's MAC> -M <router's MAC> -r <router's IPv4>
