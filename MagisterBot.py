import discord.ext
from discord.ext import commands
import mysql.connector
from mysql.connector import Error
import json
import random

def create_db_connection(host_name, user_name, user_password, db_name):
    connection = None
    try:
        connection = mysql.connector.connect(host=host_name, user=user_name, passwd=user_password, database=db_name, auth_plugin='mysql_native_password')
        print("MySQL Database connection successful")
    except Error as err:
        print(f"Error: '{err}'")

    return connection

def execute_query(connection, query):
    cursor = connection.cursor(buffered=True)
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except Error as err:
        print(f"Error: '{err}'")


client = commands.Bot(command_prefix="/")

@client.event
async def on_ready():
    print("Bot werkt.")

@client.command()
async def ping(ctx):
    await ctx.send("Pong!")

@client.command()
async def DMping(ctx):
    msg = "Pong!"
    await ctx.author.send(msg)

@client.command()
async def clear(ctx, amount=5):
    await ctx.channel.purge(limit=amount)

@client.command()
async def DM(ctx):
    print("")

@client.command(pass_context=True)
async def start(ctx):
    host_name = '85.145.194.112'
    user_name = 'groep4'
    user_password = 'Corderiusgroep4'
    db_name = 'Magister'
    connection = create_db_connection(host_name, user_name, user_password, db_name)

    laatsteCijfer = []
    query = "SELECT gebruikerId FROM Magister.gebruikers;"
    users = execute_query(connection, query)
    for user in users:
        user = str(user).replace('(', '')
        user = str(user).replace(')', '')
        user = str(user).replace(',', '')
        userl = [str(user), "1"]
        print(userl)
        laatsteCijfer.append(userl)

    B = 0

    while True:

        print(laatsteCijfer)


        for User in users:

            User = str(User).replace('(', '')
            User = str(User).replace(')', '')
            User = str(User).replace(',', '')
            print(User)
            tablename = 'Magister.' + str(User)
            query = "SELECT idCijfer, resultaat, vak, omschrijving FROM " + tablename + " where idCijfer > 0 ;"
            query1 = "SELECT idCijfer, resultaat, vak, omschrijving FROM " + tablename + " where 26 > idCijfer > 0 ;"
            query2 = "SELECT idCijfer, resultaat, vak, omschrijving FROM " + tablename + " where 26 > idCijfer ;"
            B = random.randint(0, 2)
            print(query, B)
            if B == 0:
                response = execute_query(connection, query)

            elif B == 1:
                response = execute_query(connection, query1)

            else:
                response = execute_query(connection, query2)

            print(response)
            for user in laatsteCijfer:
                if str(User) == str(user[0]):
                    print('stap geslaagd')
                    if response[0] != user[1]:
                        print(response[0])
                        print(user[1])
                        print('nieuw cijfer!')
                        cijfer = response[0][1]
                        vak = response[0][2]
                        omschrijving = response[0][3]
                        message = str(User) + "||" + cijfer + "voor " + vak + " " + omschrijving + "||"
                        await ctx.send(message)

                        user[1] = response[0]
                        print(user)




client.run("")
