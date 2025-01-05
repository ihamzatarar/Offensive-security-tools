from scapy.all import *
import random
import sys
import time

###### USAGE
# sudo python scan3.py <ip> <portLo> <portHi>

def syn_scan(target_ip, port_range):
    ctr = 0
    cur_time = time.time()
    print("[+] Scanning started at ", time.ctime(cur_time))
    for port in port_range:
        # Create SYN packet
        syn_packet = IP(dst=target_ip) / TCP(dport=port, flags="S")
        # Send SYN packet and wait for a response
        # sr1 is used to send packet and receive the response
        response = sr1(syn_packet, timeout=1, verbose=0)
        # Analyze the response
        if response:
            if response.haslayer(TCP):
                if response.getlayer(TCP).flags == 0x12:  # SYN-ACK flag
                    print(f"{f'tcp/{port}':<12}open")
                    # Send RST to close the connection
                    rst_packet = IP(dst=target_ip) / TCP(dport=port, flags="R")
                    send(rst_packet, verbose=0)
                elif response.getlayer(TCP).flags == 0x14:  # RST flag
                    ctr = ctr + 1
        else:
            print(f"tcp/{port}\t\tfiltered")
    print("closed ports ", ctr)

if __name__ == "__main__":
    # Define target IP and port range
    target_ip = sys.argv[1]
    port_low = int(sys.argv[2])
    port_high = int(sys.argv[3])
    port_range = range(port_low, port_high)  # Ports range
    print(f"Starting SYN scan on {target_ip}")
    syn_scan(target_ip, port_range)
