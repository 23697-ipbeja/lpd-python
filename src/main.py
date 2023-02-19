#                                               
#   IPBEJA: ESTIG                               
#   MESI 22/23                                  
#   Linguagens de Programacao Dinamica     
#   Titulo: Trabalho Individual - Aplicacao de Seguranca Informatica                 
#   Autor: David Henriques (23697)            
#                      
#                                              

import os, time, ipaddress, getpass, sqlite3
from Crypto.Hash import SHA512
from scripts.classes import Portscan, IM, files, flood, logs, UserPortal

# Init Clasess
P = Portscan()
Fl = flood()
l = logs()
I = IM()
F = files()
UP = UserPortal()


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
        #print (SHA512.new(b'qwerty').hexdigest())
        username = input('Username: ')
        password = getpass.getpass('Password: ').encode()
        password = SHA512.new(password).hexdigest()

        conn = sqlite3.connect('./db/mainDB.db')
        rows = conn.execute("SELECT * FROM Users WHERE username = ?", (username,)).fetchall()

        for row in rows:
            roleRows = conn.execute("SELECT * FROM Roles WHERE id = ?", (row[3],)).fetchall()
            if password == row[4]:
                clearScreen()
                print(f"\nWelcome {username.upper()}!")
                for roleRow in roleRows:
                    userRole = roleRow[1]
                conn.close()
                time.sleep(2)
                mainMenu(username, userRole)

                

            else:
                print("\nWrong Password, try again!\n")
                time.sleep(2)


def mainMenu(user, role):
    mainChoice = ""
    subChoice = ""
    userLogged = user
    userRole = role

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
        print(f"\nLogged User: {userLogged}")
        print(f"Role: {userRole}\n")
        print("1: Portscaner")
        print("2: Flooder")
        print("3: Logs")
        print("4: Instant Message")
        print("5: File Encryption")
        print("6: User Portal")
        print("7: Change User\n")
        print("Press X to Exit\n")
        mainChoice = input("Please enter your choice ")
        match mainChoice.lower():
            
            # Portscaner
            case "1":  

                # SubMenu PortScaner

                # Checks if user is Administrator
                if role != "Administrator":
                    print("Access denied!")
                    time.sleep(3)
                    mainMenu(userLogged, userRole)
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
                            try:
                                ip = input("\nEnter the remote host IP to scan: ")
                                r1 = int(input("Enter the start port number: "))
                                r2 = int(input("Enter the last port number: "))
                                P.singlePortScan(ip, r1, r2)
                                time.sleep(5)  
                            except:
                                print("\nInternal Error")
                                time.sleep(2)
                                break


                        # Multiple Portscan
                        case "2": 
                            ipList = []
                            tempIp = ""
                            print("\nTool to scan multiple remote host IP addresses")
                            try:
                                while tempIp != "x": 
                                    tempIp = input("\nEnter the remote host IP to scan or press X to exit: ")
                                    tempIp = tempIp.lower()

                                    # Validates if Input is an IP Address
                                    if validate_ipv4_address(tempIp):
                                        print("Gotcha!")

                                        # Adds IP to the list
                                        ipList.append(tempIp)
                                    elif tempIp == "x":
                                        break
                                    else:
                                        print("Invalid IP address, try again.")
                                    
                                r1 = int(input("\nEnter the start port number: "))
                                r2 = int(input("\nEnter the last port number: "))
                                P.multiplePortScan(ipList, r1, r2)
                            except:
                                print("\nInternal Error")
                                time.sleep(2)
                                break

                        # Exit Menu    
                        case "x":
                            break
                        
                        # Wrong Option
                        case _:
                            print("Opcao Invalida ")
                            time.sleep(2)  
            
            # Flooder
            case "2": 
                if role != "Administrator":
                    print("Access denied!")
                    time.sleep(3)
                    mainMenu(userLogged, userRole)
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
                            clearScreen()
                            print("UDP Flooder")
                            print("\nTool to send multiple UDP packets to remote IP address")
                            try:
                                ip = input('Target IP: ') #The IP we are attacking
                                port = int(input('Target Port: ')) #The Port we are attacking
                                num = int(input('Number of packets: ')) #The Number of packets
                                Fl.udpFlood(ip, port, num)
                            except:
                                print("\nInternal Error")
                                time.sleep(2)
                                break

                        # Syn Flood   
                        case "2":
                            clearScreen()
                            print("\nSYN Flooder")
                            print("\nTool to send multiple SYN packets to remote IP address (CTRL+C to Stop))")
                            try:
                                ip = input('Target IP: ') #The IP we are attacking
                                port = int(input('Target Port: ')) #The Port we are attacking
                                Fl.synFlood(ip, port)
                                time.sleep(3)
                            except:
                                print("\nInternal Error")
                                time.sleep(2)
                                break

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
                    print("2: SSH Failed Logins")
                    print("\nPress X to Exit\n")
                    subChoice = input("Please enter your choice ")
                
                    match subChoice.lower():
                        
                        # Mikrotik Logs
                        case "1":  
                            print("Mikrotik Logs")
                            print("Reading from File ./logs/ufw.log")
                            time.sleep(2)
                            l.readMikrotik()


                        # SSH  
                        case "2":
                            print("SSH Logs")
                            print("Reading from File ./logs/auth.log")
                            time.sleep(2)
                            l.readSSHLogs()

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
                            I.server()
                            time.sleep(3)

                        # Launch Clients    
                        case "2":
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
                            
                            print("\nFiles in folder /export/\n")
                            F.listFiles()
                            
                            # Get the file name from the user
                            file_name = input("\nEnter file name to encrypt: ")
                            key = getpass.getpass("Enter encryptiom key: ")
                            with open('./export/' + file_name, 'rb') as in_file, open('./export/' + file_name + '_enc', 'wb') as out_file:
                                F.encrypt(in_file, out_file, key)
                            # Removes old File after encryption
                            os.remove('./export/' + file_name)
                            print(f"\nThe {file_name} has been encrypted ")
                            time.sleep(5)

                        # Select Decrypt    
                        case "2":
                            print("\nFiles in folder /export/\n")
                            F.listFiles()

                            # Get the file name from the user
                            file_name = input("\nEnter file name to decrypt: ")
                            key = getpass.getpass("Enter encryptiom key: ")
                            
                            with open('./export/' + file_name, 'rb') as in_file, open('./export/' + file_name.replace("_enc", "")  , 'wb') as out_file:
                                F.decrypt(in_file, out_file, key)
                            os.remove('./export/' + file_name)
                            print(f"\nThe {file_name}_enc has been decrypted ")
                            time.sleep(5)

                        # Exit Menu
                        case "x":
                            break
                        
                        case _:
                            print("Opcao Invalida ")
                            time.sleep(2)  

            # User Portal
            case "6":  
                if role != "Administrator":
                    print("Access denied!")
                    time.sleep(3)
                    mainMenu(userLogged, userRole)
                # SubMenu Logs
                while subChoice.lower() != "x":

                    clearScreen()
                    print("\nUser Portal\n")
                    print("1: List Users")
                    print("2: Create User")
                    print("3: Change User Password")
                    print("4: Delete User")                    
                    print("\nPress X to Exit\n")
                    subChoice = input("Please enter your choice ")
                                   
                    match subChoice.lower():

                        # List Users
                        case "1":  
                            clearScreen()
                            UP.listUsers()
                        # Create User 
                        case "2":
                            clearScreen()
                            UP.createUser()

                        # Change User Password
                        case "3":
                            clearScreen()
                            UP.updatePassword()

                        # Change User Password
                        case "4":
                            clearScreen()
                            UP.deleteUser()

                        # Exit Menu
                        case "x":
                            break
                        
                        case _:
                            print("Opcao Invalida ")
                            time.sleep(2)     

            # Change User
            case "7":
                loginScreen()

            # Exit
            case "x":
                print("\nThanks for Hacking with Us!\n")
                exit()

            # Wrong Input
            case _:
                print("Wrong Choice! ")
                time.sleep(2)

# Main
loginScreen()
    