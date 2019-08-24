import  subprocess
import random
import optparse
import re

def get_arguments():
    #create instance
    parser = optparse.OptionParser()
    parser.add_option("-i", "--interface", dest="interface",
 		help="Interface to change its MAC address")

    return parser.parse_args()

def change_mac(interface):
    subprocess.call(["ifconfig", interface, "down"])
    subprocess.call(["ifconfig", interface, "hw", "ether", addr])
    subprocess.call(["ifconfig", interface, "up"])
    subprocess.call(["ifconfig", interface])
def get_current_mac(interface):
    ifconfig_result = subprocess.check_output(["ifconfig",interface]).decode('utf-8')
    mac_address_search_result = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w",  ifconfig_result)
    try:
        return mac_address_search_result.group(0)
    except:
        print('[-] Could not read MAC address')


#interface = input("Interface>")
options, arguments = get_arguments()

mac = get_current_mac(options.interface)
addr = "{}:"*5+"{}"
addr = addr.format(*(random.randint(10,99) for i in range(6)))
#mac地址第二位ishu一定是偶数
addr = addr[0]+str(random.randint(0,4)*2)+addr[2:]
print("[+] change the wlan0 mac from "+str(mac)+" to "+addr)
change_mac(options.interface)
