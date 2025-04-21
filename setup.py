import mysql.connector


mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="YourNewSecurePassword!"
     ) 


mycursor = mydb.cursor()


mycursor.execute("CREATE DATABASE IF NOT EXISTS musicLib ")

mycursor.execute("USE musicLib")

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

mycursor.execute("""
CREATE TABLE IF NOT EXISTS Ratings (
    RatingID INT AUTO_INCREMENT PRIMARY KEY,
    SongID INT NOT NULL,
    Rating TINYINT NOT NULL CHECK (Rating BETWEEN 1 AND 5),
    RatedOn TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (SongID) REFERENCES Songs(SongID)
)
""")

mycursor.execute("""
  CREATE OR REPLACE VIEW ArtistScore AS
    SELECT 
      s.Artist,
      ROUND(AVG(r.Rating),2)    AS AvgRating,
      COUNT(r.Rating)           AS NumRatings,
      ROUND(AVG(r.Rating)*COUNT(r.Rating),2) AS Score
    FROM Songs s
    JOIN Ratings r ON s.SongID = r.SongID
    GROUP BY s.Artist
""") 

print(mydb)