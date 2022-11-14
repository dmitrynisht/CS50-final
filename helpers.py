from flask import flash, redirect, render_template, request, session
from functools import wraps


def mkappdir():
    """Creating session tempdir"""
    
    from tempfile import gettempdir, mkdtemp
    import os
    
    app_dir = 'CS50_tiny_beauty'
    tmp_dir = gettempdir()
    dir = os.path.join(tmp_dir, app_dir)
    try:
        os.mkdir(dir, 0o700)
    except FileExistsError:
        pass # already exists

    app_dir_prefix = 'cs50_'
    app_dir_suffix = ''

    return mkdtemp(prefix=app_dir_prefix, suffix=app_dir_suffix, dir=dir)


def validate_customer(func):
    """
    Decorate create_customer() to provide data validation before update/create
    """
    @wraps(func)
    def decorated_function(*args, get_customers, **kwargs):
        submitMode = request.form.get("submitMode", '')
        ctmr_id = request.form.get("id", '')
        uid = request.form.get("uid", '')
        fname = request.form.get("fname", '')
        lname = request.form.get("lname", '')
        email = request.form.get("email", '')
        check_failed = False

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

        # Ensure uid was submitted
        if not uid:
            check_failed = True
            if not fname or not lname:
                error_msg = "must provide Unique Id for customer"
            else:
                error_msg = f"must provide Unique Id for customer\nit may look like: 'date{fname[0]}{lname}'"
            flash(error_msg)

        # Ensure email was submitted
        if not email:
            check_failed = True
            error_msg = "must provide Email for customer"
            flash(error_msg)

        if check_failed:
            pass
        else:
            # Query customers for email
            rows = get_customers(submitMode=submitMode, email=email)
            if len(rows) >= 1:
                row = rows[0]
                if str(row["id"]) == ctmr_id:
                    # Lets check if there where other changes
                    if (row["fname"], row["lname"], row["uid"]) == (fname, lname, uid):
                        check_failed = True

                else:
                    # Email already used
                    check_failed = True
                    error_msg = "Email already used"
                    flash(error_msg)
            
        if check_failed:
            pass
        else:
            # Query customers for uid
            rows = get_customers(submitMode=submitMode, uid=uid)
            if len(rows) >= 1:
                row = rows[0]
                if str(row["id"]) == ctmr_id:
                    # Lets check if there where other changes
                    if (row["fname"], row["lname"], row["email"]) == (fname, lname, email):
                        check_failed = True
                else:
                    # uid already used
                    check_failed = True
                    error_msg = "Unique ID already used"
                    flash(error_msg)

        if check_failed:
            # Implement better Exception handling
            assert False, "Unverified data!"

        kwargs = {
            "uid": uid,
            "fname": fname,
            "lname": lname,
            "email": email,
        }

        if submitMode == "edit customer info":
            kwargs["ctmr_id"] = ctmr_id

        return func(kwargs=kwargs)
        
    return decorated_function


def filter_customers(func):
    """
    Decorate get_customers() to provide kwargs for request
    """
    @wraps(func)
    def generate_kwargs(*, submitMode, fname='', lname='', email='', uid='', **namedargs):
        kwargs = {
            "dont_filter_by_uid": True,
            "dont_filter_by_fname": True,
            "dont_filter_by_lname": True,
            "dont_filter_by_email": True,
            "uid": '',
            "fname": '',
            "lname": '',
            "email": '',
        }
        
        # Turn On customer filters
        if submitMode == "search customer":
            if uid:
                kwargs["dont_filter_by_uid"] = False
                kwargs["uid"] = uid

            if fname:
                kwargs["dont_filter_by_fname"] = False
                kwargs["fname"] = fname

            if lname:
                kwargs["dont_filter_by_lname"] = False
                kwargs["lname"] = lname

            if email:
                kwargs["dont_filter_by_email"] = False
                kwargs["email"] = email

        if submitMode in ["new customer", "edit customer info"]:
            if email:
                kwargs["dont_filter_by_email"] = False
                kwargs["email"] = email
            
            if uid:
                kwargs["dont_filter_by_uid"] = False
                kwargs["uid"] = uid

        return func(kwargs=kwargs)

    return generate_kwargs


def login_required(f):
    """
    Decorate routes to require login.

    https://flask.palletsprojects.com/en/1.1.x/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("usr_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function


def apology(message, code=400):
    """Render message as an apology to user."""
    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [("-", "--"), (" ", "-"), ("_", "__"), ("?", "~q"),
                         ("%", "~p"), ("#", "~h"), ("/", "~s"), ("\"", "''")]:
            s = s.replace(old, new)
        return s
    return render_template("apology.html", top=code, bottom=escape(message)), code
