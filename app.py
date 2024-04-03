from flask import Flask, render_template, request, redirect, url_for
from flask_mysqldb import MySQL

app = Flask(__name__)

# MySQL Configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = "solar_insight"

# Initialize MySQL
mysql = MySQL(app)

# Route for registration page
@app.route('/registration', methods=['GET', 'POST'])
def registration():
    if request.method == 'POST':
        # Get form data
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        contact = request.form['contact']
        capacity = request.form['capacity']
        location = request.form['location']

        # Insert user data into database
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO solar_energy (fullname, email, password, contact, capacity, location, source) VALUES (%s, %s, %s, %s,%s, %s)", (username, email, password, contact, capacity, location))
        mysql.connection.commit()
        cur.close()

        # Redirect to the index page after successful registration
        return redirect(url_for("index"))
    return render_template('registration.html')

# Route for index page
@app.route('/')
def index():
    # Fetch user data from database
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM solar_energy")
    userDetails = cur.fetchall()
    cur.close()

    # Render index.html with user details
    return render_template("index.html", userDetails=userDetails)


# Route page for profile
@app.route('/profile/<int:user_id>')
def profile(user_id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM solar_energy WHERE id = %s", (user_id,))
    userDetails = cur.fetchone()
    cur.close()
 
    return render_template("proprofile.html", userDetails=userDetails)

# Route for trading pop-up
@app.route('/trade_popup')
def trade_popup():
    return render_template("trade_popup.html")

# Route for handling trade confirmation
# @app.route('/confirm_trade', methods=['POST'])
# def confirm_trade():
#     if request.method == 'POST':
#         # Get data from the trade confirmation form
#         user_id = request.form['user_id']
#         selected_quantity = int(request.form['selected_quantity'])

#         # Fetch the user's current capacity
#         cur = mysql.connection.cursor()
#         cur.execute("SELECT capacity FROM solar_energy WHERE id = %s", (user_id,))
#         user_capacity = cur.fetchone()[0]

#         # Calculate the new capacity after trade
#         new_capacity = user_capacity - selected_quantity

#         # Update the user's capacity in the database
#         cur.execute("UPDATE solar_energy SET capacity = %s WHERE id = %s", (new_capacity, user_id))
#         mysql.connection.commit()
#         cur.close()

#         # Redirect to the index page after successful trade
#         return redirect(url_for("index"))
    
    

@app.route('/confirm_trade', methods=['POST'])
def confirm_trade():
    if request.method == 'POST':
        # Your trade confirmation logic goes here
        return 'Trade confirmed successfully'  # You can return any response here



if __name__ == "__main__":
    app.run(debug=True)