import mysql.connector

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="YourNewSecurePassword!",
    database="musicLib" ) 

mycursor = mydb.cursor()

# creates the Database
mycursor.execute("CREATE DATABASE IF NOT EXISTS musicLib ")

# creates the Table
mycursor.execute("""CREATE TABLE IF NOT EXISTS Songs
    (
    SongID INT AUTO_INCREMENT PRIMARY KEY,
    Title VARCHAR(255) NOT NULL, 
    Artist VARCHAR(255) NOT NULL,
    Album VARCHAR(255),
    Genre VARCHAR(255),
    ReleaseYear YEAR,
    Duration TIME,
    TrackNumber INT,
    AddedOn TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    ) 
    """)


print(mydb)