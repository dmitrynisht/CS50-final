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
        ctmr_id = request.form.get("ctmr_id", '')
        ctmr_uid = request.form.get("ctmr_uid", '')
        ctmr_fname = request.form.get("ctmr_fname", '')
        ctmr_lname = request.form.get("ctmr_lname", '')
        ctmr_email = request.form.get("ctmr_email", '')
        sktype_name = request.form.get("sktype_name", '')
        ctmr_contraindications = request.form.get("ctmr_contraindications", '')
        ctmr_additional_info = request.form.get("ctmr_additional_info", '')
        ctmr_subscribed = request.form.get("ctmr_subscribed", False)
        check_failed = False

        # Ensure fname was submitted
        if not ctmr_fname:
            check_failed = True
            error_msg = "must provide First name for customer"
            flash(error_msg)
        
        # Ensure lname was submitted
        if not ctmr_lname:
            check_failed = True
            error_msg = "must provide Last name for customer"
            flash(error_msg)

        # Ensure uid was submitted
        if not ctmr_uid:
            check_failed = True
            if not ctmr_fname or not ctmr_lname:
                error_msg = "must provide Unique Id for customer"
            else:
                error_msg = f"must provide Unique Id for customer\nit may look like: 'date{ctmr_fname[0]}{ctmr_lname}'"
            flash(error_msg)

        # Ensure email was submitted
        if not ctmr_email:
            check_failed = True
            error_msg = "must provide Email for customer"
            flash(error_msg)
        
        # Ensure skin type was submitted
        if not sktype_name:
            check_failed = True
            error_msg = "must provide Skin type for customer"
            flash(error_msg)

        if check_failed:
            pass
        else:
            # Query customers for email
            rows = get_customers(submitMode=submitMode, ctmr_email=ctmr_email)
            if len(rows) >= 1:
                row = rows[0]
                if str(row["ctmr_id"]) == ctmr_id:
                    # Lets check if there where other changes
                    if (row["ctmr_fname"], row["ctmr_lname"], row["ctmr_uid"]) == (ctmr_fname, ctmr_lname, ctmr_uid):
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
            rows = get_customers(submitMode=submitMode, ctmr_uid=ctmr_uid)
            if len(rows) >= 1:
                row = rows[0]
                if str(row["ctmr_id"]) == ctmr_id:
                    # Lets check if there where other changes
                    if (row["ctmr_fname"], row["ctmr_lname"], row["ctmr_email"]) == (ctmr_fname, ctmr_lname, ctmr_email):
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
            "ctmr_uid": ctmr_uid,
            "ctmr_fname": ctmr_fname,
            "ctmr_lname": ctmr_lname,
            "ctmr_email": ctmr_email,
            "sktype_name": sktype_name,
            "ctmr_contraindications": ctmr_contraindications,
            "ctmr_additional_info": ctmr_additional_info,
            "ctmr_subscribed": ctmr_subscribed,
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
    def generate_kwargs(*, submitMode, ctmr_fname='', ctmr_lname='', ctmr_email='', ctmr_uid='', **namedargs):
        kwargs = {
            "dont_filter_by_uid": True,
            "dont_filter_by_fname": True,
            "dont_filter_by_lname": True,
            "dont_filter_by_email": True,
            "ctmr_uid": '',
            "ctmr_fname": '',
            "ctmr_lname": '',
            "ctmr_email": '',
        }
        
        # Turn On customer filters
        if submitMode == "search customer":
            if ctmr_uid:
                kwargs["dont_filter_by_uid"] = False
                kwargs["ctmr_uid"] = ctmr_uid

            if ctmr_fname:
                kwargs["dont_filter_by_fname"] = False
                kwargs["ctmr_fname"] = ctmr_fname

            if ctmr_lname:
                kwargs["dont_filter_by_lname"] = False
                kwargs["ctmr_lname"] = ctmr_lname

            if ctmr_email:
                kwargs["dont_filter_by_email"] = False
                kwargs["ctmr_email"] = ctmr_email

        if submitMode in ["new customer", "edit customer info"]:
            if ctmr_email:
                kwargs["dont_filter_by_email"] = False
                kwargs["ctmr_email"] = ctmr_email
            
            if ctmr_uid:
                kwargs["dont_filter_by_uid"] = False
                kwargs["ctmr_uid"] = ctmr_uid

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
