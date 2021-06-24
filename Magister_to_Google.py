import mysql.connector
import smtplib
from mysql.connector import Error
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from cryptography.fernet import Fernet
from getpass import getpass
import time
import datetime

#de webdriver configureren
options = Options()
options.add_argument('--headless')
options.add_argument('--disable-gpu')
#https://www.freecodecamp.org/news/connect-python-with-sql/ (database codes)

#def voor het encrypten van de wachtwoorden
def genwrite_key():
    key = Fernet.generate_key()
    with open("pass.key", "wb") as key_file:
        key_file.write(key)
def call_key():
    return open("pass.key", "rb").read()

#de mailserver opstarten om mails te sturen
def smtpServer():
    global server
    server = smtplib.SMTP(host="smtp.gmail.com", 
                        port=587)
    ehlo_code, ehlo_message = server.ehlo()
    ehlo_message = ehlo_message.decode('utf-8')
    print(f'ehlo code: {ehlo_code}')
    print(f'ehlo boodschap: {ehlo_message}')
    tls_code, tls_boodschap = server.starttls()
    print(tls_code)
    global sender
    sender = 'nieuwcijfer@gmail.com'
    passwd = 'Corderiusgroep4'
    login_code, login_boodschap = server.login(sender, passwd)
    print(login_code)
    print(login_boodschap)

#def voor database connectie en voor lezen en schrijven.
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
def read_query(connection, query):
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except Error as err:
        print(f"Error: '{err}'")
connection = create_db_connection(host_name, user_name, user_password, db_name)

#het nieuwe cijfer vergelijken met het oude
def vergelijkCijfer():
    try:
        getIdCijfer = """
        SELECT idCijfer FROM Magister.""" + str(id) + """ WHERE
        vak='""" + laatsteCijfer[1] + """' AND
        datumInvoer='""" + laatsteCijfer[2] + """' AND
        omschrijving='""" + laatsteCijfer[3] + """' AND
        resultaat='""" + laatsteCijfer[4] + """' AND
        weegfactor='""" + laatsteCijfer[5] + """'
        """
        idCijfer = read_query(connection, getIdCijfer)
        idCijfer = idCijfer[0]
        idCijfer = idCijfer[0]
    except:
        print('Geen cijfer')

    smtpServer()
    to = mail
    aan = 'To:' + to
    subject = 'Subject: Nieuw cijfer'
    text = 'Nieuw cijfer: \n'

    try:
        if idCijfer > 1:
            while idCijfer > 1:
                idCijfer -= 1
                getCijfer = """
                SELECT * FROM Magister.""" + str(id) + """ WHERE idCijfer=""" + str(idCijfer)
                cijfer = read_query(connection, getCijfer)
                cijfer = cijfer[0]
                text = text + cijfer[1] + ' ' + cijfer[4] + '\n'
            body = '\n'.join([aan, subject, text])
            resultaat = server.sendmail(sender, [to], body)
            print(resultaat)
    except:
        print('Wijziging')
        getCijfer = """
        SELECT * FROM Magister.""" + str(id) + """ WHERE idCijfer=1
        """
        cijfer = read_query(connection, getCijfer)
        cijfer = cijfer[0]
        text = text + cijfer[1] + ' ' + cijfer[4]
        body = '\n'.join([aan, subject, text])
        resultaat = server.sendmail(sender, [to], body)
        print(resultaat)
#cijfers uit magister ophalen
def cijfersOphalen():
    for x in range(1,26):
        vak = driver.find_element_by_xpath("/html/body/div[1]/div[5]/div/section/div/div[2]/div/div/table/tbody/tr[" + str(x) + "]/td[1]").text
        datumInvoer = driver.find_element_by_xpath("/html/body/div[1]/div[5]/div/section/div/div[2]/div/div/table/tbody/tr[" + str(x) + "]/td[2]").text
        omschrijving = driver.find_element_by_xpath("/html/body/div[1]/div[5]/div/section/div/div[2]/div/div/table/tbody/tr[" + str(x) + "]/td[3]").text
        resultaat = driver.find_element_by_xpath("/html/body/div[1]/div[5]/div/section/div/div[2]/div/div/table/tbody/tr[" + str(x) + "]/td[4]").text
        weegfactor = driver.find_element_by_xpath("/html/body/div[1]/div[5]/div/section/div/div[2]/div/div/table/tbody/tr[" + str(x) + "]/td[5]").text

        if 'x' not in resultaat:
            tabelInvullen = """
            INSERT INTO `""" + str(id) + """` (`idCijfer`, `vak`, `datumInvoer`, `omschrijving`, `resultaat`, `weegfactor`) 
            VALUES ('""" + str(x) + """', '""" + vak + """', '""" + datumInvoer + """', '""" + omschrijving + """', '""" + resultaat + """', '""" + weegfactor + """')
            ON DUPLICATE KEY 
            UPDATE `vak` = '""" + vak + """', `datumInvoer` = '""" + datumInvoer + """', `omschrijving` = '""" + omschrijving + """', `resultaat` = '""" + resultaat + """', `weegfactor` = '""" + weegfactor + """'
            """

            execute_query(connection,tabelInvullen)
    driver.close()
#usertabel resetten om nieuwe cijfers in te voeren
def resetTabel():
    getLaatsteCijfer = """
    SELECT * FROM Magister.""" + str(id) + """ WHERE idCijfer=1
    """

    maakTabel = """
    CREATE TABLE `Magister`.`""" + str(id) + """` (
          `idCijfer` INT NOT NULL,
          `vak` VARCHAR(50) NOT NULL,
          `datumInvoer` VARCHAR(10) NOT NULL,
          `omschrijving` VARCHAR(50) NOT NULL,
          `resultaat` VARCHAR(10) NOT NULL,
          `weegfactor` VARCHAR(10) NOT NULL,
    PRIMARY KEY (`idCijfer`));
    """

    execute_query(connection,maakTabel)

    global laatsteCijfer
    laatsteCijfer = read_query(connection, getLaatsteCijfer)
    try:
        laatsteCijfer = laatsteCijfer[0]
    except:
        print('Geen cijfers')
    
# inloggen in magister
def inloggen():
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
            if error >= 1000:
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
            if error >= 1000:
                break
    
    error = 0
    print("Inloggen...")
    while True:
        try:
            driver.find_element_by_xpath("/html/body/div/form/div/div/div[1]/div[2]/div/div[2]/div/div[3]/div[2]/div/div/div[2]/input").click()
        except:
            error += 1
            if error >= 1000:
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
            if error >= 1000:
                break
        
    error = 0
    while True:
        try:
            driver.find_element_by_xpath("/html/body/div[1]/div[5]/div/section/div/div[2]/div/div/table/tbody/tr[1]")
            break
        except:
            error += 1
            if error >= 1000:
                break

#genwrite_key() #Alleen gebruiken wanneer pass.key verwijderd is.
key = call_key()
b = Fernet(key)

krijgGebruikers = """
SELECT * FROM Magister.gebruikers
"""

while True:
    gebruikers = read_query(connection,krijgGebruikers)
    for a in gebruikers:
        ingelogt = False
        id = a[0] #dit gebeurt omdat de string uit de DB als [()] komt. Dit moet dus omgezet worden.
        print(id)
        encryptedData = a[1]
        mail = a[2]
        decryptedData = b.decrypt(encryptedData.encode())
        pw = decryptedData.decode()

        try:
            inloggen()
        except:
            break
        if error < 1000:
            resetTabel()
            cijfersOphalen()
            vergelijkCijfer()
        else:
            try:
                driver.close()
                print('error')
            except:
                print('error')

        