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

