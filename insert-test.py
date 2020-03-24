import mysql.connector
from mysql.connector import Error
from mysql.connector import errorcode
import time
import os

AURORA_NODE1 = os.environ['AURORA_NODE1']
AURORA_NODE2 = os.environ['AURORA_NODE2']

DB_NAME = "demo"
DB_USER = "admin"
DB_PASSWORD = "cloudacademy"

def reconnect(connection):
    try:
        connection.reconnect()
        print("reconnection succeeded...")
    except:
        print("reconnection failed...")

try:
    connection1 = mysql.connector.connect(host=AURORA_NODE1,
                                            database=DB_NAME,
                                            user=DB_USER,
                                            password=DB_PASSWORD)

    connection2 = mysql.connector.connect(host=AURORA_NODE2,
                                            database=DB_NAME,
                                            user=DB_USER,
                                            password=DB_PASSWORD)

    sql = "INSERT INTO course (title, instructor, duration, created, url) VALUES (%s, %s, %s, %s, %s)"

    for x in range(100):
        courseTitle = "Title{}".format(x)
        data = (courseTitle, 'Jeremy Cook', 100, '1999-03-30', 'http://here.com')

        #connection load balancing logic
        if x % 2 == 0:
            connection = connection1
            connection_backup = connection2
        else:
            connection = connection2
            connection_backup = connection1

        try:
            cursor = connection.cursor()
            cursor.execute(sql, data)
            connection.commit()
            print(cursor.rowcount, "record inserted successfully [{}]...".format(connection.server_host))
            cursor.close()

        #connection retry logic
        except mysql.connector.errors.Error:
            cursor = connection_backup.cursor()
            cursor.execute(sql, data)
            connection_backup.commit()
            print(cursor.rowcount, "record inserted (BACKUP) successfully [{}]...".format(connection_backup.server_host))
            cursor.close()

        if not connection1.is_connected():
            reconnect(connection1)

        if not connection2.is_connected():
            reconnect(connection2)

        time.sleep(0.5)

except Error as error:
    print("Failed to insert record into table: {}".format(error))

finally:
    if (connection1.is_connected()):
        connection1.close()
        print("connection1 is closed")

    if (connection2.is_connected()):
        connection2.close()
        print("connection2 is closed")