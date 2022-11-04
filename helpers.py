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
