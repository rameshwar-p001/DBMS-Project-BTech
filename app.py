from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
import mysql.connector
import os

app = Flask(__name__)

# Set secret key from environment variable for better security
app.secret_key = os.environ.get('SECRET_KEY', 'your_default_secret_key')

# MySQL database connection
def get_db_connection():
    connection = mysql.connector.connect(
        host="localhost",
        user=os.environ.get('DB_USER', 'root'),  # MySQL username from environment
        password=os.environ.get('DB_PASSWORD', 'root'),  # MySQL password from environment
        database=os.environ.get('DB_NAME', 'grahak_bhandar')  # MySQL database name from environment
    )
    return connection

@app.route('/')
def home():
    return render_template('index.html')

# Admin panel to manage products
@app.route('/admin', methods=['GET', 'POST', 'PUT'])
def admin():
    connection = get_db_connection()
    cursor = connection.cursor()

    if request.method == 'POST':
        # Add a new product
        product_name = request.form['product_name']
        category = request.form['category']
        price = float(request.form['price'])
        stock = int(request.form['stock'])
        cursor.execute("""
            INSERT INTO products (product_name, category, price, stock)
            VALUES (%s, %s, %s, %s)
        """, (product_name, category, price, stock))
        connection.commit()

    elif request.method == 'PUT':
        # Update an existing product (handle PUT request)
        data = request.get_json()  # Assuming the data is sent as JSON (typically from a form or API request)
        if data:
            product_id = data['product_id']
            product_name = data['product_name']
            category = data['category']
            price = data['price']
            stock = data['stock']

            cursor.execute("""
                UPDATE products SET product_name = %s, category = %s, price = %s, stock = %s WHERE product_id = %s
            """, (product_name, category, price, stock, product_id))
            connection.commit()

            return jsonify({"success": True, "message": "Product updated successfully!"})
        else:
            return jsonify({"success": False, "error": "Invalid data provided."})

    # Fetch all products from the database
    cursor.execute("SELECT * FROM products")
    products = cursor.fetchall()
    cursor.close()
    connection.close()

    return render_template('admin.html', products=products)


# Admin route for deleting a product
@app.route('/admin/cutoff', methods=['DELETE'])
def cutoff_product():
    try:
        product_data = request.get_json()
        product_id = product_data.get('product_id')  # Make sure to use 'product_id'

        if not product_id:
            return jsonify({"success": False, "error": "Product ID is required"}), 400

        connection = get_db_connection()
        cursor = connection.cursor()

        # Check if the product exists before deleting
        cursor.execute("SELECT * FROM products WHERE product_id = %s", (product_id,))
        product = cursor.fetchone()
        if not product:
            return jsonify({"success": False, "error": "Product not found"}), 404

        # Deleting the product from the database
        cursor.execute("DELETE FROM products WHERE product_id = %s", (product_id,))
        connection.commit()

        cursor.close()
        connection.close()

        return jsonify({"success": True}), 200

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


# User interface to view products and add them to the bucket
@app.route('/shop', methods=['GET', 'POST'])
def shop():
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM products")
    products = cursor.fetchall()
    cursor.close()
    connection.close()

    # Initialize cart if not present
    if 'cart' not in session:
        session['cart'] = {}

    if request.method == 'POST':
        if 'product_name' in request.form:
            product_name = request.form['product_name']
            quantity = int(request.form['quantity'])  # Ensure quantity is an integer

            # Check if the product is already in the cart
            if product_name in session['cart']:
                session['cart'][product_name]['quantity'] += quantity
            else:
                # Fetch product details
                for product in products:
                    if product[1] == product_name:  # Use index or dictionary column names if possible
                        session['cart'][product_name] = {
                            'price': float(product[3]),  # Ensure price is a float
                            'quantity': quantity
                        }

            session.modified = True
            flash("Product added to bucket!")

        if 'buy_now' in request.form:
            # Generate Bill and update stock
            bill = {}
            bill_total = 0.0

            # Begin transaction to update stock and save order
            connection = get_db_connection()
            cursor = connection.cursor()

            try:
                # Save order details to 'orders' table
                user_id = 1  # Assuming a logged-in user, replace with actual user session
                cursor.execute("""
                    INSERT INTO orders (user_id, total_amount, order_date, status)
                    VALUES (%s, %s, NOW(), 'pending')
                """, (user_id, bill_total))
                connection.commit()

                # Get the last inserted order_id
                cursor.execute("SELECT LAST_INSERT_ID()")
                order_id = cursor.fetchone()[0]

                # Save order items to 'order_items' table
                for product_name, product_data in session['cart'].items():
                    price = float(product_data['price'])
                    quantity = int(product_data['quantity'])
                    bill[product_name] = product_data
                    bill_total += price * quantity

                    # Fetch product details
                    cursor.execute("SELECT * FROM products WHERE product_name = %s", (product_name,))
                    product = cursor.fetchone()

                    if product:
                        new_stock = product[4] - quantity  # Assuming stock is the fifth column
                        cursor.execute("UPDATE products SET stock = %s WHERE product_name = %s", (new_stock, product_name))

                        # Insert the product into order_items table
                        cursor.execute("""
                            INSERT INTO order_items (order_id, product_name, quantity, price)
                            VALUES (%s, %s, %s, %s)
                        """, (order_id, product_name, quantity, price))

                connection.commit()
                session['cart'] = {}  # Clear the cart after purchase
                session.modified = True
                flash("Thank you for your purchase!")

            except Exception as e:
                connection.rollback()  # Rollback in case of any error
                flash("An error occurred while processing your order.")
                print(f"Error: {e}")

            cursor.close()
            connection.close()

            return render_template('shop.html', products=products, cart={}, cart_total=0.0, bill=bill, bill_total=round(bill_total, 2))  # Round the total

    # Calculate cart total
    cart_total = 0.0
    for product_name, product_data in session['cart'].items():
        price = float(product_data['price'])
        quantity = int(product_data['quantity'])
        cart_total += price * quantity

    return render_template('shop.html', products=products, cart=session['cart'], cart_total=round(cart_total, 2), bill=None)


# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
