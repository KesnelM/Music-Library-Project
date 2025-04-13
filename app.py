from flask import Flask, render_template, request, redirect, session
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
def index():
    return render_template('signup.html')

@app.route('/signup', methods=['POST'])
def signup():
    username = request.form['username']
    password = request.form['password']

    try:
        sql = "INSERT INTO Users (Username, Password) VALUES (%s, %s)"
        val = (username, password)
        mycursor.execute(sql, val)
        mydb.commit()
        user_id = mycursor.lastrowid 
        session['user_id'] = user_id
        
    except Exception as e:
        return f"An error occurred: {e}"

    return render_template('index.html', username=username)

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/login_now', methods=['POST'])
def sum_login():
    
    username = request.form['username']
    password = request.form['password']

    sql = "SELECT * FROM Users WHERE Username = %s AND Password = %s"
    val = (username, password)
    mycursor.execute(sql, val)
    user = mycursor.fetchone()

    if user:
        return render_template('index.html', username=username)
    else:
        return "Invalid credentials"

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
    app.run(debug=True)
