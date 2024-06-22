import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="lmz",
  password="1628",
  database="Teeka"
)

mycursor = mydb.cursor()

mycursor.execute("SELECT * FROM ili")

myresult = mycursor.fetchall()

for x in myresult:
  print(x)