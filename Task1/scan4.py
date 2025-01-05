from scapy.all import *
import sys
import time
from scapy.layers.inet import IP, TCP

conf.iface = "en0"


###### USAGE
# sudo python scan4.py <ip> <portLo> <portHi>


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
                    service_name = get_service_name(port)  # Get service name
                    banner = get_banner(target_ip, port)  # Get banner
                    print(f"{f'tcp/{port}':<6}| open | {service_name:<6} | {banner}")
                    # Send RST to close the connection
                    rst_packet = IP(dst=target_ip) / TCP(dport=port, flags="R")
                    send(rst_packet, verbose=0)
                elif response.getlayer(TCP).flags == 0x14:  # RST flag
                    ctr = ctr + 1
        else:
            print(f"tcp/{port}\t\tfiltered")
    print("closed ports ", ctr)


def get_service_name(port):
    """
    Gets the common service name associated with a port number.

    Args:
        port: The port number.

    Returns:
        The service name as a string, or "unknown" if not found.
    """
    try:
        # /etc/services is a common file mapping services to ports on Linux
        # This only works on systems with this file present, usually Unix-like.
        with open("/etc/services", "r") as f:
            for line in f:
                if line.strip().startswith("#"):  # Ignore comment lines
                    continue
                parts = line.split()
                if len(parts) >= 2:
                    service_port = parts[1].split("/")[0]
                    if not service_port.isdigit():
                        continue  # Skip lines where port is not a number
                    if int(service_port) == port:
                        return parts[0]

    except FileNotFoundError:
        pass

    # Fallback: use a basic dictionary
    common_services = {
        20: "ftp-data",
        21: "ftp",
        22: "ssh",
        23: "telnet",
        25: "smtp",
        53: "domain",
        80: "http",
        110: "pop3",
        143: "imap",
        443: "https",
        465: "smtps",
        587: "submission",
        993: "imaps",
        995: "pop3s",
        3306: "mysql",
        3389: "ms-wbt-server",
        5432: "postgresql",
        5900: "vnc",
        8080: "http-proxy",
    }
    return common_services.get(port, "unknown")


def get_banner(target_ip, port):
    """
    Attempts to connect to a port and retrieve the service banner.

    Args:
        target_ip: The target IP address.
        port: The target port number.

    Returns:
        The service banner as a string, or "Unknown version" if not retrievable.
    """
    try:
        # Create a socket and connect to the target IP and port
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(2)  # Set timeout for the connection
            s.connect((target_ip, port))

            # If the port is 80 or 443 (HTTP/HTTPS), send an HTTP request
            if port in (80, 443):
                http_request = "HEAD / HTTP/1.1\r\nHost: {}\r\n\r\n".format(target_ip)
                s.send(http_request.encode())

            # Try to receive data from the port
            banner = s.recv(1024).decode("utf-8", errors="ignore").strip()
            return banner if banner else "Unknown version"
    except Exception as e:
        return "Unknown version"


if __name__ == "__main__":
    # Define target IP and port range
    target_ip = sys.argv[1]
    port_low = int(sys.argv[2])
    port_high = int(sys.argv[3])
    port_range = range(port_low, port_high + 1)
    print(f"Starting SYN scan on {target_ip}")
    syn_scan(target_ip, port_range)
