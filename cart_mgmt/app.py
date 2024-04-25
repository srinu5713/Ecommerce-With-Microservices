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

@app.route('/')
def u_home():
    cur = conn.cursor()
    cur.execute("SELECT * FROM products")
    products = cur.fetchall()
    cur.close()
    return render_template('u_home.html', products=products)


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