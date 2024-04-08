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


# Modify your Flask route to fetch product data
@app.route('/u_home')
def u_home():
    cur = conn.cursor()
    cur.execute("SELECT * FROM products")
    products = cur.fetchall()
    cur.close()
    return render_template('u_home.html', products=products)



@app.route('/a_home')
def a_home():
    # Check if the user is logged in as admin
    if session.get('user_type') != 'Admin':
        flash('Unauthorized access. Please log in as admin.', 'error')
        return redirect(url_for('login'))
    
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
    # Fetch orders from the database
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM orders')
    orders = cursor.fetchall()
    cursor.close()
    return render_template('orders.html', orders=orders)


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

@app.route('/wishlist')
def wishlist():
    # Render the wishlist page
    return render_template('wishlist.html', username=session.get('username'))

@app.route('/product/<int:product_id>')
def product_detail(product_id):
    # Fetch the product details based on the provided ID (replace this with your actual data retrieval logic)
    product = fetch_product_by_id(product_id)
    if product:
        return render_template('product_detail.html', product=product)
    else:
        return "Product not found", 404

# Replace this with your actual data retrieval function
def fetch_product_by_id(product_id):
    # Placeholder logic to return a sample product for demonstration
    cur = conn.cursor()
    cur.execute("SELECT * FROM products WHERE id=%s",product_id)
    product_detail = cur.fetchone()
    cur.close()
    
    return product_detail

@app.route('/add_to_cart/<int:product_id>/<int:quantity>', methods=['POST'])
def add_to_cart(product_id, quantity):
    # Fetch the product details based on the provided ID
    product = fetch_product_by_id(product_id)
    if product:
        # Initialize the cart if it doesn't exist in the session
        if 'cart' not in session:
            session['cart'] = {}
        # Add the product to the cart or update its quantity
        session['cart'][product_id] = {
            'name': product['pName'],
            'price': product['price'],
            'quantity': session['cart'].get(product_id, {}).get('quantity', 0) + quantity
        }
        flash('Product added to cart successfully!', 'success')
    else:
        flash('Product not found!', 'error')
    return redirect(url_for('cart'))

# Create a route to display the cart
@app.route('/cart')
def cart():
    # Fetch the products in the cart from the session
    cart_products = session.get('cart', {})
    total_amount = sum(product['price'] * product['quantity'] for product in cart_products.values())
    return render_template('cart.html', cart_products=cart_products, total_amount=total_amount)

if __name__ == '__main__':
    app.run(debug=True)