from flask import flash, redirect, render_template, request, session
from functools import wraps
from datetime import datetime as dt


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


def validate_customer_order(func):
    """
    Decorate create_order_details() and update_order_details()
    provide data validation before update/create customer's order
    """
    @wraps(func)
    def decorated_function(*args, get_order_details, requestMethod, **kwargs):
        if requestMethod == "POST":
            submitMode = request.form.get("submitMode", '')
            ord_id = request.form.get("ord_id", '')
            ord_number = request.form.get("ord_number", '')
            ord_status = request.form.get("ord_status", '')
            ord_appointment_date = request.form.get("ord_appointment_date", '')
            ord_beautician = request.form.get("ord_beautician", '')
            ord_description = request.form.get("ord_description", '')
            ord_ctmr_complaints = request.form.get("ord_ctmr_complaints", '')
            ord_skin_condition = request.form.get("ord_skin_condition", '')
        else:
            submitMode = request.args.get("submitMode", '')
            ord_id = request.args.get("ord_id", '')
            ord_number = request.args.get("ord_number", '')
            ord_status = request.args.get("ord_status", '')
            ord_appointment_date = request.args.get("ord_appointment_date", '')
            ord_beautician = request.args.get("ord_beautician", '')
            ord_description = request.args.get("ord_description", '')
            ord_ctmr_complaints = request.args.get("ord_ctmr_complaints", '')
            ord_skin_condition = request.args.get("ord_skin_condition", '')

        ord_appointment_date = dt.fromisoformat(ord_appointment_date)
        ord_appointment_date = ord_appointment_date.isoformat()
        check_failed = False
        error_msg = ""

        # Ensure ord_number was submitted
        if not ord_number:
            check_failed = True
            error_msg = "must provide unique Order number for order"

        # Ensure ord_status was submitted
        if not ord_status:
            check_failed = True
            error_msg = "must provide Order status"

        # Ensure ord_appointment_date was submitted
        if not ord_appointment_date:
            check_failed = True
            error_msg = "must provide Appointment date for order"

        # Ensure ord_beautician was submitted
        if not ord_beautician:
            check_failed = True
            error_msg = "must provide Beautician for order"

        if check_failed:
            pass
        else:
            rows = get_order_details(ord_id=ord_id)
            if len(rows) >= 1:
                row = rows[0]
                if (row["ord_number"], row["ord_status"], dt.fromisoformat(row["ord_appointment_date"]), row["ord_beautician"], row["ord_description"], row["ord_ctmr_complaints"], row["ord_skin_condition"]) == (ord_number, ord_status, dt.fromisoformat(ord_appointment_date), ord_beautician, ord_description, ord_ctmr_complaints, ord_skin_condition):
                    check_failed = False
                    error_msg = "Nothing to change"
                    return []
            else:
                check_failed = True
                error_msg = "Unexpected mistake while processing order details. No order found by provided ID"

        if check_failed:
            # Implement better Exception handling
            assert False, error_msg

        kwargs = {
            "ord_number": ord_number,
            "ord_status": ord_status,
            "ord_appointment_date": ord_appointment_date,
            "ord_beautician": ord_beautician,
            "ord_description": ord_description,
            "ord_ctmr_complaints": ord_ctmr_complaints,
            "ord_skin_condition": ord_skin_condition,
        }

        if submitMode == "edit order details":
            kwargs["ord_id"] = ord_id

        return func(kwargs=kwargs)

    return decorated_function


def validate_customer(func):
    """
    Decorate create_customer() and update_customer() to provide data validation before update/create
    """
    @wraps(func)
    def decorated_function(*args, get_customers, requestMethod, **kwargs):
        if requestMethod == "POST":
            submitMode = request.form.get("submitMode", '')
            ctmr_id = request.form.get("ctmr_id", '')
            ctmr_uid = request.form.get("ctmr_uid", '')
            ctmr_fname = request.form.get("ctmr_fname", '')
            ctmr_lname = request.form.get("ctmr_lname", '')
            ctmr_gender = request.form.get("ctmr_gender", '')
            ctmr_email = request.form.get("ctmr_email", '')
            sktype_name = request.form.get("sktype_name", '')
            ctmr_contraindications = request.form.get("ctmr_contraindications", '')
            ctmr_additional_info = request.form.get("ctmr_additional_info", '')
            ctmr_subscribed = request.form.get("ctmr_subscribed", '0')
        else:
            submitMode = request.args.get("submitMode", '')
            ctmr_id = request.args.get("ctmr_id", '')
            ctmr_uid = request.args.get("ctmr_uid", '')
            ctmr_fname = request.args.get("ctmr_fname", '')
            ctmr_lname = request.args.get("ctmr_lname", '')
            ctmr_gender = request.args.get("ctmr_gender", '')
            ctmr_email = request.args.get("ctmr_email", '')
            sktype_name = request.args.get("sktype_name", '')
            ctmr_contraindications = request.args.get("ctmr_contraindications", '')
            ctmr_additional_info = request.args.get("ctmr_additional_info", '')
            ctmr_subscribed = request.args.get("ctmr_subscribed", '0')

        ctmr_subscribed = int(ctmr_subscribed)
        check_failed = False
        error_msg = ""

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

        # Ensure skin type was submitted
        if not ctmr_gender:
            check_failed = True
            error_msg = "must provide Gender for customer"
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
                    if (row["ctmr_fname"], row["ctmr_lname"], row["ctmr_uid"], row["ctmr_gender"], row["sktype_name"], row["ctmr_contraindications"], row["ctmr_additional_info"], row["ctmr_subscribed"]) == (ctmr_fname, ctmr_lname, ctmr_uid, ctmr_gender, sktype_name, ctmr_contraindications, ctmr_additional_info, ctmr_subscribed):
                        check_failed = True
                        error_msg = "Nothing to change"
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
                    if (row["ctmr_fname"], row["ctmr_lname"], row["ctmr_email"], row["ctmr_gender"], row["sktype_name"], row["ctmr_contraindications"], row["ctmr_additional_info"], row["ctmr_subscribed"]) == (ctmr_fname, ctmr_lname, ctmr_email, ctmr_gender, sktype_name, ctmr_contraindications, ctmr_additional_info, ctmr_subscribed):
                        check_failed = True
                        error_msg = "Nothing to change"
                else:
                    # uid already used
                    check_failed = True
                    error_msg = "Unique ID already used"
                    flash(error_msg)

        if check_failed:
            # Implement better Exception handling
            assert False, error_msg

        kwargs = {
            "ctmr_uid": ctmr_uid,
            "ctmr_fname": ctmr_fname,
            "ctmr_lname": ctmr_lname,
            "ctmr_email": ctmr_email,
            "ctmr_gender": ctmr_gender,
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
    def generate_kwargs(*, submitMode, ctmr_fname='', ctmr_lname='', ctmr_email='', ctmr_uid='', ctmr_id='', **namedargs):
        kwargs = {
            "dont_filter_by_uid": True,
            "dont_filter_by_fname": True,
            "dont_filter_by_lname": True,
            "dont_filter_by_email": True,
            "dont_filter_by_id": True,
            "ctmr_uid": '',
            "ctmr_fname": '',
            "ctmr_lname": '',
            "ctmr_email": '',
            "ctmr_id": '',
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
            
            if ctmr_id:
                kwargs["dont_filter_by_id"] = False
                kwargs["ctmr_uid"] = ctmr_id

        if submitMode in ["new customer", "edit customer info"]:
            if ctmr_email:
                kwargs["dont_filter_by_email"] = False
                kwargs["ctmr_email"] = ctmr_email
            
            if ctmr_uid:
                kwargs["dont_filter_by_uid"] = False
                kwargs["ctmr_uid"] = ctmr_uid

            if ctmr_id:
                kwargs["dont_filter_by_id"] = False
                kwargs["ctmr_id"] = ctmr_id

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
