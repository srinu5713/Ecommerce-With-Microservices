from flask import Flask, render_template, request, redirect, url_for, flash, session
import pymysql.cursors

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this to a secure secret key

# MySQL Configuration
conn = pymysql.connect(
    host='localhost',
    user='root',
    password='Chinu139*',
    database='ecom',
    cursorclass=pymysql.cursors.DictCursor
)

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        session['email']=email
        cursor = conn.cursor()
        cursor.execute('SELECT username FROM users WHERE email = %s AND password = %s', (email, password))
        user = cursor.fetchone()
        cursor.close()
        print(session)
        if user:
            cursor = conn.cursor()
            cursor.execute('SELECT user_type FROM users WHERE email = %s', (email,))
            user_type = cursor.fetchone()['user_type']
            cursor.close()
            if user_type == 'Admin':
                return redirect(url_for('a_home'))
            else:
                return redirect(url_for('u_home'))
        else:
            flash('Invalid email or password. Please try again.', 'error')
            # Clear password field by passing empty string to the login.html template
            return render_template('login.html', email=email, password='')
    return render_template('login.html')

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
            cursor.execute('SELECT * FROM users WHERE email = %s', (email,))
            user = cursor.fetchone()
            session['user_id']=user['user_id']
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

@app.route('/u_home')
def u_home():
    # Check user session or authentication here before rendering the home page
    return render_template('u_home.html')

@app.route('/a_home')
def a_home():
    # Check user session or authentication here before rendering the home page
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM orders")
    # c1=cur.fetchone()
    print("-----------------------------------------------")
    # print(c1)
    print("-----------------------------------------------")
    orders_count = cur.fetchone()['COUNT(*)']
    cur.execute("SELECT COUNT(*) FROM users")
    users_count = cur.fetchone()['COUNT(*)']
    cur.execute("SELECT COUNT(*) FROM products")
    products_count = cur.fetchone()['COUNT(*)']
    cur.close()
    return render_template('a_home.html', orders_count=orders_count, users_count=users_count, products_count=products_count)


@app.route('/orders')
def orders():
    # Fetch orders from the database
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM orders')
    orders = cursor.fetchall()
    cursor.close()
    return render_template('orders.html', orders=orders)

@app.route('/users')
def users():
    # Fetch users from the database
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users')
    users = cursor.fetchall()
    cursor.close()
    return render_template('users.html', users=users)

@app.route('/products')
def products():
    # Fetch products from the database
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM products')
    products = cursor.fetchall()
    cursor.close()
    return render_template('products.html', products=products)

@app.route('/profile')
def profile():
    '''if 'user_id' not in session:
        flash('Please login to access this page.', 'error')
        return redirect(url_for('login'))'''
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

@app.route('/cart')
def cart():
    # Render the cart page
    return render_template('cart.html', username=session.get('username'))

@app.route('/wishlist')
def wishlist():
    # Render the wishlist page
    return render_template('wishlist.html', username=session.get('username'))

if __name__ == '__main__':
    app.run(debug=True)