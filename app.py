from flask import Flask, flash, redirect, render_template, url_for, request, session
from flask_session import Session
from cs50 import SQL
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime as dt
from helpers import mkappdir, filter_customers, validate_customer, login_required, apology
import db_requests


# Configure application
app = Flask(__name__)

# Create dummy secrey key so we can use sessions
app.config['SECRET_KEY'] = '123456790'

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkappdir()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
# Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///tiny_beauty.db")


@app.route("/")
@login_required
def index():
    """"""
    
    s_action = "/"
    
    # return render_template("index.html")
    return redirect("/customers")


@app.route("/customers", methods=["GET", "POST"])
@login_required
def customers():
    """List of customers"""

    submitMode = request.form.get("submitMode", 'clear filter')

    if request.method == "POST":
        url = "customer_info"
        s_action = f"/{url}"

        if submitMode in ["new customer", "edit customer info"]:
            return redirect(
                        url_for(
                            url,
                            s_action=s_action,
                            submitMode=request.form.get("submitMode", submitMode),
                            uid=request.form.get("uid", ''),
                            fname=request.form.get("fname", ''),
                            lname=request.form.get("lname", ''),
                            email=request.form.get("email", ''),
                            id=request.form.get("id", ''),
                        )
                    )

    s_action = "/customers"
    uid = request.form.get("uid", '')
    fname = request.form.get("fname", '')
    lname = request.form.get("lname", '')
    email = request.form.get("email", '')

    customers = get_customers(submitMode=submitMode, uid=uid, fname=fname, lname=lname, email=email)
    # customers = get_customers(kwargs=kwargs)

    if submitMode == "clear filter":
        uid = ''
        fname = ''
        lname = ''
        email = ''
        
    return render_template("customers.html",
        s_action=request.args.get("s_action", s_action),
        customers=request.args.get("customers", customers),
        uid=uid,
        fname=fname,
        lname=lname,
        email=email
        )


@app.route("/customer_info", methods=["GET", "POST"])
@login_required
def customer_info():
    """Customer info"""
    
    s_action = "/customer_info"

    if request.method == "POST":
        submitMode = request.form.get("submitMode", '')
        ctmr_id = request.form.get("id", '')
        uid = request.form.get("uid", '')
        fname = request.form.get("fname", '')
        lname = request.form.get("lname", '')
        email = request.form.get("email", '')

        if submitMode in ["new customer", "edit customer info"]:
            if submitMode == "new customer":
                try:
                    ctmr_id = create_customer(get_customers=get_customers, kwargs={})
                    submitMode = "edit customer info"
                except AssertionError:
                    error_msg = "Unverified data!"
                    ctmr_id = ""
                    flash(error_msg)
                except:
                    error_msg = "Customer already exists"
                    ctmr_id = ""
                    flash(error_msg)

                customer_orders = []

            else:
                # Implement better Exception handling:
                #   when check_failed Exception occured
                try:
                    rows = update_customer(get_customers=get_customers, kwargs={})
                except AssertionError:
                    error_msg = "Unverified data!"
                    flash(error_msg)
                except:
                    # Implement better Exception handling:
                    #   when check_failed Exception occured
                    error_msg = "SOMETHING WENT WRONG!"
                    flash(error_msg)

                customer_orders = get_customer_orders(ctmr_id=ctmr_id)
                # customer_orders = []

            return render_template("customer_info.html",
                    s_action=s_action,
                    submitMode=submitMode,
                    uid=uid,
                    fname=fname,
                    lname=lname,
                    email=email,
                    id=ctmr_id,
                    orders=customer_orders
                    )

        elif submitMode == "edit order details":
            pass
        elif submitMode == "new order":
            pass
    
    else:
        # request.method == 'GET'
        s_action = request.args.get("s_action", s_action)
        submitMode = request.args.get("submitMode", '')
        ctmr_id = request.args.get("id", '')
        uid = request.args.get("uid", '')
        fname = request.args.get("fname", '')
        lname = request.args.get("lname", '')
        email = request.args.get("email", '')

    if submitMode == "new customer":
        customer_orders = []
    elif submitMode == "edit customer info":
        # customer_orders = []
        customer_orders = get_customer_orders(ctmr_id=ctmr_id)
    else:
        submitMode = "new customer"
        customer_orders = []
        fname = ""
        lname = ""
        email = ""
        ctmr_id = ""
        uid = ""

    return render_template("customer_info.html",
            s_action=s_action,
            submitMode=submitMode,
            uid=uid,
            fname=fname,
            lname=lname,
            email=email,
            id=ctmr_id,
            orders=request.args.get("orders", customer_orders)
            )


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    s_action = "/login"

    # Forget any user_id
    if 'usr_id' in session:
        session.clear()
    
    ###-start-#######################
    opengate = False
    # opengate = True
    if opengate:
        # temp gate: user_id provided or not provided
        #   if not provided - testing /login route
        #   if provided - ommiting /login route - testing /index
        authenticated = False
        authenticated = True
        if authenticated:
            session["usr_id"] = 1
            session["usr_login"] = "admin"
            # Redirect user to home page
            return redirect("/")
        else:
            # User reached route via GET (as by clicking a link or via redirect)
            return render_template("login.html", s_action=s_action)
    ###-finish-#######################

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        
        username = request.form.get("username")
        
        # Ensure username was submitted
        if not username:
            error_msg = "must provide username (login)"
            flash(error_msg)
            return render_template("login.html", s_action=s_action)

        password = request.form.get("password")
        
        # Ensure password was submitted
        if not password:
            error_msg = "must provide password"
            flash(error_msg)
            return render_template("login.html", s_action=s_action, 
                username=request.args.get("username", username)
            )

        # Query database for username
        rows = get_user(username=username)

        # Ensure username exists
        if len(rows) != 1:
            error_msg = "invalid username"
            flash(error_msg)
            return render_template("login.html", s_action=s_action, 
                username=request.args.get("username", username),
                password=request.args.get("password", password)
            )

        # Ensure password is correct
        if not check_password_hash(rows[0]["usr_hash"], password):
            error_msg = "invalid password"
            flash(error_msg)
            return render_template("login.html", s_action=s_action, 
                username=request.args.get("username", username),
                password=request.args.get("password", password)
            )
            
        # Remember which user has logged in
        session["usr_id"] = rows[0]["usr_id"]
        session["usr_login"] = rows[0]["usr_login"]
        
        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    return render_template("login.html", s_action=s_action)


def get_user(*, username):
    """Search for user by username provided"""

    stmt = db_requests.stmt_sql_get_user()
    rows = db.execute(stmt, usr_login=username)

    return rows


@filter_customers
def get_customers(*, kwargs):
    """Get customers. Optionaly filtered"""

    stmt = db_requests.stmt_sql_get_customers()
    rows = db.execute(stmt, **kwargs)

    return rows


@validate_customer
def create_customer(*, kwargs):
    """"""

    stmt = db_requests.stmt_sql_ins_customer()
    rows = db.execute(stmt, **kwargs)
    
    return rows


@validate_customer
def update_customer(*, kwargs):
    """"""
    
    stmt = db_requests.stmt_sql_upd_customer()
    rows = db.execute(stmt, **kwargs)
    
    return rows


def get_customer_orders(**kwargs):
    """Search for orders by customer id provided"""

    stmt = db_requests.stmt_sql_get_customer_orders()
    rows = db.execute(stmt, **kwargs)
    
    return rows

@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    # session.clear()

    # Redirect user to login form
    return redirect(url_for("login"))


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


def main(argv=None):
    if argv is None:
        argv = sys.argv

    print('hello world')

    # with app.test_request_context():
    #     testingrequests()
    # generate_password_hash(request.form.get("password"))
    # from datetime import datetime as dt
    # from datetime import timezone
    # transacted = dt.now(timezone.utc).isoformat()
    # ordered = dt.now().isoformat()
    # date_string = '2022-10-14T09:01:40.319631'
    # vartime = dt.fromisoformat(date_string)

    pass

    # Start app
    app.run(debug=True)

    s ='stop'


if __name__ == '__main__':
    import sys
    sys.exit(main())

else:
    # Listen for errors
    for code in default_exceptions:
        app.errorhandler(code)(errorhandler)
