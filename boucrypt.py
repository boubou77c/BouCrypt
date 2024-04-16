from cryptography.fernet import Fernet
import time
import os
from rich import print as rprint,progress
from rich.progress import track
from art import tprint

#Function to read file
def read_file(file) -> bytes:
    try:
        with open(file,"rb") as f:
            file_content = f.read()
        return file_content
    except Exception as e:
        print(f"ReadFileError : {e}")
        return None

#Function to write file
def write_file(file,new_content) -> bytes:
    try:
        with open(file, "wb") as f:
            file_content = f.write(new_content)
        return file_content
    except Exception as e:
        print(f"WriteFileError : {e}")
        return None

#Function to search the file if it is not in the same folder as the program
def search_file(file_name:str) -> str :
    try:
        print("Searching the file...")
        #Start to search
        pc_start = os.path.join(os.path.expanduser("C:\\"))
        #Search through the storage
        for root, dir, files in os.walk(pc_start):
            if file_name in files:
                abs_path_file = os.path.join(root, file_name)
                break
                # Loop to confirm if the path is correct
        rprint(f"[bright_yellow]{abs_path_file}[/bright_yellow]")

        while (True):
            # input answer
            confirm_path_input = str(input("\nIt is the path to your file ? (y/n)\n> "))
            # The path is correct :
            if (confirm_path_input.lower() == "y"):
                rprint("[green]yes[/green]")
                return abs_path_file
            # The pas is not correct :
            elif (confirm_path_input.lower() == "n"):
                rprint("[red]No.[/red]")
                print("Sorry , we didn't find the file. Try to put the file path.")
                return None
            # The input is different from y/n (retry)
            else:
                print("Enter a correct answer. (y/n)\n")
    except Exception as e:
        print(f"ErrorSearchFile: {e}")
        time.sleep(4)
        return None

#Function to create a key
def create_key() -> bool:
    try:
        os.system("cls" if os.name == "nt" else "clear")
        #print("Generating a key...")
        key = Fernet.generate_key()
        for _ in track(range(100), description="[green]Generating a key"):
            time.sleep(0.02)
        if(key):
            time.sleep(2)
            print("Saving the key in a txt file...")
            write_file("Key BouCrypt.txt", key)
            if (write_file("Key BouCrypt.txt", key)):
                time.sleep(1)
                rprint("The key has been created and saved successfully\n"
                      f"[underline]Path[/underline] : [red]{os.path.abspath('Key BouCrypt.txt')}[/red]")
                time.sleep(4)
                return True
    except Exception as e:
        print(f"KeyGenerationError: {e}")
        time.sleep(4)
        return False



def encrypt_file() -> bool:
    try:
        #Clear the terminal
        os.system("cls" if os.name == "nt" else "clear")
        #Key input
        key = input("Enter the key : ")
        fernet = Fernet(key)
        #File to encrypt
        file = input("Which file do you want to encrypt ? (don't forget the type ! ex: .txt...) : ")
        # Check if the file exist
        file_exist = os.path.isfile(file)
        # Else find it through the storage
        if (file_exist is False):
            file = search_file(file)
            if (file is None):
                return False
        # Read the file
        original_file = read_file(file)
        # Encrypt the file
        encrypted_file = fernet.encrypt(original_file)
        # Write the encrypted file
        write_file(file, encrypted_file)
        print(f"{file} has been encrypted successfully")
        time.sleep(4)
        return True
    #Error management -> Show the exception
    except Exception as e:
        print(f"Error: {e}")
        time.sleep(4)
        return False


def decrypt_file() -> bool:
    try:
        os.system("cls" if os.name == "nt" else "clear")
        #Key input
        key = input("Enter the key : ")
        fernet = Fernet(key)
        #File to decrypt input
        file = input("Which file do you want to decrypt ? : ")
        file_exist = os.path.isfile(file)
        #Search file if is False
        if (file_exist is False):
            file = search_file(file)
            if (file is False):
                return False
        #Read the file
        encrypted_file = read_file(file)
        #Decrypt the file
        file_decrypt = fernet.decrypt(encrypted_file)
        #Write the decrypted file
        write_file(file, file_decrypt)
        print(f"{file} has been decrypted successfully")
        time.sleep(4)
        return True
    except Exception as e:
        print(f"Error: {e}")
        time.sleep(4)
        return False



while (True):
    os.system("cls" if os.name == "nt" else "clear")
    #Choice input
    tprint("BouCrypt")
    rprint("[bold underline]Press number to do an action :[/bold underline]\n"
          "[purple]1-Generate key[/purple]\n"
          "[blue]2-Encrypt a file[/blue]\n"
          "[yellow]3-Decrypt a file[/yellow]\n"
          "[red]4-Leave the program[/red]\n")
    try:
        choice = int(input("> "))
        if (choice == 1): create_key()
        elif (choice == 2): encrypt_file()
        elif (choice == 3): decrypt_file()
        elif (choice == 4): break
    except:
        print("Please enter a number between 1-4")
        time.sleep(1)
