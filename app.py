from flask import Flask, flash, redirect, render_template, url_for, request, session
from flask_session import Session
from cs50 import SQL
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime as dt
from helpers import mkappdir, filter_customers, validate_customer, validate_customer_order, login_required, apology
import db_requests, json


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
                            ctmr_id=request.form.get("ctmr_id", ''),
                        )
                    )

    s_action = "/customers"
    ctmr_uid = request.form.get("ctmr_uid", '')
    ctmr_fname = request.form.get("ctmr_fname", '')
    ctmr_lname = request.form.get("ctmr_lname", '')
    ctmr_email = request.form.get("ctmr_email", '')

    customers = get_customers(submitMode=submitMode, ctmr_uid=ctmr_uid, ctmr_fname=ctmr_fname, ctmr_lname=ctmr_lname, ctmr_email=ctmr_email)
    # customers = get_customers(kwargs=kwargs)

    if submitMode == "clear filter":
        ctmr_uid = ''
        ctmr_fname = ''
        ctmr_lname = ''
        ctmr_email = ''
        
    return render_template("customers.html",
        s_action=request.args.get("s_action", s_action),
        customers=request.args.get("customers", customers),
        ctmr_uid=ctmr_uid,
        ctmr_fname=ctmr_fname,
        ctmr_lname=ctmr_lname,
        ctmr_email=ctmr_email
        )


@app.route("/customer_info", methods=["GET", "POST"])
@login_required
def customer_info():
    """Customer info"""
    
    s_action = "/customer_info"

    if request.method == "POST":
        submitMode = request.form.get("submitMode", '')
        if submitMode in ["new order", "edit order details"]:
            url = "svc_order_details"
            s_action = f"/{url}"
            
            order_kwargs = {
                "ord_id": request.form.get("ord_id", ''),
                # "ord_number": request.form.get("ord_number", ''),
                # "ord_appointment_date": request.form.get("ord_appointment_date", ''),
                # following args are not present in form and beeing passed through args
                "ctmr_uid": request.args.get("ctmr_uid", ''),
                "ctmr_fname": request.args.get("ctmr_fname", ''),
                "ctmr_lname": request.args.get("ctmr_lname", ''),
                "ctmr_gender": request.args.get("ctmr_gender", ''),
                "ctmr_email": request.args.get("ctmr_email", ''),
                "ctmr_contraindications": request.args.get("ctmr_contraindications", ''),
                "ctmr_additional_info": request.args.get("ctmr_additional_info", ''),
            }
            return redirect(
                        url_for(
                            url,
                            s_action=s_action,
                            submitMode=submitMode,
                            **order_kwargs
                        )
                    )
    
    else:
        # request.method == 'GET'
        s_action = request.args.get("s_action", s_action)
        submitMode = request.args.get("submitMode", 'new customer')
        ctmr_id = request.args.get("ctmr_id", '')
        if submitMode == "new customer":
            customer_orders = []
            ctmr_fname = ""
            ctmr_lname = ""
            ctmr_email = ""
            ctmr_gender = ""
            sktype_name = ""
            ctmr_contraindications = ""
            ctmr_additional_info = ""
            ctmr_subscribed = '0'
            ctmr_id = ""
            ctmr_uid = ""
        else:
            rows = get_customer_info(submitMode=submitMode, ctmr_id=ctmr_id)
            ctmrInfo = rows[0]
            ctmr_uid = ctmrInfo["ctmr_uid"] if "ctmr_uid" in ctmrInfo else ''
            ctmr_fname = ctmrInfo["ctmr_fname"] if "ctmr_fname" in ctmrInfo else ''
            ctmr_lname = ctmrInfo["ctmr_lname"] if "ctmr_lname" in ctmrInfo else ''
            ctmr_gender = ctmrInfo["ctmr_gender"] if "ctmr_gender" in ctmrInfo else ''
            ctmr_email = ctmrInfo["ctmr_email"] if "ctmr_email" in ctmrInfo else ''
            sktype_name = ctmrInfo["sktype_name"] if "sktype_name" in ctmrInfo else ''
            ctmr_contraindications = ctmrInfo["ctmr_contraindications"] if "ctmr_contraindications" in ctmrInfo else ''
            ctmr_additional_info = ctmrInfo["ctmr_additional_info"] if "ctmr_additional_info" in ctmrInfo else ''
            ctmr_subscribed = str(ctmrInfo["ctmr_subscribed"]) if "ctmr_subscribed" in ctmrInfo else '0'

    if submitMode == "edit customer info":
        customer_orders = get_customer_orders(ctmr_id=ctmr_id)

    return render_template("customer_info.html",
            s_action=s_action,
            submitMode=submitMode,
            ctmr_uid=ctmr_uid,
            ctmr_fname=ctmr_fname,
            ctmr_lname=ctmr_lname,
            ctmr_gender=ctmr_gender,
            ctmr_email=ctmr_email,
            sktype_name=sktype_name,
            ctmr_contraindications=ctmr_contraindications,
            ctmr_additional_info=ctmr_additional_info,
            ctmr_subscribed=ctmr_subscribed,
            ctmr_id=ctmr_id,
            orders=request.args.get("orders", customer_orders),
            sktypes=get_skin_types(),
            genders=get_genders(),
            )


@app.route("/save_customer_info", methods=["GET", "POST"])
@login_required
def save_customer_info():
    """Save customer info"""

    trn_data = {
        'trn_complete': False,
        'error_msg': "",
    }

    requestMethod = request.method
    if requestMethod == "POST":
        submitMode = request.form.get("submitMode", '')
    else:
        submitMode = request.args.get("submitMode", '')

    if submitMode in ["new customer", "edit customer info"]:
        if submitMode == "new customer":
            # generate_UID
            # ctmr_uid = 
            try:
                # create_customer() is decorated by validate_customer()
                # validate_customer() invokes get_customers()/get_customer_info() which is passed by name to get_customers argument
                ctmr_id = create_customer(get_customers=get_customer_info, requestMethod=requestMethod, kwargs={})
                submitMode = "edit customer info"
                trn_data['trn_complete'] = True

            except AssertionError as error_msg:
                ctmr_id = ""
                # error_msg = "Unverified data!"
                # flash(error_msg)
                trn_data["error_msg"] = error_msg

            except:
                error_msg = "Customer already exists"
                ctmr_id = ""
                # flash(error_msg)
                trn_data["error_msg"] = error_msg

        else:
            # Implement better Exception handling:
            #   when check_failed Exception occured
            try:
                # update_customer() is decorated by validate_customer()
                # validate_customer() invokes get_customers()/get_customer_info() which is passed by name to get_customers argument
                rows = update_customer(get_customers=get_customer_info, requestMethod=requestMethod, kwargs={})
                trn_data['trn_complete'] = True

            except AssertionError as error_msg:
                # error_msg = "Unverified data!"
                # flash(error_msg)
                trn_data["error_msg"] = error_msg.args

            except:
                # Implement better Exception handling:
                #   when check_failed Exception occured
                error_msg = "SOMETHING WENT WRONG!"
                # flash(error_msg)
                trn_data["error_msg"] = error_msg

    return trn_data


@app.route("/svc_order_details", methods=["GET", "POST"])
@login_required
def svc_order_details():
    """Order details"""

    s_action = "/svc_order_details"
    submitMode = request.args.get("submitMode", '')
    ord_id=request.args.get("ord_id", '')
    if submitMode == "edit order details":
        # retrieve order details
        rows = get_service_order_details(ord_id=ord_id)
        order_details = rows[0]
        ord_id = order_details["ord_id"]
        ord_number = order_details["ord_number"]
        ord_status = order_details["ord_status"]
        ord_date = order_details["ord_date"]
        ord_appointment_date = order_details["ord_appointment_date"]
        ord_beautician = order_details["ord_beautician"]
        ord_description = order_details["ord_description"]
        ord_ctmr_complaints = order_details["ord_ctmr_complaints"]
        ord_skin_condition = order_details["ord_skin_condition"]
        tbdOrderDetails = get_service_rendered(ord_number=ord_number)
        tbdHomeSkinCare = get_service_homecare(ord_number=ord_number)
        tbdTreatmentPlan = get_treatment_plan(ord_number=ord_number)
    else:
        ord_number=request.args.get("ord_number", '')
        ord_date=request.args.get("ord_date", '')
        ord_appointment_date=request.args.get("ord_appointment_date", '')
        tbdOrderDetails = []
        tbdHomeSkinCare = []
        tbdTreatmentPlan = []

    return render_template("svc_order_details.html",
            s_action=s_action,
            submitMode=submitMode,
            ord_id=ord_id,
            ord_number=ord_number,
            ord_status=ord_status,
            ord_date=ord_date,
            ord_appointment_date=ord_appointment_date,
            ord_beautician=ord_beautician,
            ord_description=ord_description,
            ord_ctmr_complaints=ord_ctmr_complaints,
            ord_skin_condition=ord_skin_condition,
            ctmr_uid=request.args.get("ctmr_uid", ''),
            ctmr_fname=request.args.get("ctmr_fname", ''),
            ctmr_lname=request.args.get("ctmr_lname", ''),
            ctmr_gender=request.args.get("ctmr_gender", ''),
            ctmr_email=request.args.get("ctmr_email", ''),
            ctmr_contraindications=request.args.get("ctmr_contraindications", ''),
            ctmr_additional_info=request.args.get("ctmr_additional_info", ''),
            ordStatusList=get_statusList(),
            ordBeauticiansList=get_usersByRole(role_name="beautician"),
            tbdOrderDetails=tbdOrderDetails,
            tbdHomeSkinCare=tbdHomeSkinCare,
            tbdTreatmentPlan=tbdTreatmentPlan,
            )


@app.route("/save_order_details", methods=["GET", "POST"])
@login_required
def save_order_details():
    """Save detailed order info"""

    trn_data = {
        'trn_complete': False,
        'error_msg': "",
    }

    requestMethod = request.method
    if requestMethod == "POST":
        submitMode = request.form.get("submitMode", '')
    else:
        submitMode = request.args.get("submitMode", '')

    if submitMode in ["new order", "edit order details"]:
        if submitMode == "new order":
            try:
                # do something here
                # rows = save_order_details()
                pass

            except:pass

        else:
            try:
                # update_order_details() is decorated by validate_customer_order()
                # validate_customer_order() invokes get_service_order_details() which is passed by name to get_order_details argument
                rows = update_order_details(get_order_details=get_service_order_details, requestMethod=requestMethod, kwargs={})

                rows = update_services_rendered(requestMethod=requestMethod, kwargs={})
                
                rows = update_services_homecare(requestMethod=requestMethod, kwargs={})

                rows = update_treatment_plan(requestMethod=requestMethod, kwargs={})

                trn_data['trn_complete'] = True

            except AssertionError as error_msg:
                trn_data["error_msg"] = error_msg.args
                
            except:
                error_msg = "SOMETHING WENT WRONG!"
                trn_data["error_msg"] = error_msg

    return trn_data


@app.route("/edit_product_list", methods=["GET", "POST"])
@login_required
def edit_product_list():
    """"""

    trn_data = {
        'trn_complete': False,
        # 'ctmr_id':        total,
    }

    requestMethod = request.method
    if requestMethod == "POST":
        submitMode = request.form.get("submitMode", '')
        ptype = request.form.get("ptype", '')
    else:
        submitMode = request.args.get("submitMode", '')
        ptype = request.args.get("ptype", '')
    
    # ptype = "service"
    productList = get_services(ptype=ptype)
    
    trn_data = {
        'trn_complete': True,
        'productList': productList,
    }

    return trn_data


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    s_action = "/login"

    # Forget any user_id
    if 'usr_id' in session:
        session.clear()
    
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


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    # session.clear()

    # Redirect user to login form
    return redirect(url_for("login"))


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


@filter_customers
def get_customer_info(*, kwargs):
    """Retrieve all data by customer id provided"""
    
    stmt = db_requests.stmt_sql_get_customer_info()
    rows = db.execute(stmt, **kwargs)
    
    return rows


@validate_customer
def create_customer(*, kwargs):
    """Insert new customer"""

    stmt = db_requests.stmt_sql_ins_customer()
    rows = db.execute(stmt, **kwargs)
    
    return rows


@validate_customer
def update_customer(*, kwargs):
    """Update customer's info"""
    
    stmt = db_requests.stmt_sql_upd_customer()
    rows = db.execute(stmt, **kwargs)
    
    return rows


def get_customer_orders(**kwargs):
    """Search for orders by customer id provided"""

    stmt = db_requests.stmt_sql_get_customer_orders()
    rows = db.execute(stmt, **kwargs)
    
    return rows


def get_service_order_details(**kwargs):
    """Retrieve all data by service order id provided"""

    stmt = db_requests.stmt_sql_get_customer_order_info()
    rows = db.execute(stmt, **kwargs)
    
    return rows


@validate_customer_order
def update_order_details(*, kwargs):
    """Update customer's order details"""
    
    stmt = db_requests.stmt_sql_upd_customer_order()
    rows = db.execute(stmt, **kwargs)
    
    return rows


# @validate_services_rendered
def update_services_rendered(*, requestMethod, kwargs):
    """Update services rendered within order"""

    if requestMethod == "POST":
        ord_number = request.form.get("ord_number", '')
        ord_status = request.form.get("ord_status", '')
        tbl_service_rendered_new = request.form.get("tbl_service_rendered", '')
    else:
        ord_number = request.args.get("ord_number", '')
        ord_status = request.args.get("ord_status", '')
        tbl_service_rendered_new = request.args.get("tbl_service_rendered", '')

    tbl_service_rendered_new = json.loads(tbl_service_rendered_new)
    # validating data for changes
    tbl_service_rendered_old = get_service_rendered(ord_number=ord_number)
    new_t = tuple(svr["product"] for svr in tbl_service_rendered_new)
    old_t = tuple(svr["product"] for svr in tbl_service_rendered_old)
    if new_t == old_t:
        return []
    # data was modified clear old rendered services
    rows = clear_old_rendered_services(ord_number=ord_number)

    rows = []
    kwargs = {
        "ord_number": ord_number,
        "ord_status": ord_status,
    }
    stmt = db_requests.stmt_sql_ins_service_rendered()
    for service in tbl_service_rendered_new:
        kwargs.update(dict(service))
        row = db.execute(stmt, **kwargs)
        rows.append(row)

    return rows


# @validate_services_rendered
def update_services_homecare(*, requestMethod, kwargs):
    """Update services rendered within order"""

    if requestMethod == "POST":
        ord_number = request.form.get("ord_number", '')
        tbl_service_homecare_new = request.form.get("tbl_service_homecare", '')
    else:
        ord_number = request.args.get("ord_number", '')
        tbl_service_homecare_new = request.args.get("tbl_service_homecare", '')

    tbl_service_homecare_new = json.loads(tbl_service_homecare_new)
    # validating data for changes
    tbl_service_homecare_old = get_service_homecare(ord_number=ord_number)
    new_t = tuple(shc["product"] for shc in tbl_service_homecare_new)
    old_t = tuple(shc["product"] for shc in tbl_service_homecare_old)
    if new_t == old_t:
        return []
    # data was modified clear old homecare services
    rows = clear_old_service_homecare(ord_number=ord_number)

    rows = []
    kwargs = {
        "ord_number": ord_number,
    }
    stmt = db_requests.stmt_sql_ins_service_homecare()
    for homecare in tbl_service_homecare_new:
        kwargs.update(dict(homecare))
        row = db.execute(stmt, **kwargs)
        rows.append(row)

    return rows


def update_treatment_plan(*, requestMethod, kwargs):
    """Update treatment plan within order"""

    if requestMethod == "POST":
        ord_number = request.form.get("ord_number", '')
        tbl_treatment_plan_new = request.form.get("tbl_treatment_plan", '')
    else:
        ord_number = request.args.get("ord_number", '')
        tbl_treatment_plan_new = request.args.get("tbl_treatment_plan", '')

    tbl_treatment_plan_new = json.loads(tbl_treatment_plan_new)
    # validating data for changes
    tbl_treatment_plan_old = get_treatment_plan(ord_number=ord_number)
    new_t = tuple(stp["product"] for stp in tbl_treatment_plan_new)
    old_t = tuple(stp["product"] for stp in tbl_treatment_plan_old)
    if new_t == old_t:
        return []
    # data was modified clear old treatment plan
    rows = clear_old_treatment_plan(ord_number=ord_number)
    
    rows = []
    kwargs = {
        "ord_number": ord_number,
    }
    stmt = db_requests.stmt_sql_ins_service_trt_plan()
    for homecare in tbl_treatment_plan_new:
        kwargs.update(dict(homecare))
        row = db.execute(stmt, **kwargs)
        rows.append(row)

    return rows


def get_service_rendered(**kwargs):
    """Get services rendered within order"""

    stmt = db_requests.stmt_sql_get_service_rendered()
    rows = db.execute(stmt, **kwargs)
    
    return rows


def clear_old_rendered_services(**kwargs):
    """Delete rendered services within order"""

    stmt = db_requests.stmt_sql_del_services_rendered()
    rows = db.execute(stmt, **kwargs)
    
    return rows


def get_service_homecare(**kwargs):
    """Get homecare products within order"""

    stmt = db_requests.stmt_sql_get_service_homecare()
    rows = db.execute(stmt, **kwargs)
    
    return rows


def clear_old_service_homecare(**kwargs):
    """Delete home care recommendations within order"""

    stmt = db_requests.stmt_sql_del_service_homecare()
    rows = db.execute(stmt, **kwargs)
    
    return rows


def get_treatment_plan(**kwargs):
    """Get treatment plan within order"""

    stmt = db_requests.stmt_sql_get_service_trt_plan()
    rows = db.execute(stmt, **kwargs)
    
    return rows


def clear_old_treatment_plan(**kwargs):
    """Delete treatment plan within order"""

    stmt = db_requests.stmt_sql_del_service_trt_plan()
    rows = db.execute(stmt, **kwargs)
    
    return rows


def get_skin_types(**kwargs):
    """Get list of skin types"""

    stmt = db_requests.stmt_sql_get_skin_types()
    rows = db.execute(stmt, **kwargs)
    
    return rows


def get_genders(**kwargs):
    """Get list of skin types"""

    stmt = db_requests.stmt_sql_get_genders()
    rows = db.execute(stmt, **kwargs)
    
    return rows


def get_services(**kwargs):
    """Get products filtered by product_type"""
    
    stmt = db_requests.stmt_sql_get_services()
    rows = db.execute(stmt, **kwargs)

    return rows


def get_statusList(**kwargs):
    """Get all values for order_status available"""
    
    stmt = db_requests.stmt_sql_get_status_list()
    rows = db.execute(stmt, **kwargs)

    return rows


def get_usersByRole(**kwargs):
    """Get all users filtered by role"""
    
    stmt = db_requests.stmt_sql_get_users_list()
    rows = db.execute(stmt, **kwargs)

    return rows


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
