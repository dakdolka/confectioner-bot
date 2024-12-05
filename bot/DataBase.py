import mysql.connector as sqllib

db = sqllib.connect(
    host="localhost",
    user="Bobr",
    password="qwerty123",
    database='test'
)

cursor = db.cursor()
