import mysql.connector

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="YourNewSecurePassword!",
    database="musicLib" ) 

mycursor = mydb.cursor()


mycursor.execute("CREATE DATABASE IF NOT EXISTS musicLib ")



mycursor.execute("""CREATE TABLE IF NOT EXISTS Users
    (
    UserID INT AUTO_INCREMENT PRIMARY KEY,
    Username VARCHAR(255) NOT NULL,
    Password VARCHAR(255) NOT NULL
    )
""")

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
    AddedOn TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UserID INT,
    FOREIGN KEY (UserID) REFERENCES Users(UserID)
    ) 
    """)


print(mydb)