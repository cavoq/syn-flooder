# SYN-Flooder

![license](https://img.shields.io/badge/license-MIT-brightgreen.svg)
![version](https://img.shields.io/badge/version-1.3.1-lightgrey.svg)

Tool for performing syn-flood attacks on a target.

## Disclaimer
**This tool is designed for educational purposes only, i do not support the use for any illegal activities.
Only use this on networks you own or have permission for.**

## Note

**Since this script uses scapy, it needs to have root privileges, if
you install it with pip, you need to install it with sudo.**

## Requirements

**System**
```bash
sudo apt update &&
sudo apt install python3-scapy ntp -y
```

## Installation

**PyPi**

```bash
sudo pip install syn-flooder
sudo syn-flooder
```

**From source**
```bash
pip install -r requirements.txt
sudo python3 syn_flooder.py
```

## Usage

```
SYN-Flooder Attack Tool for stress testing

positional arguments:
  target                Target IP address

options:
  -h, --help            show this help message and exit
  -a PACKETS_TO_SEND, --amount PACKETS_TO_SEND
                        Amount of packets (default are infinity)
  -v, --verbose         Increases logging
  -s TIME_LIMIT, --seconds TIME_LIMIT
                        Time limit for attack (default is 60 seconds)
  -t THREADS, --threads THREADS
                        Threads (default is 1)
  -p D_PORT, --port D_PORT
                        Destination Port (default is 80)
```

## Developer notes

**publish**
```bash
python3 setup.py sdist bdist_wheel
python3 -m twine upload --verbose dist/*
```
