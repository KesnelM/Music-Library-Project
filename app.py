from flask import Flask, render_template, request, redirect
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
    except Exception as e:
        return f"An error occurred: {e}"

    return render_template('index.html')

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
        return render_template('index.html')
    else:
        return "Invalid credentials"

@app.route('/add-album', methods=['POST'])
def add_album():
    title = request.form['album-title']
    release_date = request.form['release-date']
    track_count = request.form['track-list']

    try:
        sql = """
            INSERT INTO Songs (Title, Artist ,Album, ReleaseYear, TrackNumber)
            VALUES (%s, "Unknown Artist",%s, %s, %s)
        """
        release_year = release_date.split('-')[0] 

        val = (title, title, release_year, track_count) 
        mycursor.execute(sql, val)
        mydb.commit()
    except Exception as e:
        return f"An error occurred: {e}"

    return redirect('index.html')

if __name__ == '__main__':
    app.run(debug=True)
