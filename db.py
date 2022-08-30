import mysql.connector

conn = mysql.connector.connect(host="localhost", 
    user="root", 
    passwd="0Minar16",
    )

cur = conn.cursor()
cur.execute("CREATE DATABASE Blog")
cur.execute("SHOW DATABASES")

for db in cur:
    print(db)

conn.close()