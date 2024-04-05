from flask import Flask, render_template, request, redirect, url_for, flash
import pymysql.cursors

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this to a secure secret key

# MySQL Configuration
conn = pymysql.connect(
    host='localhost',
    user='root',
    password='wasd',
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
        cursor = conn.cursor()
        cursor.execute('SELECT username, user_type FROM users WHERE email = %s AND password = %s', (email, password))
        user = cursor.fetchone()
        cursor.close()
        if user:
            if user['user_type'] == 'Admin':
                return redirect(url_for('a_home'))
            else:
                return redirect(url_for('u_home'))
        else:
            flash('Invalid email or password. Please try again.', 'error')
            return render_template('login.html')  # Render login page again on failed login
    return render_template('login.html')

@app.route('/logout', methods=['POST'])
def logout():
    return redirect(url_for('login'))

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

@app.route('/u_home')
def u_home():
    # Check user session or authentication here before rendering the home page
    return render_template('u_home.html')

@app.route('/a_home')
def a_home():
    # Check user session or authentication here before rendering the home page
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM orders")
    orders_count = cur.fetchone()['COUNT(*)']
    cur.execute("SELECT COUNT(*) FROM users")
    users_count = cur.fetchone()['COUNT(*)']
    cur.execute("SELECT COUNT(*) FROM products")
    products_count = cur.fetchone()['COUNT(*)']
    cur.close()
    return render_template('a_home.html', orders_count=orders_count, users_count=users_count, products_count=products_count)

@app.route('/orders')
def orders():
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM orders')
    orders = cursor.fetchall()
    cursor.close()
    return render_template('orders.html', orders=orders)

@app.route('/users')
def users():
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users')
    users = cursor.fetchall()
    cursor.close()
    return render_template('users.html', users=users)

@app.route('/products')
def products():
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM products')
    products = cursor.fetchall()
    cursor.close()
    return render_template('products.html', products=products)

@app.route('/add_product', methods=['GET', 'POST'])
def add_product():
    if request.method == 'POST':
        # Retrieve form data
        name = request.form['name']
        price = request.form['price']
        description = request.form['description']
        quantity = request.form['quantity']
        category = request.form['category']
        item = request.form['item']
        pcode = request.form['pcode']
        picture = request.form['picture']
        date = request.form['date']

        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO products (name, price, description, quantity, category, item, pcode, picture, date) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
                           (name, price, description, quantity, category, item, pcode, picture, date))
            conn.commit()
            flash('Product added successfully!', 'success')
            return redirect(url_for('products'))
        except Exception as e:
            flash('An error occurred while adding the product. Please try again.', 'error')
            conn.rollback()
        finally:
            cursor.close()
    return render_template('add_product.html')

@app.route('/edit_product/<int:product_id>', methods=['GET', 'POST'])
def edit_product(product_id):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM products WHERE id = %s", (product_id,))
    product = cursor.fetchone()
    cursor.close()

    if request.method == 'POST':
        # Retrieve form data
        name = request.form['name']
        price = request.form['price']
        description = request.form['description']
        quantity = request.form['quantity']
        category = request.form['category']
        item = request.form['item']
        pcode = request.form['pcode']
        picture = request.form['picture']
        date = request.form['date']

        cursor = conn.cursor()
        try:
            cursor.execute("UPDATE products SET name = %s, price = %s, description = %s, quantity = %s, category = %s, item = %s, pcode = %s, picture = %s, date = %s WHERE id = %s",
                           (name, price, description, quantity, category, item, pcode, picture, date, product_id))
            conn.commit()
            flash('Product updated successfully!', 'success')
            return redirect(url_for('products'))
        except Exception as e:
            flash('An error occurred while updating the product. Please try again.', 'error')
            conn.rollback()
        finally:
            cursor.close()
    return render_template('edit_product.html', product=product)

@app.route('/delete_product/<int:product_id>', methods=['GET', 'POST'])
def delete_product(product_id):
    if request.method == 'POST':
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM products WHERE id = %s", (product_id,))
            conn.commit()
            flash('Product deleted successfully!', 'success')
        except Exception as e:
            flash('An error occurred while deleting the product. Please try again.', 'error')
            conn.rollback()
        finally:
            cursor.close()
    return redirect(url_for('products'))

if __name__ == '__main__':
    app.run(debug=True)
