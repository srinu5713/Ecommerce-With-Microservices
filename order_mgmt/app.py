from flask import Flask, render_template, request, redirect, url_for, flash, session
import pymysql.cursors
import datetime
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this to a secure secret key

# MySQL Configuration   (password**)
conn = pymysql.connect(
    host=os.getenv('DB_HOST', 'localhost'),
    user=os.getenv('DB_USER', 'root'),
    password=os.getenv('DB_PASSWORD'),
    database=os.getenv('DB_NAME', 'ecom'),
    cursorclass=pymysql.cursors.DictCursor
)

@app.route('/u_home')
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