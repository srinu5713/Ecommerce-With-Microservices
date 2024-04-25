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
def u_home():
    cur = conn.cursor()
    cur.execute("SELECT * FROM products")
    products = cur.fetchall()
    cur.close()
    return render_template('u_home.html', products=products)

@app.route('/orders_u')
def orders_u():
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM orders")
    orders = cursor.fetchall()
    cursor.close()
    return render_template('orders_u.html', orders=orders)

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