#                                               
#   IPBEJA: ESTIG                               
#   MESI 22/23                                  
#   Linguagens de Programacao Dinamica     
#   Titulo: Exercicios Python                   
#   Autor: David Henriques (23697)            
#                      
#                                              

import os
import time

# Clear Screen Windows/Linux
def clearScreen():
    os.system('cls' if os.name=='nt' else 'clear')

def mainMenu():
    mainChoice = ""
    #subChoice = ""

    # Menu
    while mainChoice.lower() != "x":
        clearScreen()
        print("IPBEJA: ESTIG")
        print("MESI 22/23")
        print("Linguagens de Programacao Dinamica")
        print("Titulo: Trabalho Individual - Aplicacao de Seguranca Informatica")
        print("Autores: David Henriques (23697)")
        print("")
        print("Hacking Tool for Dummies 3000")
        print("")
        print("1: Portscaner")
        print("2: Flooder")
        print("3: Logs")
        print("4: Instant Message")
        print("5: Reports")
        print("")
        print("Press X to Exit")
        print("")
        mainChoice = input("Please enter your choice ")
        
        match mainChoice.lower():
            
            # Portscaner
            case "1":  
                print("")

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
    