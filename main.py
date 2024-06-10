#importing Password manager. hashlib is for encryption and getpass will hide our string
import hashlib 

#to prevent shoulder surfing
import getpass 

# import required module for encryption and file editing
from cryptography.fernet import Fernet
import csv


#dictionary to store key value pairs of username and password
password_manager = {}

#import usernames and passwords from a csv file as "masterList"
with open("passwords.csv", "r") as f:
    fieldnames = ['username', 'password']
    reader = csv.DictReader(f, fieldnames=fieldnames)
    masterList = list(reader)

#Reads the stored username and password frpm login.csv
with open('login.csv', 'r') as login_stuff:
    headers = ['username', 'password']
    reader1 = csv.DictReader(login_stuff, fieldnames=headers)
    master_login = list(reader1)

loginCreds = master_login[0]


    
    


#function to log into an existing user account
def login(): 
    
    username = input("enter your username: ")
    password = getpass.getpass("enter your password: ")
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    if username == loginCreds['username'] and loginCreds['password'] == hashed_password:
        print("Login successful!")
        secondary_loop()
    else:
        print("Invalid username or password.")

#what the code does when sucessfully logged on
def secondary_loop():
     while True:
        choice = input("press 0 to log out, 1 to lookup a password, 2 to add a new password, or 3 for executive controls ")
        if choice == "0":
            break;
        if choice == "1":
            user = input("enter the username for the corrosponding password you would like to lookup ")
            password_lookup(user)
        if choice =="2":
             NewUsername = input("enter a new username ")
             NewPassword = getpass.getpass("enter a new password ")
             add_password(NewUsername, NewPassword)
        if choice =="3":
             setup()
             

#this function looks up the password based off of a username inputed in the secondary loop
def password_lookup(user):
     for userPair in masterList:
        #print(userPair['username'])
        if userPair['username'] == user:
            print(userPair['password'])

def add_password(NewUsername, NewPassword):
    credsDict =   {"user":NewUsername, "password":NewPassword}
    # opens file and appends new credintials to it
    with open('passwords.csv', mode='a') as csvfile:
        fieldnames = ['user', 'password']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writerow(credsDict)
    print("Restart application to see updated changes")

        
def setup():
    a = input("press 1 to make a new key, press 2 to update your credintials")
    if a =="1":
        create_key()
    if a =="2":
        update_creds()

    

def create_key():
    # key generation
    key = Fernet.generate_key()

# string the key in a file
    with open('filekey.key', 'wb') as filekey:
	    filekey.write(key)

#reading key from keyfile
with open('filekey.key', 'rb') as filekey:
	key = filekey.read()
     
# opening the original file to encrypt it
with open('passwords.csv', 'rb') as file:
	original = file.read()

# using the key from key file
fernet = Fernet(key)
#updates the value of original incase changes have been made since start of program

def encrypt():
    # encrypting the file
    encryptedFunc = fernet.encrypt(original)

    # opening the file in write mode and 
    # writing the encrypted data
    with open('passwords.csv', 'wb') as encrypted_file:
	    encrypted_file.write(encryptedFunc)
         


#decrypt starts here
#opening the encrypted file

fernet = Fernet(key)

with open('passwords.csv', 'rb') as enc_file:
	encrypted_password = enc_file.read()



def decrypt():
#decrypting the file
    print("WARNING! You will lose any changes since you've logged in, RESTART APPLICATION AFTERDECRYPTING    ")
    decrypted = fernet.decrypt(encrypted_password)

    # opening the file in write mode and
    # writing the decrypted data
    with open('passwords.csv', 'wb') as dec_file:
	    dec_file.write(decrypted)

        
#function that creates a user account
def update_creds():
        creds = {}
        username = input ("Enter your desired username: ")
        password = getpass.getpass("Enter your desired password: ")
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        creds[username] = hashed_password 

        with open('login.csv', 'w') as csv_file:  
            writer = csv.writer(csv_file)
            for key, value in creds.items():
                writer.writerow([key, value])
        

#calls the encrypt or decrypt function
def cryptography_loop():
    choice = input("enter 1 to encrypt, or 2 to decrypt")
    if choice =="1":
        encrypt()
    if choice =="2":
         decrypt()



          
         
#main loop
def main():
    while True:
            choice = input("Enter 1 to login, 2 to encrypt/decrypt or 0 to exit: ")
            if choice =="1":
                 login()  
            elif choice =="2":
                 cryptography_loop()
                 break
            elif choice == "0":
                 print("REMEMBER TO ENCRYPT YOUR PASSWORD FILE!!!!")
                 break;
            else:
                 print("Invalid format, pick an option from the list")

#statement to order functions and to be used in futrure livbraries 
if __name__ == "__main__":
    main()
