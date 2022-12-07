
def stmt_sql_get_user():
    """Search for user by username provided"""

    stmt = "SELECT * FROM users WHERE usr_login=:usr_login"

    return stmt


def stmt_sql_get_customers():
    """Retrieve all customers"""

    stmt = """
    SELECT
        customers.ctmr_id AS ctmr_id,
        customers.ctmr_uid AS ctmr_uid,
        customers.ctmr_first_name AS ctmr_fname,
        customers.ctmr_last_name AS ctmr_lname,
        customers.ctmr_email AS ctmr_email
    FROM customers
    WHERE ((:dont_filter_by_uid)
            OR (customers.ctmr_uid=:ctmr_uid))
        AND ((:dont_filter_by_fname)
            OR (customers.ctmr_first_name=:ctmr_fname))
        AND ((:dont_filter_by_lname)
            OR (customers.ctmr_last_name=:ctmr_lname))
        AND ((:dont_filter_by_email)
            OR (customers.ctmr_email=:ctmr_email))
        AND ((:dont_filter_by_id)
            OR (customers.ctmr_id=:ctmr_id))
    """

    return stmt


def stmt_sql_get_customer_info():
    """Retrieve detailed customer's info"""

    stmt = """
    SELECT
        customers.ctmr_id AS ctmr_id,
        customers.ctmr_uid AS ctmr_uid,
        customers.ctmr_first_name AS ctmr_fname,
        customers.ctmr_last_name AS ctmr_lname,
        customers.ctmr_email AS ctmr_email,
        customers.sktype_name AS sktype_name,
        customers.ctmr_contraindications AS ctmr_contraindications,
        customers.ctmr_additional_info AS ctmr_additional_info,
        customers.ctmr_subscribed AS ctmr_subscribed
    FROM customers
    WHERE ((:dont_filter_by_uid)
            OR (customers.ctmr_uid=:ctmr_uid))
        AND ((:dont_filter_by_fname)
            OR (customers.ctmr_first_name=:ctmr_fname))
        AND ((:dont_filter_by_lname)
            OR (customers.ctmr_last_name=:ctmr_lname))
        AND ((:dont_filter_by_email)
            OR (customers.ctmr_email=:ctmr_email))
        AND ((:dont_filter_by_id)
            OR (customers.ctmr_id=:ctmr_id))
    """

    return stmt


def stmt_sql_ins_customer():
    """Insert new customer"""

    stmt = """
    INSERT INTO customers (ctmr_uid, ctmr_first_name, ctmr_last_name, ctmr_email)
    VALUES (:ctmr_uid, :ctmr_fname, :ctmr_lname, :ctmr_email)
    """

    return stmt


def stmt_sql_upd_customer():
    """Update customer info"""

    stmt = """
    UPDATE customers
    SET ctmr_uid=:ctmr_uid, ctmr_first_name=:ctmr_fname, ctmr_last_name=:ctmr_lname, ctmr_email=:ctmr_email, sktype_name=:sktype_name, ctmr_contraindications=:ctmr_contraindications, ctmr_additional_info=:ctmr_additional_info, ctmr_subscribed=:ctmr_subscribed
    WHERE ctmr_id=:ctmr_id
    """

    return stmt

def stmt_sql_get_customer_orders():
    """Retrieve orders for customer_id provided"""

    stmt = """
    SELECT
        orders.svc_ord_id AS ord_id,
        orders.svc_ord_number AS ord_number,
        datetime(orders.svc_ord_date) AS ord_date,
        orders.svcos_name AS ord_status,
        orders.ctmr_id AS ctmr_id
    FROM service_orders AS orders
    WHERE (orders.ctmr_id=:ctmr_id)
    """
    # WHERE ((:dont_filter_by_ctmr_id)
    #         OR (orders.ctmr_id=:ctmr_id))

    return stmt