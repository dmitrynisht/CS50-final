from flask import Flask, flash, redirect, render_template, url_for, request, session
from flask_session import Session
from cs50 import SQL
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import mkappdir, login_required, apology
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

    submitMode = request.form.get("submitMode") or None

    if request.method == "POST":
        url = "customer_info"
        s_action = f"/{url}"

        if submitMode == "edit customer info":
            return redirect(
                        url_for(
                            url,
                            s_action=s_action,
                            submitMode=request.form.get("submitMode", submitMode),
                            fname=request.form.get("fname", ''),
                            lname=request.form.get("lname", ''),
                            email=request.form.get("email", ''),
                            id=request.form.get("id", ''),
                        )
                    )

        if submitMode == "new customer":
            return redirect(
                        url_for(
                            url,
                            s_action=s_action,
                            submitMode=request.form.get("submitMode", submitMode),
                            fname=request.form.get("fname", ''),
                            lname=request.form.get("lname", ''),
                            email=request.form.get("email", ''),
                        )
                    )

    s_action = "/customers"

    # Turn Off customer filters
    kwargs = {
        "dont_filter_by_fname": True,
        "dont_filter_by_lname": True,
        "dont_filter_by_email": True,
        "fname": '',
        "lname": '',
        "email": '',
    }

    fname = request.form.get("fname")
    lname = request.form.get("lname")
    email = request.form.get("email")

    if submitMode == "search customer":
        # Turn On customer filters
        if request.form.get("fname"):
            kwargs["dont_filter_by_fname"] = False
            kwargs["fname"] = fname

        if request.form.get("lname"):
            kwargs["dont_filter_by_lname"] = False
            kwargs["lname"] = lname

        if request.form.get("email"):
            kwargs["dont_filter_by_email"] = False
            kwargs["email"] = email

    if submitMode == "clear filter":
        fname = ''
        lname = ''
        email = ''

    customers = get_customers(kwargs=kwargs)

    return render_template("customers.html",
        s_action=request.args.get("s_action", s_action),
        customers=request.args.get("customers", customers),
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
        submitMode = request.form.get("submitMode") or ""
        
        fname = request.form.get("fname") or ""
        lname = request.form.get("lname") or ""
        email = request.form.get("email") or ""
        check_failed = False
        
        if submitMode == "new customer":
            # Ensure fname was submitted
            if not fname:
                check_failed = True
                error_msg = "must provide First name for customer"
                flash(error_msg)
            
            # Ensure lname was submitted
            if not lname:
                check_failed = True
                error_msg = "must provide Last name for customer"
                flash(error_msg)
            
            # Ensure email was submitted
            if not email:
                check_failed = True
                error_msg = "must provide Email for customer"
                flash(error_msg)
            
            if check_failed:
                return render_template("customer_info.html",
                        s_action=s_action,
                        fname = fname,
                        lname = lname,
                        email = email
                        )

            kwargs = {
                "fname": fname,
                "lname": lname,
                "email": email,
            }
            row = create_customer(kwargs=kwargs)
            submitMode == "edit customer info"

            return render_template("customer_info.html",
                    s_action=request.args.get("s_action", s_action),
                    submitMode = submitMode,
                    fname = fname,
                    lname = lname,
                    email = email
                    )
                    
        elif submitMode == "edit customer info":
            pass
        elif submitMode == "edit order details":
            pass
        elif submitMode == "new order":
            pass

    customer_orders = get_customer_orders(customer_id=1)

    return render_template("customer_info.html",
            s_action=request.args.get("s_action", s_action),
            submitMode = request.args.get("submitMode"),
            id=request.args.get("id", ''),
            fname=request.args.get("fname", ''),
            lname=request.args.get("lname", ''),
            email=request.args.get("email", ''),
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


def get_customers(*, kwargs):
    """Get customers. Optionaly filtered"""

    stmt = db_requests.stmt_sql_get_customers()
    rows = db.execute(stmt, **kwargs)

    return rows


def create_customer(*, kwargs):
    """"""

    stmt = db_requests.stmt_sql_ins_customer()
    rows = db.execute(stmt, **kwargs)
    
    return rows


def get_customer_orders(*, customer_id):
    """Search for orders by customer id provided"""

    return [
        {"id": 42, "number": 'order1', "date": ''},
        {"id": 113, "number": 'order4', "date": ''},
        {"id": 121, "number": 'order13', "date": ''},
    ]

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
