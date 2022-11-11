from flask import redirect, render_template, session
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
