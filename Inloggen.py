import mysql.connector
from mysql.connector import Error
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from getpass import getpass
from cryptography.fernet import Fernet

options = Options()
options.add_argument('--headless')
options.add_argument('--disable-gpu')

def create_db_connection(host_name, user_name, user_password, db_name):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password,
            database=db_name
        )
        print("MySQL Database connection successful")
    except Error as err:
        print(f"Error: '{err}'")

    return connection
def execute_query(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        print("Query successful")
    except Error as err:
        print(f"Error: '{err}'")
def call_key():
    return open("pass.key", "rb").read()
def inloggen(id,pw):
    global driver
    driver = webdriver.Firefox(options=options)
    global error
    print("Magister openen...")
    driver.get("https://corderius.magister.net")
        
    error = 0
    print("Gebruikersnaam invullen...")
    while True:
        try:
            driver.find_element_by_xpath("/html/body/div/div[1]/div[2]/div/form/div[2]/div/input").send_keys(id)
            driver.find_element_by_xpath("/html/body/div/div[1]/div[2]/div/form/div[3]/button").click()
            break
        except:
            error += 1
            if error >= 2500:
                break
    
    error = 0
    print("Wachtwoord invullen...")
    while True:
        try:
            driver.find_element_by_xpath("/html/body/div/form[1]/div/div/div[2]/div[1]/div/div/div/div/div/div[3]/div/div[2]/div/div[2]/div/div[2]/input").send_keys(pw)
            driver.find_element_by_xpath("/html/body/div/form[1]/div/div/div[2]/div[1]/div/div/div/div/div/div[3]/div/div[2]/div/div[3]/div[2]/div/div/div/div/input").click()
            break
        except:
            error += 1
            if error >= 2500:
                break
    
    error = 0
    print("Inloggen...")
    while True:
        try:
            driver.find_element_by_xpath("/html/body/div/form/div/div/div[1]/div[2]/div/div[2]/div/div[3]/div[2]/div/div/div[2]/input").click()
        except:
            error += 1
            if error >= 2500:
                break

    error = 0
    while True:
        try:
            try:
                driver.find_element_by_xpath("/html/body/div[3]/div[2]/mg-reminder-dialog/ng-container/div/div/button[1]").click()
                driver.find_element_by_xpath("/html/body/div[1]/div[4]/nav/div[1]/ul/li[4]/a").click()
                break
            except:
                driver.find_element_by_xpath("/html/body/div[1]/div[4]/nav/div[1]/ul/li[4]/a").click()
                break
        except:
            error += 1
            if error >= 2500:
                break
        
    error = 0
    while True:
        try:
            driver.find_element_by_xpath("/html/body/div[1]/div[5]/div/section/div/div[2]/div/div/table/tbody/tr[1]")
            return True
            break
        except:
            error += 1
            if error >= 2500:
                break


connection = create_db_connection('localhost',username,password,database)

Username = input("Gebruikersnaam: ")
Password = getpass("Wachtwoord: ")
Mail = input("E-mail: ")
print("Dit mag leeg gelaten worden")
discordId = input("Discord id: ")
key = call_key()
b = Fernet(key)
encryptedPw = b.encrypt(Password.encode())

insertGebruiker = """
INSERT INTO `gebruikers` (`gebruikerId`, `gebruikerPw`, `gebruikerMail`, `discordId`) VALUES ('""" + Username + """','""" + encryptedPw.decode() + """','""" + Mail + """','""" + discordId + """')
"""

if inloggen(Username,Password) == True:
    execute_query(connection,insertGebruiker)
    driver.close()
    print('Gelukt')
else:
    print('Gebruikersnaam of wachtwoord fout')