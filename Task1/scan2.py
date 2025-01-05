from scapy.all import Ether, ARP, srp, conf
import sys
import time
###usage
# python scan1.py eth0 <ip_range to scan>
###
def arp_scan(iface,ip_range):
    print("[+] Scanning ",ip_range)
    cur_time = time.time()
    print("[+] Scanning started at ",time.ctime(cur_time))
    #from here on we start sending packets
    conf.verb = 0
    broadcast = "ff:ff:ff:ff:ff:ff"
    ether_layer = Ether(dst=broadcast)
    arp_layer = ARP(pdst=ip_range)
    packet = ether_layer / arp_layer
    print(packet.show())
if __name__ == "__main__":
    iface = sys.argv[1]
    ip_range = sys.argv[2]
    arp_scan(iface,ip_range)