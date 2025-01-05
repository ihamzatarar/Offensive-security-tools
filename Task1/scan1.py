from scapy.all import Ether, ARP, srp, conf
import sys
import time
###usage
####
# python scan1.py eth0 <ip address or ip_range to scan>
def arp_scan(iface,ip_range):
    print("[+] Scanning ",ip_range)
    cur_time = time.time()
    print("[+] Scanning started at ",time.ctime(cur_time))

if __name__ == "__main__":
    iface = sys.argv[1]
    ip_range = sys.argv[2]
    arp_scan(iface,ip_range)