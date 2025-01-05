# README for SYN Port Scanner

## Overview

This document describes a Python-based SYN Port Scanner developed using the `scapy` library. The program performs a SYN scan to identify open ports on a target IP address, detect associated services, and retrieve service banners for analysis.

---

## Features

1. **SYN Scan:**
   - Sends TCP SYN packets to a range of ports on the target IP address.
   - Analyzes responses to determine the state of the ports:
     - **Open** (responds with SYN-ACK).
     - **Closed** (responds with RST).
     - **Filtered** (no response).

2. **Service Detection:**
   - Maps common port numbers to service names using:
     - `/etc/services` (if available on the system).
     - A hardcoded dictionary for common ports.

3. **Banner Grabbing:**
   - Attempts to retrieve banners from services on open ports.
   - Sends HTTP requests to ports 80 and 443 for additional data.

4. **Error Handling:**
   - Handles invalid inputs and errors gracefully.
   - Displays port status clearly in the output.

---

## Command-Line Arguments

1. **Target IP**: The IP address to scan.
2. **Port Low**: Starting port number for the scan.
3. **Port High**: Ending port number for the scan.

---

## Usage

Run the program with `sudo` to ensure sufficient privileges for sending raw packets.

```bash
sudo python syn_scanner.py <target_ip> <port_low> <port_high>
```

### Example

```bash
sudo python syn_scanner.py 192.168.1.1 20 100
```

---

## Output Format

The scanner produces output in the following format:

```
tcp/<port> | <state> | <service_name> | <banner>
```

- `<port>`: The scanned port number.
- `<state>`: Indicates if the port is `open`, `closed`, or `filtered`.
- `<service_name>`: The detected service name (e.g., HTTP, SSH, etc.).
- `<banner>`: Retrieved service banner or "Unknown version" if unavailable.

### Example Output

```
tcp/22   | open   | ssh      | OpenSSH_8.2p1 Ubuntu-4ubuntu0.5
tcp/80   | open   | http     | Apache/2.4.41 (Ubuntu)
tcp/443  | open   | https    | Unknown version
tcp/8080 | filtered
```

---

## Functions

### `syn_scan(target_ip, port_range)`
Performs the SYN scan on the target IP within the specified port range.

### `get_service_name(port)`
Returns the service name associated with a port number by checking:
- `/etc/services` (if available).
- A predefined dictionary for common services.

### `get_banner(target_ip, port)`
Attempts to connect to an open port and retrieve the service banner.

---

## Prerequisites

- **Python 3.x**
- **Scapy library**: Install using `pip install scapy`.

---

## Limitations

- Requires administrative privileges to send raw packets.
- Output depends on the target system's firewall and security settings.
- Some banners may not be retrieved due to server restrictions or timeouts.

---

## Disclaimer

This program is intended for educational purposes only. Unauthorized scanning of networks you do not own or have explicit permission to test is illegal and unethical.

---

## Author

Hamza Tarar