import mysql.connector
from mysql.connector import Error
from mysql.connector import errorcode
import time
import os

NODE1 = os.environ['AURORA_NODE1']
NODE2 = os.environ['AURORA_NODE2'] 

DB_NAME = "demo"
DB_USER = "admin"
DB_PASSWORD = "cloudacademy"

def reconnect(connection):
    try:
        connection.reconnect()
        print("reconnection succeeded...")
    except:
        print("reconnection failed...")

def insertCourse(connection, courseTitle):
    try:
        sql = "INSERT INTO course (title, instructor, duration, created, url) VALUES (%s, %s, %s, %s, %s)"
        cursor = connection.cursor()
        cursor.execute(sql, (courseTitle, 'Jeremy Cook', 100, '1999-03-30', 'http://here.com'))
        connection.commit()
        print(cursor.rowcount, "record inserted successfully [{}]...".format(connection.server_host))
        cursor.close()
    except:
        pass

try:
    connection1 = mysql.connector.connect(host=NODE1,
                                            database=DB_NAME,
                                            user=DB_USER,
                                            password=DB_PASSWORD)

    connection2 = mysql.connector.connect(host=NODE2,
                                            database=DB_NAME,
                                            user=DB_USER,
                                            password=DB_PASSWORD)

    for x in range(100):
        if x % 2 ==0:
            connection = connection1
            connection_backup = connection2
        else:
            connection = connection2
            connection_backup = connection1

        try:
            courseTitle = "Title{}".format(x)
            insertCourse(connection, courseTitle)
        
        except mysql.connector.Error as error:
            insert(connection_backup)

        if not connection1.is_connected():
            reconnect(connection1)

        if not connection2.is_connected():
            reconnect(connection2)

        time.sleep(0.5)

except:
    print("Failed to insert record into table {}".format(error))

finally:
    if (connection1.is_connected()):
        connection1.close()
        print("connection1 is closed")

    if (connection2.is_connected()):
        connection2.close()
        print("connection2 is closed")