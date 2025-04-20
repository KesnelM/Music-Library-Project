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
        session['username'] = username  # ✅ set session
        return redirect(url_for('home_page'))
    else:
        return "Invalid credentials"
    

@app.route('/lib')
def view_songs():
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('signup_page'))

    query = """
        SELECT SongID, Title, Artist, Album, Genre, ReleaseYear, Duration, AddedOn
        FROM Songs
        WHERE UserID = %s
        ORDER BY AddedOn DESC
    """
    mycursor.execute(query, (user_id,))
    songs = mycursor.fetchall()

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


if __name__ == '__main__':
    print(app.url_map)
    app.run(debug=True)
   
