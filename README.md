# SYN Flooding
Tool for SYN-Flooding attack

## Disclaimer
This tool is designed for educational purposes only, i do not support the use for any illegal activities.
## Requirements
**Install Scapy**
```
pip install --pre scapy[basic]
```
## Usage
**Example**
```
python3 syn_flooding.py 192.168.2.1 -p 80 -a 10000
```
will send 10000 packets to 192.168.2.1:80
