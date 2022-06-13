"""
we are validating username and password with registered users
in database
"""

# --------------------
# Create App (Object) for our website
# --------------------
import flask
from flask_session import Session
from flask import session
foodcourt_app = flask.Flask(__name__)

foodcourt_app.secret_key = "My Secrete password"
foodcourt_app.config["SESSION_TYPE"] = "filesystem"

Session(foodcourt_app)
# --------------------


#import flask
#foodcourt_app = flask.Flask("foodcourtApp")
# --------------------

# --------------------
# END POINT - 1 : http://127.0.0.1:5000/ URL MAPPED to '/'
# --------------------
@foodcourt_app.route('/')
def my_index_page():
    return flask.render_template('index.html')
# --------------------

# --------------------
# END POINT - 2 : http://127.0.0.1:5000/about URL MAPPED to '/about'
# --------------------
@foodcourt_app.route('/about')
def my_about_page():
    return flask.render_template('about.html')
# --------------------

# --------------------
# END POINT - 3 : http://127.0.0.1:5000/login URL MAPPED to '/login'
# --------------------
@foodcourt_app.route('/login')
def my_login_page():
    return flask.render_template('login.html')
# --------------------

# --------------------

# END POINT - 4: http://127.0.0.1:5000/validate URL MAPPED to '/validate'
# --------------------
@foodcourt_app.route('/validate', methods=['POST'])
def my_validate_page():
    # Task - 1 : Get user name & pass word entered by user
    # ----------------
    # framework will keep all the form data entered by use in a dictionary.
    # dictionary is 'flask.request.form'. from this dictionary we can retrieve username & password
    # key will be 'uname' and 'pw'
    entered_username = flask.request.form.get('uname')
    entered_password = flask.request.form.get('pw')
    entered_username=entered_username.lower()
    entered_username=entered_username.strip()

    # Connect to user_db.sqlite, check whether entered username and password
    # present. If not present then return login failed
    import sqlite3

    print("Create/Connect to database 'users_db.sqlite' ")
    my_db_connection = sqlite3.connect(r'users_db.sqlite')
    print("Done")

    print("Get cursor object, which help us to execute SQL query on database ")
    my_db_cursor = my_db_connection.cursor()
    print("Done")

    print("Check weather table exist")
    my_db_cursor.execute(
        f"SELECT name FROM sqlite_master WHERE type='table' AND name='users_table';")
    print("Done")

    print("Retrieve all data from cursor")
    my_db_result = my_db_cursor.fetchall()
    print("Done")
    if len(my_db_result)==0:
        return 'first register to login'

    print("Executing select query")
    my_db_cursor.execute(f"SELECT NAME, PASSWORD FROM USERS_TABLE WHERE NAME='{entered_username}' AND PASSWORD = '{entered_password}'")
    print("Done")

    print("Retrieve all data from cursor")
    my_db_result = my_db_cursor.fetchall()
    print("Done")
    # if we get record then username & password correct else wrong

    # This work is done, so close db connection
    my_db_connection.close()

    if len(my_db_result) > 0:
        # Store Username in Session Object
        session['username'] = entered_username

        return "login success"

    else:
        return "Login Failed. Invalid Credentials <br><br> <a href='/login'>Go Back To Login</a>"

# ----------------
# POINTS - 1
# ----------------
# - We are sending data inside python object to html file
# - If we need to display python variable in html then we need to
#   write python code inside html
# - We can write python code inside html file using below syntax
#   1) Use this {{variable_name}} to display any python variable value
#   2) Use this {% to write any python code %}
#   3) Use this {% if condn%}  for any block like if, for etc
#               {% endif %}
# ----------------
# --------------------

# --------------------
# END POINT - 5 : http://127.0.0.1:5000/newuser URL MAPPED to '/newuser'
# --------------------
@foodcourt_app.route('/newuser')
def my_newuser_page():
    return flask.render_template('newuser.html')
# --------------------

# --------------------
# END POINT - 6 : http://127.0.0.1:5000/register URL MAPPED to '/register'
# --------------------
@foodcourt_app.route('/register', methods=['POST'])
def my_register_page():

    # Get all data
    entered_username = flask.request.form.get('uname')
    entered_password_1 = flask.request.form.get('pw1')
    entered_password_2 = flask.request.form.get('pw2')
    entered_email = flask.request.form.get('email')

    # Check whether both the passwords are matching
    if entered_password_1 != entered_password_2:
        return "Both Passwords Are Not Matching. <br><br><a href='/login'>Go Back To Registration</a>"

    # Create Database and table if not present
    import sqlite3

    print("Create/Connect to database 'users_db.sqlite' ")
    my_db_connection = sqlite3.connect('users_db.sqlite')
    print("Done")

    print("Get cursor object, which help us to execute SQL query on database ")
    my_db_cursor = my_db_connection.cursor()
    print("Done")

    print("Create table if not exists")
    my_query = '''CREATE TABLE IF NOT EXISTS users_table(
    NAME    VARCHAR(100),
    PASSWORD    VARCHAR(100),
    EMAIL   VARCHAR(100)
    )
    '''
    my_db_cursor.execute(my_query)
    print("Done")
    # ------------------------

    # verify whether user already exists in the database
    # How? select from table where username = entered_username
    # if we get records then we decide found
    # if we get 0 records the we can decide not found
    entered_username = entered_username.lower()
    entered_username = entered_username.strip()
    my_query = f"SELECT * FROM users_table WHERE name='{entered_username}'"
    my_db_cursor.execute(my_query)
    my_db_result = my_db_cursor.fetchall()
    if len(my_db_result) > 0:
        return "User Already Exists. <br><br><a href='/login'>Go Back To Registration</a>"

    # if user not exists then add new record to database and return account created successfully
    my_query = f"INSERT INTO USERS_TABLE VALUES('{entered_username}', '{entered_password_1}', '{entered_email}')"
    my_db_cursor.execute(my_query)
    my_db_connection.commit()
    my_db_connection.close()
    return "User Created Successfully. <a href='/login'>Click Here To Login</a>"


# END POINT - 7 : http://127.0.0.1:5000/addnew URL MAPPED to '/addnew'

@foodcourt_app.route('/addnew')
def my_addnew_page():
    return flask.render_template('addnew.html')
#______________________________________

# END POINT - 8 : http://127.0.0.1:5000/foodmin URL MAPPED to '/foodmin'
@foodcourt_app.route('/foodmin', methods=['POST'])
def my_foodmin_page():
    # Get all data
    entered_restoname = flask.request.form.get('rname')
    entered_restolocation = flask.request.form.get('rlocation')
    entered_foodname = flask.request.form.get('food')
    entered_preperationcost = flask.request.form.get('cost')
    entered_sellingprice = flask.request.form.get('sellingprice')
    entered_description = flask.request.form.get('description')

    # Create Database and table if not present
    import sqlite3

    print("Create/Connect to database 'users_db.sqlite' ")
    my_db_connection = sqlite3.connect('users_db.sqlite')
    print("Done")

    print("Get cursor object, which help us to execute SQL query on database ")
    my_db_cursor = my_db_connection.cursor()
    print("Done")

    print("Create table ")
    my_query = '''CREATE TABLE if not exists foodmin_table(
        RESTO_NAME    VARCHAR(100),
        FOOD_ITEM_ID INTEGER PRIMARY KEY AUTOINCREMENT,
        RESTO_LOCATION   VARCHAR(100),
        FOOD_ITEM_NAME  VARCHAR(100),
        PREPERATION_COST  INTEGER,
        SELLING_PRICE    INTEGER,
        DESCRIPTION    VARCHAR(100)

        )
        '''
    my_db_cursor.execute(my_query)
    print("Done")
    # ------------------------

    #  add new record to database and return account created successfully
    my_query = f"INSERT INTO FOODMIN_TABLE (RESTO_NAME , RESTO_LOCATION,FOOD_ITEM_NAME ,PREPERATION_COST , SELLING_PRICE ,DESCRIPTION ) VALUES('{entered_restoname}','{entered_restolocation}','{entered_foodname}', '{entered_preperationcost}', '{entered_sellingprice}', '{entered_description}')"
    my_db_cursor.execute(my_query)
    my_db_connection.commit()
    my_db_connection.close()
    return "We Received your form.  <a href='/'>Click Here To fill your qureirs</a>"

# END POINT - 9 : http://127.0.0.1:5000/foodmenu URL MAPPED to '/foofmenu'

@foodcourt_app.route('/foodmenu')
def my_foodmenu_page():
    return flask.render_template('foodmenu.html')

# END POINT - 10 : http://127.0.0.1:5000/logout URL MAPPED to '/logout'
# --------------------
@foodcourt_app.route('/logout')
def my_logout_page():
    session['username'] = None
    return flask.render_template('logout.html')
# --------------------


# Run the server
# --------------------
foodcourt_app.run()
# --------------------
