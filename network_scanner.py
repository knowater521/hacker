import scapy.all as scapy
import argparse

def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--target", dest="target", help="Target IP / IP range")
    options = parser.parse_args()
    return options

def scan(ip):
    arp_request = scapy.ARP(pdst=ip)
    #arp_request.show()
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    #broadcast.show()
    arp_request_broadcast = broadcast/arp_request
    answer_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]
    
    clients_list = []
    for element in answer_list:
        client_dict = {"ip":element[1].psrc, "mac":element[1].hwsrc}
        clients_list.append(client_dict)
        #print(element[1].psrc+"\t"+element[1].hwsrc)
    return clients_list

def print_result(results_list):
    print(("{:^10}\t{:^20}\n"+'-'*35).format("IP", "MAC Address"))
    for client in results_list:
        print(client['ip']+"\t"+client['mac'])

options = get_arguments()
#print(options, type(options))
scan_result = scan(options.target)
print_result(scan_result)
