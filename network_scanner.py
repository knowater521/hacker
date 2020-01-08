import scapy.all as scapy
import argparse

def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--target", dest="target", help="Target IP / IP range")
    options = parser.parse_args()
    return options

def scan(ip,times=1):
    arp_request = scapy.ARP(pdst=ip)
    #arp_request.show()
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    #broadcast.show()
    arp_request_broadcast = broadcast/arp_request
    clients_dict = {}
    for _ in range(times):
        answer_list = scapy.srp(arp_request_broadcast, timeout=2, verbose=False)[0]
        for element in answer_list:
            clients_dict.update({element[1].psrc:element[1].hwsrc})
            #print(element[1].psrc+"\t"+element[1].hwsrc)
    return clients_dict

def print_result(results_list):
    print(("{:^10}\t{:^20}\n"+'-'*35).format("IP", "MAC Address"))
    for ip, mac in results_list.items():
        print(ip+"\t" + mac)

options = get_arguments()
#print(options, type(options))
scan_result = scan(options.target)
print_result(scan_result)
