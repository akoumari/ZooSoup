# Import requests (to download the page)
import requests

# Import BeautifulSoup (to parse what we download)
from bs4 import BeautifulSoup

# Import Time (to add a delay between the times the scape runs)
import time

# Import smtplib (to allow us to email)
import smtplib

# Import OS to clear terminal for clean aesthetic 
import os

# Import Regex to check email format
import re 

# Import Get Pass to hide password input from terminal
import getpass

def check(email):  
    regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
    # pass the regular expression 
    # and the string in search() method 
    if(re.search(regex,email)):  
        print("\t" + email + " is a valid email address")
        return True  
          
    else:  
        print("\t" + email + " is an invalid email address")
        return False  

# This function counts how many times a string appears on the page and returns the count
def extract(key, input): 
    count=0
    substr = re.search(key,input) 
    while substr!=None:  
        count=count+1
          
        input = input[(substr.end()-1):] 
        substr = re.search(key,input) 
    return (count) 


os.system('cls')

print("\t\t\t\t\t**********************************")
print("\t\t\t\t\t***  Welcome to Zoo Soup V1.0  ***")
print("\t\t\t\t\t**********************************")
print("\tThis program will scan the Toronto Zoo Website\n\tto see if the Scenic Safari tickets are still sold out!\n\n\n")
# set the default 'from' address,
fromaddr = 'ibmwax@gmail.com'
# set the default 'to' addresses,
toaddrs  = 'alex.koumarianos@gmail.com'
# set the default password 
passfile = "C:\\Users\\alexk\\Desktop\\superdupersecretfile.txt"
with open(passfile, 'r', encoding='utf-8') as pwf:
        password = str(pwf.readline())
# Checks counter 
numChecks = 0
mins = 15
config = ""


# Allow user to change defaults 
while True:
    if config == "n" or config == "no":
        break
    config = input('\tDo you need to enter sender and receiver? y/n ').lower()
    if config =="y" or config == "yes":
        # set the 'from' address,
        isValid = False
        while isValid == False:
            fromaddr = input("\tPlease enter sender address: ")
            isValid = check(fromaddr)
        password = getpass.getpass("\tPlease enter sender password: \n\t*If you are using Gmail you need to have 2-factor auth and a randomly generated app password\n\t")
        # set the 'to' addresses,
        isValid = False
        while isValid == False:
            toaddrs  = input("\tPlease enter receiver address: ")
            isValid = check(toaddrs)
        # Change the check interval and check for valid interval 1 min - 12 hours 
        while True:
            try:
                mins  = int(input("\tPlease enter custome period for checks in mins(Numbers 1 - 720 no decimals): "))
                if mins < 1 or mins > 720:
                    print("Please enter a value within range. If unsure of best range we recommend 15")
                    continue
            except ValueError:
                print("Please enter a NUMERIC NON-DECIMAL value. If unsure what to enter we recommend 15")
            else:
                break
        config = "no"
        
   
        

while True:
    # set the url to be scraped
    url = "https://www.canadapost.ca/trackweb/en#/details/7286247000163091"
    # set the headers like we are a browser,
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    # download the page
    response = requests.get(url, headers=headers)
    # parse the downloaded page and grab all text, then,
    soup = BeautifulSoup(response.text, "lxml")
    # set the various search keys
    key3 = "Item out for delivery"
    key2 = "Item processed"
    key1 = "<p style=\"color:red; text-align:center; font-size:125%; font-weight:bold;\">\r\n    Scenic Safari tickets are now SOLD OUT\r\n<!--  \r\n  <span style=\"font-size:75%;\">\r\n  <br />\(Tickets for June 15, 19, 20 & 21 are now Sold Out\)\r\n  </span>\r\n-->"
    
    # set the search parameters for specific count values/ranges
    if extract(key3, str(soup)) >= 1 or extract(key2, str(soup)) >= 1:
        #  or extract(key3, str(soup)) >= 1 :
        msg = 'Subject: The eagle has taken off'
        # setup the email server,
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        # add account login name and password,
        server.login(fromaddr, password)
        
        # Print the email's contents
        print('From: ' + fromaddr)
        print('To: ' + str(toaddrs))
        print('Message: ' + msg)
        
        # send the email
        server.sendmail(fromaddr, toaddrs, msg)
        # disconnect from the server
        server.quit()
        
        break
    # If key trigger value/ranges were not matched the user is notified that another check will be run in 15 mins and a count of checks + countdown timer is displayed  
    else:
        numChecks = numChecks + 1
        sec = mins*60
        for i in range(sec):
            os.system('cls')
            print("\t\t\t\t\t**********************************")
            print("\t\t\t\t\t***  Welcome to Zoo Soup V1.0  ***")
            print("\t\t\t\t\t**********************************")
            print("\tThis program will scan the Toronto Zoo Website\n\tto see if the Scenic Safari tickets are still sold out!\n\n")
            print("\tUpdates will be sent from", fromaddr, "to", toaddrs,"\n\n")
            print("\tNothing to report yet Master Overlord... Don\'t worry I\'m still on it! Let\'s check again in 15 mins.\n\tNumber of checks:",numChecks)
            print("")
            print("\tMinutes left till next check: "+ str(sec//60) +":" + str(sec%60))
            sec = sec - 1
            time.sleep(1)
        # continue with the script,
        continue