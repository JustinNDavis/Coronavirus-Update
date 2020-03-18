#Author: Justin Davis
#Date: 3/17/2020
#Purpose - the purpose of this program is to scrape the web for information and numbers related to the Coronavirus and send them in an email to avoid manually checking every day

#imports libraries
import smtplib
import requests 
from bs4 import BeautifulSoup
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def PrepareMessage():
    #opens file and for writing (deletes previous text file)
    file = open("message.txt", "w")
    file.write("Good morning Justin, here are the latest totals for Coronavirus: \n\n")
    file.close()

#this functions scrapes the new counts from worldometers
def TotalCount():

    #opens file and creates variable
    file = open("message.txt", "a")

    result = requests.get("https://www.worldometers.info/coronavirus/")
    src = result.content
    soup = BeautifulSoup(src, "lxml")

    #lists for the numbers beings stored
    numbers = []

    for div_tag in soup.find_all("div", {"class" : "maincounter-number"}):
        span_tag = div_tag.find_all("span")
        numbers.append([span.get_text() for span in span_tag])
    
    #adding context to numbers
    numbers[0] = "Coronavirus cases: " + str(numbers[0])
    numbers[1] = "Deaths: " + str(numbers[1])
    numbers[2] = "Recovered: " + str(numbers[2])

    #writes Items
    for item in numbers:
        file.write(item + "\n")
    file.close()

#This function shows the number of affected countries and the new counts for each country each day
def CountryDetails():
    #opens file and creates variable
    file = open("message.txt", "a")

    #goes to the coronavirus #countries section
    result = requests.get("https://www.worldometers.info/coronavirus/#countries")
    src = result.content
    soup = BeautifulSoup(src, "lxml")

    #lists for the numbers beings stored
    numbers = []

    #works the same as it does in TotalCount
    td_tag = soup.find("td", {"style" : "background-color:#FFEEAA; color:#000;"})
    numbers.append("New cases globally: " + str([td_tag.text]))
    td_tag2 = soup.find("td", {"style" : "background-color:red; color:#fff"})
    numbers.append("New deaths: " + str([td_tag2.text]))
    
    for item in numbers:
        file.write(str(item) + '\n')

    file.write("\nContinue to wash your hands!")
    file.close()

def PrepareEmail():

    #assistance provided through Arjun Krishna Babu on freeCodeCamp
    #CONSTANTS
    MY_ADDRESS = "Name@somewhere.com"
    PASSWORD = "notMyREalP@SSworD!!"

    #logs in
    s = smtplib.SMTP(host="smtp-mail.outlook.com", port = 587)
    s.starttls()
    s.login(MY_ADDRESS, PASSWORD)

    file = open("message.txt", "r")

    #creates a message
    msg = file.read()
    file.close()
    #creates a Mime Multipart message object
    message = MIMEMultipart()

    #updates the from, to, and subject lines in the message
    message['From'] = MY_ADDRESS
    message['To'] = MY_ADDRESS
    message['Subject'] = "Coronavirus Update"

    message.attach(MIMEText(msg, "plain"))
    s.send_message(message)

    #terminates the SMPT session
    s.quit()

def main():
    PrepareMessage()
    TotalCount()
    CountryDetails()
    PrepareEmail()

main()