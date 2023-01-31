class Portscan:

    def portScan(self, ip, r1, r2):

        import socket
        import sys
        from datetime import datetime

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

#UDP FLOOD
#SYN FLOOD