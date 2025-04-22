from flask import Flask, render_template, request, redirect, session, url_for
import mysql.connector

app = Flask(__name__)

# Configure DB connection
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="YourNewSecurePassword!",
    database="musicLib"
)
mycursor = mydb.cursor()

app.secret_key = 'supersecretkey'

@app.route('/')
def signup_page(): 
    return render_template('signup.html')


@app.route('/home')
def home_page():
    username = session.get('username')
    if not username:
        return redirect(url_for('signup_page'))  
    return render_template('index.html', username=session.get('username'))

@app.route('/login')
def login_page():
    return render_template('login.html')


@app.route('/signup', methods=['POST'])
def signup():
    username = request.form['username']
    password = request.form['password']

    try:
        while mycursor.nextset():
            pass
    
        sql = "INSERT INTO Users (Username, Password) VALUES (%s, %s)"
        val = (username, password)
        mycursor.execute(sql, val)
        mydb.commit()

        
        user_id = mycursor.lastrowid 
        session['user_id'] = user_id
        session['username'] = username
        
    except Exception as e:
        return f"An error occurred: {e}"

    return redirect(url_for('home_page'))



@app.route('/login_now', methods=['POST'])
def sum_login():
    
    username = request.form['username']
    password = request.form['password']

    sql = "SELECT * FROM Users WHERE Username = %s AND Password = %s"
    val = (username, password)
    mycursor.execute(sql, val)
    user = mycursor.fetchone()

    if user:
        session['user_id'] = user[0]
        session['username'] = username  
        return redirect(url_for('home_page'))
    else:
        return "Invalid credentials"
    

@app.route('/lib')
def view_songs():
    user_id = session.get('user_id')
    print(user_id)
    if not user_id:
        return redirect(url_for('signup_page'))

    query = """
    SELECT
      s.SongID,
      s.Title,
      s.Artist,
      s.Album,
      s.Genre,
      s.ReleaseYear,
      s.Duration,
      s.AddedOn,
      IFNULL(ROUND(AVG(r.Rating), 2), 0) AS AvgRating,
      COUNT(r.Rating)               AS RatingCount
    FROM Songs AS s
    LEFT JOIN Ratings AS r
      ON s.SongID = r.SongID
    WHERE s.UserID = %s
    GROUP BY s.SongID
    ORDER BY s.AddedOn DESC
"""

    createuser = user_id
    mycursor.execute(query, (createuser,))
    songs = mycursor.fetchall()
    print(songs)
    if not songs:
        print("No songs found for this user.")
        return render_template('lib.html', songs=[])

    return render_template('lib.html', songs=songs)    

@app.route('/add-song', methods=['POST'])
def add_song():
    user_id = session.get('user_id')
    if not user_id:
            return "User not logged in"
    
    title = request.form['title']
    artist = request.form['artist']
    album = request.form['album']
    genre = request.form['genre']
    release_year = request.form['release-year']
    duration = request.form['duration']
    track_number = request.form['track-number']

    try:
        sql = """
        INSERT INTO Songs (Title, Artist, Album, Genre, ReleaseYear, Duration, TrackNumber, UserID)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """

        val = (title, artist, album, genre, release_year, duration, track_number, user_id) 
        mycursor.execute(sql, val)
        mydb.commit()
    except Exception as e:
        return f"An error occurred: {e}"

    return render_template('index.html', message="Song added successfully!")

@app.route('/delete/<int:song_id>', methods=['POST'])
def delete_song(song_id):
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('signup_page'))

    try:
        delete_ratings = "DELETE FROM Ratings WHERE SongID = %s"
        mycursor.execute(delete_ratings, (song_id,)) 
        
        sql = "DELETE FROM Songs WHERE SongID = %s AND UserID = %s"
        mycursor.execute(sql, (song_id, user_id))
        mydb.commit()
    except Exception as e:
        return f"An error occurred while deleting the song: {e}"

    return redirect(url_for('view_songs'))


@app.route('/edit/<int:song_id>', methods=['GET'])
def edit_song(song_id):
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('signup_page'))

    query = """
        SELECT SongID, Title, Artist, Album, Genre, ReleaseYear, Duration, TrackNumber
        FROM Songs WHERE SongID = %s AND UserID = %s
    """
    mycursor.execute(query, (song_id, user_id))
    song = mycursor.fetchone()

    if not song:
        return "Song not found or unauthorized access."

    return render_template('editsong.html', song=song)


@app.route('/update-song/<int:song_id>', methods=['POST'])
def update_song(song_id):
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('signup_page'))

    title = request.form['title']
    artist = request.form['artist']
    album = request.form['album']
    genre = request.form['genre']
    release_year = request.form['release-year']
    duration = request.form['duration']
    track_number = request.form['track-number']

    try:
        sql = """
        UPDATE Songs
        SET Title = %s, Artist = %s, Album = %s, Genre = %s,
            ReleaseYear = %s, Duration = %s, TrackNumber = %s
        WHERE SongID = %s AND UserID = %s
        """
        val = (title, artist, album, genre, release_year, duration, track_number, song_id, user_id)
        mycursor.execute(sql, val)
        mydb.commit()
    except Exception as e:
        return f"An error occurred: {e}"

    return redirect(url_for('view_songs'))

@app.route('/rate-song', methods=['POST'])
def rate_song():
    song_id = request.form.get('song_id')
    rating  = int(request.form.get('rating', 0))

    # simple validation
    if rating < 1 or rating > 5:
        return "Rating must be between 1 and 5", 400

    sql = "INSERT INTO Ratings (SongID, Rating) VALUES (%s, %s)"
    mycursor.execute(sql, (song_id, rating))
    mydb.commit()
    return redirect(url_for('view_songs'))

@app.route('/artist-ratings')
def artist_ratings():
    sql = """
      SELECT Artist, ROUND(AVG(Rating), 2) AS AvgRating
      FROM Songs
      JOIN Ratings ON Songs.SongID = Ratings.SongID
      GROUP BY Artist
      ORDER BY AvgRating DESC
    """
    mycursor.execute(sql)
    ratings = mycursor.fetchall() 
    return render_template('artist_ratings.html', ratings=ratings)

@app.route('/best-artist')
def best_artist():
    mycursor.execute("""
      SELECT
        s.Artist           AS ArtistName,
        ROUND(AVG(r.Rating), 2)  AS AvgRating,
        COUNT(r.Rating)         AS NumRatings,
        ROUND(AVG(r.Rating)*COUNT(r.Rating), 2) AS Score
      FROM Songs s
      JOIN Ratings r
        ON s.SongID = r.SongID
      GROUP BY s.Artist
      ORDER BY Score DESC
      LIMIT 1
    """)
    row = mycursor.fetchone()
    if row:
        artist_name, avg, num, score = row
    else:
        artist_name = avg = num = score = None

    return render_template(
      'best_artists.html',
      artist=artist_name,
      avg_rating=avg,
      num_ratings=num,
      score=score
    )
    
    #best = mycursor.fetchone()  
    #return render_template('best_artists.html', best=best)



if __name__ == '__main__':
    print(app.url_map)
    app.run(debug=True)
   
