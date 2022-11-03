from flask import Flask, render_template, request, session
from flask_session import Session
from cs50 import SQL
from helpers import mkappdir


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
def index():
    """List of top customers"""

    s_action = "/"

    # session["user_id"] = 1
    # session["username"] = "admin"

    return render_template("customers.html", s_action=request.args.get("s_action", s_action))
    # return render_template("index.html")


def main(argv=None):
    if argv is None:
        argv = sys.argv

    print('hello world')

    # with app.test_request_context():
    #     testingrequests()
    #
    
    # Start app
    app.run(debug=True)

    s ='stop'


if __name__ == '__main__':
    import sys
    sys.exit(main())