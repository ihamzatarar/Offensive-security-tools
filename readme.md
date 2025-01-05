# SYN Port Scanner


---

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

# Brute Force Automation Tasks

## Overview

This document describes two Python programs designed for automating brute force attacks against login forms. These tasks include:

1. **Basic Brute Force Attack**: Attempts to guess passwords by submitting combinations of usernames and passwords.
2. **Advanced Brute Force Attack for DVWA**: Incorporates cookies to handle DVWA's session-based security while brute-forcing.

---

## Task 1: Basic Brute Force Attack

### Description

This program performs a brute force attack against a login form by attempting multiple username-password combinations and identifying valid credentials.

### Features

- Accepts inputs via command-line arguments.
- Gracefully handles invalid inputs and errors.
- Detects and reports successful login attempts.

### Command-Line Arguments

1. **URL**: Target URL of the login form.
2. **Username**: Username to test.
3. **Password File**: File containing potential passwords (one password per line).
4. **Failure String**: Text returned by the server when login fails.

### Usage

```bash
python brute_force.py <url> <username> <password_file> <failure_string>
```

### Example

```bash
python Task-1.py http://10.211.55.5/dvwa/login.php admin passwords.txt "Login failed"
```

---

## Task 2: Brute Force Attack for DVWA

### Description

This program extends the basic brute force functionality to support the Damn Vulnerable Web Application (DVWA) brute force page by utilizing cookies for session-based authentication.

### Features

- Supports cookies for maintaining session integrity.
- Handles DVWA's security mechanism.
- Gracefully exits on invalid inputs.

### Command-Line Arguments

1. **URL**: Target URL of the DVWA brute force page.
2. **Username**: Username to test.
3. **Password File**: File containing potential passwords (one password per line).
4. **Failure String**: Text returned by the server when login fails.
5. **Cookies** _(Optional)_: Session cookies in the format `key=value; key2=value2`.

### Usage

```bash
python dvwa_brute_force.py <url> <username> <password_file> <failure_string> [cookies]
```

### Example

```bash
python Task-2.py http://10.211.55.5/dvwa/vulnerabilities/brute/ admin passwords.txt "Username and/or password incorrect" "security=high; PHPSESSID=3269347b8be5684e7daa389e1382afc3"
```

### Notes

- Use a tool like Burp Suite's Proxy tab to extract session cookies for DVWA.
- If cookies are not required, pass an empty string as the fifth argument.

---

## Password File

Create a file named `passwords.txt` with potential passwords, one per line. For example:

```
password1
123456
admin
welcome
```

---

## Error Handling

- The programs handle invalid file paths, malformed inputs, and unexpected server responses.
- In case of invalid inputs, the program exits gracefully with an error message.

---

## Prerequisites

- Python 3.x
- `requests` library: Install using `pip install requests`.

---

## Disclaimer

These programs are intended for educational purposes only. Unauthorized use of these scripts against systems you do not own or have explicit permission to test is illegal and unethical.

---

## Author

Hamza Tarar

