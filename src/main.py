#                                               
#   IPBEJA: ESTIG                               
#   MESI 22/23                                  
#   Linguagens de Programacao Dinamica     
#   Titulo: Trabalho Individual - Aplicacao de Seguranca Informatica                 
#   Autor: David Henriques (23697)            
#                      
#                                              

import os
import time
import ipaddress
import getpass
import sqlite3
from Crypto.Hash import SHA512
from scripts.classes import Portscan, IM, files, flood


def validate_ipv4_address(address):
    try:
        ipaddress.IPv4Address(address)
        return True
    except ValueError:
        return False

# Clear Screen Windows/Linux
def clearScreen():
    os.system('cls' if os.name=='nt' else 'clear')

def loginScreen():
    clearScreen()
    

    while True:
        print("Please Login\n")
        #print (SHA512.new(b'1234').hexdigest())
        username = input('Username: ')
        password = getpass.getpass('Password: ').encode()
        password = SHA512.new(password).hexdigest()

        rows = sqlite3.connect('./db/mainDB.db').execute("SELECT * FROM Users WHERE username = ?", (username,)).fetchall()
        for row in rows:
            if password == row[4]:
                clearScreen()
                print(f"\n\n\nWelcome {username.upper()}!")
                time.sleep(3)
                mainMenu()
            else:
                print("\nWrong Password, try again!\n")
                time.sleep(2)

def mainMenu():
    mainChoice = ""
    subChoice = ""
    # Menu
    while mainChoice.lower() != "x":
        mainChoice = ""
        subChoice = ""
        clearScreen()
        print("IPBEJA: ESTIG")
        print("MESI 22/23")
        print("Linguagens de Programacao Dinamica")
        print("Titulo: Trabalho Individual - Aplicacao de Seguranca Informatica")
        print("Autor: David Henriques (23697)\n")
        print("Hacking Tools for Dummies 3000\n")
        print("1: Portscaner")
        print("2: Flooder")
        print("3: Logs")
        print("4: Instant Message")
        print("5: File Encryption")
        print("6: Reports")
        print("7: User Portal\n")
        print("Press X to Exit\n")
        mainChoice = input("Please enter your choice ")
        match mainChoice.lower():
            
            # Portscaner
            case "1":  

                # SubMenu PortScaner
                while subChoice.lower() != "x":
                    clearScreen()
                    print("\nPortScan Menu\n")
                    print("1: PortScan One Device")
                    print("2: PortScan Multiple Devices")
                    #print("3: PortScan Multiple Devices by Range\n")
                    print("\nPress X to Exit\n")
                    subChoice = input("Please enter your choice ")
                
                    match subChoice.lower():
                        
                        # Single Portscan
                        case "1":  
                            ip = input("\nEnter the remote host IP to scan: ")
                            r1 = int(input("Enter the start port number: "))
                            r2 = int(input("Enter the last port number: "))
                            P = Portscan()
                            P.portScan(ip, r1, r2)
                            time.sleep(5)  


                        # Multiple Portscan
                        case "2": 
                            ipList = []
                            tempIp = ""
                            print("\nTool to scan multiple remote host IP addresses")
                            while tempIp != "x": 
                                tempIp = input("\nEnter the remote host IP to scan or press X to exit: ")
                                tempIp = tempIp.lower()
                                if validate_ipv4_address(tempIp):
                                    print("Gotcha!")
                                    ipList.append(tempIp)
                                elif tempIp == "x":
                                    break
                                else:
                                    print("Invalid IP address, try again.")
                                   

                            r1 = int(input("\nEnter the start port number: "))
                            r2 = int(input("\nEnter the last port number: "))
                            P = Portscan()
                            P.multiplePortScan(ipList, r1, r2)
                        
                        # Exit Menu    
                        case "x":
                            break
                        
                        # Wrong Option
                        case _:
                            print("Opcao Invalida ")
                            time.sleep(2)  
            # Flooder
            case "2": 

                # SubMenu Flood
                while subChoice.lower() != "x":

                    clearScreen()
                    print("\nFlooding Menu\n")
                    print("1: UDP Flood")
                    print("2: SYN Flood")
                    print("\nPress X to Exit\n")
                    subChoice = input("Please enter your choice ")
                
                    match subChoice.lower():
                        
                        # UDP Flood
                        case "1":  
                            print("UDP Flooder")
                            print("\nTool to send multiple UDP packets to remote IP address")
                            Fl = flood()
                            ip = input('Target IP: ') #The IP we are attacking
                            port = int(input('Target Port: ')) #The Port we are attacking
                            Fl.udpFlood(ip, port)

                        # Syn Flood   
                        case "2":
                            print("\nSYN Flooder")
                            print("\nTool to send multiple SYN packets to remote IP address")
                            Fl = flood()
                            ip = input('Target IP: ') #The IP we are attacking
                            port = int(input('Target Port: ')) #The Port we are attacking
                            Fl.synFlood(ip, port)
                            time.sleep(3)

                        # Exit Menu
                        case "x":
                            break
                        
                        case _:
                            print("Opcao Invalida ")
                            time.sleep(2)  
           
            # Logs
            case "3": 
                # SubMenu Logs
                while subChoice.lower() != "x":

                    clearScreen()
                    print("\nLogs\n")
                    print("1: Mikrotik Logs")
                    print("2: SSH Logs")
                    print("\nPress X to Exit\n")
                    subChoice = input("Please enter your choice ")
                
                    match subChoice.lower():
                        
                        # Mikrotik Logs
                        case "1":  
                            print()

                        # SSH  
                        case "2":
                            print()

                        # Exit Menu
                        case "x":
                            break
                        
                        case _:
                            print("Opcao Invalida ")
                            time.sleep(2)     
                          
            # Instant Message
            case "4":

                # SubMenu Instant Message
                while subChoice.lower() != "x":

                    clearScreen()
                    print("\nInstant Message\n")
                    print("1: Launch Server")
                    print("2: Launch New Client")
                    print("\nPress X to Exit\n")
                    subChoice = input("Please enter your choice ")
                
                    match subChoice.lower():
                        
                        # Launch Server (Listening Connections)
                        case "1":  
                            I = IM()
                            I.server()
                            time.sleep(3)

                        # Launch Clients    
                        case "2":
                            I = IM()
                            I.client()
                            time.sleep(3)

                        # Exit Menu
                        case "x":
                            break
                        
                        case _:
                            print("Opcao Invalida ")
                            time.sleep(2)  

            # File Encryption
            case "5":  

                # SubMenu File Encryption
                while subChoice.lower() != "x":

                    clearScreen()
                    print("\nFile Encryption\n")
                    print("1: Encrypt File")
                    print("2: Decrypt File")
                    print("\nPress X to Exit\n")
                    subChoice = input("Please enter your choice ")
                
                    match subChoice.lower():

                        # Select Encrypt
                        case "1":  
                            F = files()
                            print("\nFiles in folder /logs/\n")
                            F.listFiles()
                            
                            # Get the file name from the user
                            file_name = input("\nEnter file name to encrypt: ")
                            key = input("Enter encryptiom key: ")

                            with open('./logs/' + file_name, 'rb') as in_file, open('./logs/' + file_name + '_enc', 'wb') as out_file:
                                F.encrypt(in_file, out_file, key)
                            os.remove('./logs/' + file_name)
                            print(f"\nThe {file_name} has been encrypted ")
                            time.sleep(5)

                        # Select Decrypt    
                        case "2":
                            F = files()
                            print("\nFiles in folder /logs/\n")
                            F.listFiles()

                            # Get the file name from the user
                            file_name = input("\nEnter file name to decrypt: ")
                            key = input("Enter encryptiom key: ")
                            
                            with open('./logs/' + file_name, 'rb') as in_file, open('./logs/' + file_name.replace("_enc", "")  , 'wb') as out_file:
                                F.decrypt(in_file, out_file, key)
                            os.remove('./logs/' + file_name)
                            print(f"\nThe {file_name}_enc has been decrypted ")
                            time.sleep(5)

                        # Exit Menu
                        case "x":
                            break
                        
                        case _:
                            print("Opcao Invalida ")
                            time.sleep(2)  

            # User Portal
            case "7":  

                # SubMenu Logs
                while subChoice.lower() != "x":

                    clearScreen()
                    print("User Portal\n")
                    print("1: Create User")
                    print("2: Edit User")
                    print("3: List Users")
                    print("\nPress X to Exit\n")
                    subChoice = input("Please enter your choice ")
                
                    match subChoice.lower():
                        
                        # Create User
                        case "1":  
                            print()

                        # Edit User 
                        case "2":
                            print()

                        # List Users
                        case "3":
                            print()

                        # Exit Menu
                        case "x":
                            break
                        
                        case _:
                            print("Opcao Invalida ")
                            time.sleep(2)     

            case "x":
                print("\nThanks for Hacking with Us!\n")
                break
            case _:
                print("Wrong Choice! ")
                time.sleep(2)


loginScreen()
    