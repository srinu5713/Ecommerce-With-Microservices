from flask import Flask, render_template, request, redirect, url_for, flash, session
import pymysql.cursors
import datetime
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this to a secure secret key

# MySQL Configuration
conn = pymysql.connect(
    host=os.getenv('DB_HOST', 'host.docker.internal'),
    user=os.getenv('DB_USER', 'root'),
    password=os.getenv('DB_PASSWORD'),
    database=os.getenv('DB_NAME', 'ecom'),
    cursorclass=pymysql.cursors.DictCursor
)

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
    cur = conn.cursor()
    cur.execute("SELECT * FROM products")
    products = cur.fetchall()
    cur.close()
    return render_template('u_home.html', products=products)



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
    # Fetch orders from the database
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM orders WHERE user_id=%s',int(session['user_id']))
    orders = cursor.fetchall()
    cursor.close()
    return render_template('orders.html', orders=orders)

@app.route('/orders_u')
def orders_u():
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM orders")
    orders = cursor.fetchall()
    cursor.close()
    return render_template('orders_u.html', orders=orders)

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
        picture_url = request.form['picture_url']
        # date = request.form['date'] # Assuming you have a field named 'date' in your form

        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO products (pName, price, description, quantity, category, picture_url) VALUES (%s, %s, %s, %s, %s, %s)",
                           (name, price, description, quantity, category, picture_url))
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
        picture_url = request.form['picture_url']
        # date = request.form['date'] # Assuming you have a field named 'date' in your form

        cursor = conn.cursor()
        try:
            cursor.execute("UPDATE products SET pName = %s, price = %s, description = %s, quantity = %s, category = %s, picture_url = %s WHERE id = %s",
                           (name, price, description, quantity, category, picture_url, product_id))
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
    if request.method == 'GET':
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

@app.route('/add_to_cart/<product_id>/<quantity>', methods=['POST','GET'])
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
            'quantity': session['cart'].get(product_id, {}).get('quantity', 0) + int(quantity)
        }
        print(session['cart'])
        flash('Product added to cart successfully!', 'success')
    else:
        flash('Product not found!', 'error')
    return redirect(url_for('cart'))


from flask import request, jsonify

@app.route('/remove_from_cart/<product_id>', methods=['POST','GET'])
def remove_from_cart(product_id):
    try:
        # Get the user's cart data from the session
        cart = session.get('cart', {})
        # Check if the product exists in the cart
        if product_id in cart:
            # Remove the product from the cart
            del cart[product_id]
            session['cart'] = cart  # Update the cart data in the session
            
            # Optionally, you can also remove the product from the database cart if needed
            
            return jsonify({'message': 'Product removed from cart successfully'}), 200
        else:
            return jsonify({'error': 'Product not found in cart'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# Create a route to display the cart
@app.route('/cart')
def cart():
    # Fetch the products in the cart from the session
    cart_products = session.get('cart', {})
    total_amount = sum(product['price'] * product['quantity'] for product in cart_products.values())
    return render_template('cart.html', cart_products=cart_products, total_amount=total_amount)

@app.route('/place_order', methods=['POST'])
def place_order():
    # Receive cart details from the request
    cart_data = session.get('cart')

    if cart_data:
        try:
            # Connect to MySQL database
            cursor = conn.cursor()

            # Insert each cart item into the orders table
            for product_id, quantity in cart_data.items():
                cursor.execute("SELECT pName , price FROM products WHERE id = %s", (product_id,))
                product_data = cursor.fetchone()
                print(product_data)
                if product_data:
                    pName, price = product_data['pName'],product_data['price']
                    print(pName,price)
                    try:
                        price = int(price)
                        product_id=int(product_id)

                    except ValueError:
                        return f"Invalid price value: {price}", 500
                    print(session['user_id'], product_id, pName, quantity, price, datetime.datetime.now(),datetime.date.today())
                    cursor.execute("INSERT INTO orders (user_id, product_id, product_name, quantity, price, order_date, expected_date) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                                (session['user_id'], product_id, pName, quantity['quantity'], price, datetime.datetime.now(),datetime.date.today()+datetime.timedelta(days=3)))

                else:
                    return "Product not found", 404 


            # Commit changes and close connection
            conn.commit()
            cursor.close()
            conn.close()

            return "Order placed successfully", 200
        except Exception as e:
            return str(e), 500
    else:
        return "No data received", 400
    
@app.route('/wishlist/<product_id>', methods=['POST', 'GET'])
def add_to_wishlist(product_id):
    # Fetch the product details based on the provided ID
    product = fetch_product_by_id(product_id)
    if product:
        print("Entered Wishlist Add")
        cur = conn.cursor()
        try:
            print("Entry")
            cur.execute("SELECT * FROM products WHERE id=%s", product_id)
            product = cur.fetchall()
            print("----------------")
            print(session['user_id'], product_id, product[0]['pName'], product[0]['quantity'])
            print("----------------")
            cur.execute("INSERT INTO wishlist (user_id, product_id, product_name, quantity) VALUES (%s, %s, %s, %s)", (int(session['user_id']), product_id, product[0]['pName'], product[0]['quantity']))
            conn.commit()
            print("Committed")
            flash('Product added to wishlist successfully!', 'success')
        except Exception as e:
            print('Error')
            flash('An error occurred while adding the product to the wishlist. Please try again.', 'error')
            conn.rollback()
        finally:
            cur.close()
            # conn.close()  # Do not close the connection here, as it's being used in wishlist_page function
    else:
        flash('Product not found!', 'error')
    return redirect(url_for('wishlist'))

@app.route('/wishlist', methods=['POST', 'GET'])
def wishlist():
    print("---------------------")
    # Fetch the user's wishlist from the database
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM wishlist WHERE user_id = %s", (session['user_id'],))
    wishlist_items = cursor.fetchall()
    print(wishlist_items)
    cursor.close()
    return render_template('wishlist.html', wishlist_items=wishlist_items)

@app.route('/remove_from_wishlist/<int:product_id>', methods=['POST'])
def remove_from_wishlist(product_id):
    # Remove the product from the user's wishlist
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM wishlist WHERE user_id = %s AND product_id = %s", (session['user_id'], product_id))
        conn.commit()
        flash('Product removed from wishlist successfully!', 'success')
    except Exception as e:
        flash('An error occurred while removing the product from the wishlist. Please try again.', 'error')
        conn.rollback()
    finally:
        cursor.close()
    return redirect(url_for('wishlist'))
    

    
if __name__ == '__main__':
    app.run(debug=True)