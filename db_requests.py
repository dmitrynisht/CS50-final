
def stmt_sql_get_user():
    """Search for user by username provided"""

    stmt = "SELECT * FROM users WHERE usr_login=:usr_login"

    return stmt


def stmt_sql_get_customers():
    """Retrieve all customers"""

    stmt = """
    SELECT
        customers.ctmr_id AS id,
        customers.ctmr_uid AS uid,
        customers.ctmr_first_name AS fname,
        customers.ctmr_last_name AS lname,
        customers.ctmr_email AS email
    FROM customers
    WHERE ((:dont_filter_by_uid)
            OR (customers.ctmr_uid=:uid))
        AND ((:dont_filter_by_fname)
            OR (customers.ctmr_first_name=:fname))
        AND ((:dont_filter_by_lname)
            OR (customers.ctmr_last_name=:lname))
        AND ((:dont_filter_by_email)
            OR (customers.ctmr_email=:email))
    """

    return stmt


def stmt_sql_ins_customer():
    """Insert new customer"""

    stmt = """
    INSERT INTO customers (ctmr_uid, ctmr_first_name, ctmr_last_name, ctmr_email)
    VALUES (:uid, :fname, :lname, :email)
    """

    return stmt


def stmt_sql_upd_customer():
    """Update customer info"""

    stmt = """
    UPDATE customers
    SET ctmr_uid=:uid, ctmr_first_name=:fname, ctmr_last_name=:lname, ctmr_email=:email
    WHERE ctmr_id=:ctmr_id
    """

    return stmt

def stmt_sql_get_customer_orders():
    """Retrieve orders for customer_id provided"""

    stmt = """
    SELECT
        orders.svc_ord_id AS ord_id,
        orders.svc_ord_number AS ord_number,
        orders.svc_ord_date AS ord_date,
        orders.svcos_name AS ord_status,
        orders.ctmr_id AS ctmr_id
    FROM service_orders AS orders
    WHERE (orders.ctmr_id=:ctmr_id))
    """
    # WHERE ((:dont_filter_by_ctmr_id)
    #         OR (orders.ctmr_id=:ctmr_id))

    return stmt