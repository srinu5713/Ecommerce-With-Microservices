from flask import Flask, render_template, request, redirect, url_for, flash, session
import pymysql.cursors
import datetime
import os
from dotenv import load_dotenv
import time

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this to a secure secret key

# MySQL Configuration   (password**)

print("DB_HOST:", os.getenv('DB_HOST'))
print("DB_USER:", os.getenv('DB_USER'))
print("DB_PASSWORD:", os.getenv('DB_PASSWORD'))
print("DB_NAME:", os.getenv('DB_NAME'))

conn = None

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    # session['cart'].clear()
    error_message = False
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        cursor = conn.cursor()
        cursor.execute('SELECT username FROM users WHERE email = %s AND password = %s', (email, password))
        user = cursor.fetchone()
        cursor.close()
        if user:
            print("Hello user!...")
            session['email'] = email
            cursor = conn.cursor()
            cursor.execute('SELECT user_type FROM users WHERE email = %s', (email,))
            user_type = cursor.fetchone()['user_type']
            cursor.execute('SELECT user_id FROM users WHERE email = %s', (email,))
            user = cursor.fetchone()
            session['user_id'] = user['user_id']
            print(session['user_id'])
            print(user_type)
            cursor.close()
            if user_type == 'Admin':
                return redirect(url_for('a_home'))
            else:
                return redirect(url_for('u_home'))
        else:
            print("Hello...")
            error_message = True
    return render_template('login.html', error_message=error_message)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        user_type = 'Cust'  # Assuming all signups are customers
        cursor = conn.cursor()
        try:
            cursor.execute('INSERT INTO users (username, password, email, user_type) VALUES (%s, %s, %s, %s)', (name, password, email, user_type))
            conn.commit()
            flash('Signup successful! Please login.', 'success')
            return redirect(url_for('login'))
        except pymysql.err.IntegrityError as e:
            error_message = str(e)
            if 'Duplicate entry' in error_message:
                flash('Email already exists. Please use a different email.', 'error')
            else:
                flash('An error occurred. Please try again later.', 'error')
            conn.rollback()
        finally:
            cursor.close()
    return render_template('signup.html')


@app.route('/logout', methods=['GET','POST'])
def logout():
    # Clear the user session
    session.pop('user_id', None)
    return redirect(url_for('login'))


# Modify your Flask route to fetch product data
@app.route('/u_home')
def u_home():
    return render_template('u_home.html')


@app.route('/a_home')
def a_home():
    return render_template('a_home.html')

@app.route('/users')
def users():
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users')
    users = cursor.fetchall()
    cursor.close()
    return render_template('users.html', users=users)

@app.route('/profile')
def profile():
    if 'user_id' not in session:
        flash('Please login to access this page.', 'error')
        return redirect(url_for('login'))
    print(session)
    email = session['email']
    # Fetch user data from the database
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE email = %s', (email,))
    user = cursor.fetchone()
    cursor.close()
    return render_template('profile.html', user=user)



@app.route('/edit_profile', methods=['POST'])
def edit_profile():
    if 'user_id' not in session:
        flash('Please login to access this page.', 'error')
        return redirect(url_for('login'))
    user_id = session.get('user_id')
    # Fetch form data
    username = request.form['username']
    email = request.form['email']
    password = request.form['password']
    # Update user data in the database
    cursor = conn.cursor()
    try:
        cursor.execute('UPDATE users SET username = %s, email = %s, password = %s WHERE user_id = %s', (username, email, password, user_id))
        conn.commit()
        flash('Profile updated successfully!', 'success')
    except Exception as e:
        flash('An error occurred while updating the profile. Please try again.', 'error')
        conn.rollback()
    finally:
        cursor.close()
    return redirect(url_for('u_home'))
    

    
if __name__ == '__main__':
    time.sleep(5)
    conn= pymysql.connect(
    host=os.getenv('DB_HOST', 'localhost'),
    user=os.getenv('DB_USER', 'root'),
    password=os.getenv('DB_PASSWORD','qwerty@#6789'),
    database=os.getenv('DB_NAME', 'user_mgmt'),
    port=int(os.getenv("DB_PORT")),
    cursorclass=pymysql.cursors.DictCursor
    )
    app.run(host="0.0.0.0")