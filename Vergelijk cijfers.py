import mysql.connector
import smtplib
from mysql.connector import Error

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
connection = create_db_connection('85.145.194.112', 'groep4', 'Corderiusgroep4', 'Magister')
id = 141507

getLaatsteCijfer = """
SELECT * FROM view""" + str(id) + """ WHERE idCijfer=1
"""

global laatsteCijfer
laatsteCijfer = read_query(connection, getLaatsteCijfer)
try:
    laatsteCijfer = laatsteCijfer[0]
    print(laatsteCijfer)
except:
	print('Geen cijfers')

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
    print(idCijfer)
except:
	print('Geen cijfer')

smtpServer()
to = 'mathijs.tak@outlook.com'
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
