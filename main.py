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
from classes.hackingTools import Portscan

def validate_ipv4_address(address):
    try:
        ipaddress.IPv4Address(address)
        return True
    except ValueError:
        return False

# Clear Screen Windows/Linux
def clearScreen():
    os.system('cls' if os.name=='nt' else 'clear')

def mainMenu():
    mainChoice = ""
    subChoice = ""

    # Menu
    while mainChoice.lower() != "x":
        clearScreen()
        print("IPBEJA: ESTIG")
        print("MESI 22/23")
        print("Linguagens de Programacao Dinamica")
        print("Titulo: Trabalho Individual - Aplicacao de Seguranca Informatica")
        print("Autor: David Henriques (23697)\n")
        print("fSociety - Hacking Tools for Dummies 3000\n")
        print("1: Portscaner")
        print("2: Flooder")
        print("3: Logs")
        print("4: Instant Message")
        print("5: Reports\n")
        print("Press X to Exit\n")
        mainChoice = input("Please enter your choice ")
        
        match mainChoice.lower():
            
            # Portscaner
            case "1":  

                # SubMenu
                while subChoice.lower() != "x":
                    clearScreen()
                    print("\nPortScan Menu\n")
                    print("1: PortScan One Device")
                    print("2: PortScan Multiple Devices")
                    print("3: PortScan Multiple Devices by Range\n")
                    print("Press X to Exit\n")
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
                        case "3": 
                            print("")
                            
                        case "x":
                            break
                        
                        case _:
                            print("Opcao Invalida ")
                            time.sleep(2)  
            # Flooder
            case "2": 
                print("")
           
            # Logs
            case "3": 
                print("")   
                          
            # Instant Message
            case "4": 
                print("")  

            # Reports
            case "5":  
                print("")

            case "x":
                print("\nThanks for Hacking with Us!\n")
                break
            case _:
                print("Wrong Choice! ")
                time.sleep(2)



mainMenu()
    