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

# Replace this with your actual data retrieval function
def fetch_product_by_id(product_id):
    # Placeholder logic to return a sample product for demonstration
    cur = conn.cursor()
    cur.execute("SELECT * FROM products WHERE id=%s",product_id)
    product_detail = cur.fetchone()
    cur.close()
    
    return product_detail
    
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