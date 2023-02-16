import socket
import sys
from datetime import datetime
import subprocess

class Portscan:

    def singlePortScan(self, ip, r1, r2):

        print("\nScanner is working on ", ip)
        t1 = datetime.now()
        try:
            for port in range(r1, r2):
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                socket.setdefaulttimeout(1)
                result = sock.connect_ex((ip, port))
                if result == 0:
                    print("Port Open:\t", port)
                sock.close()
        except KeyboardInterrupt:
            print("You stopped this")
            sys.exit()
        except socket.gaierror:
            print("Hostname could not be resolved")
            sys.exit()
        except socket.error:
            print("Could not connect to server")
            sys.exit()
        t2 = datetime.now()
        total = t2 - t1
        print("Scanning complete in ", total)

    # PortScan from multiple IP Addresses 
    def multiplePortScan(self, ipList, r1, r2):
        i = 0
        print(ipList)
        t1 = datetime.now()
        try:
            for x in ipList:
                print("\nScanner is working on ", ipList[i])
                
                for port in range(r1, r2):
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    socket.setdefaulttimeout(1)
                    result = sock.connect_ex((ipList[i], port))
                    print("Testing Port", port)
                    if result == 0:
                        print("Port Open:\t", port)
                    sock.close()
                i = i + 1

        except KeyboardInterrupt:
            print("You stopped this")
            sys.exit()
        except socket.gaierror:
            print("Hostname could not be resolved")
            sys.exit()
        except socket.error:
            print("Could not connect to server")
            sys.exit()
        t2 = datetime.now()
        total = t2 - t1
        print("\nScanning complete in ", total)        
        input()
        
    # PortScan from a Range of IP Addresses   
#UDP FLOOD
#SYN FLOOD

class IM:

    def server(self):
        print("Server started")
        subprocess.call('start cmd /k python scripts/server.py', shell=True)

    def client(self):
        print("New Client Launched")
        subprocess.call('start cmd /k python scripts/client.py', shell=True)

