
def stmt_sql_get_user():
    """Search for user by username provided"""

    stmt = "SELECT * FROM users WHERE usr_login=:usr_login"

    return stmt


def stmt_sql_get_skin_types():
    """Retrieve all skin types"""

    stmt = """
    SELECT
        sktypes.sktype_name AS name
    FROM skin_types AS sktypes
    ORDER BY
        sktypes.sktype_id
    """

    return stmt


def stmt_sql_get_genders():
    """Retrieve all genders"""

    stmt = """
    SELECT
        genders.gd_name AS name
    FROM genders
    ORDER BY
        genders.gd_id
    """

    return stmt


def stmt_sql_get_status_list():
    """Retrieve all status values"""

    stmt = """
    SELECT
        statusList.svcos_name AS name
    FROM service_order_status AS statusList
    ORDER BY
        statusList.svcos_id
    """

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
        customers.gd_name AS ctmr_gender,
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
    INSERT INTO customers (ctmr_uid, ctmr_first_name, ctmr_last_name, ctmr_email, sktype_name, gd_name, ctmr_contraindications, ctmr_additional_info, ctmr_subscribed)
    VALUES (:ctmr_uid, :ctmr_fname, :ctmr_lname, :ctmr_email, :sktype_name, :ctmr_gender, :ctmr_contraindications, :ctmr_additional_info, :ctmr_subscribed)
    """

    return stmt


def stmt_sql_upd_customer():
    """Update customer info"""

    stmt = """
    UPDATE customers
    SET ctmr_uid=:ctmr_uid, ctmr_first_name=:ctmr_fname, ctmr_last_name=:ctmr_lname, ctmr_email=:ctmr_email, sktype_name=:sktype_name, gd_name=:ctmr_gender, ctmr_contraindications=:ctmr_contraindications, ctmr_additional_info=:ctmr_additional_info, ctmr_subscribed=:ctmr_subscribed
    WHERE ctmr_id=:ctmr_id
    """

    return stmt

def stmt_sql_get_customer_orders():
    """Retrieve orders for customer_id provided"""

    stmt = """
    SELECT
        orders.svc_ord_id AS ord_id,
        orders.svc_ord_number AS ord_number,
        datetime(orders.svc_ord_appointment_date) AS ord_appointment_date,
        orders.svc_ord_skin_condition AS ord_skin_condition,
        orders.usr_login AS ord_beautician,
        orders.svcos_name AS ord_status
    FROM service_orders AS orders
    WHERE (orders.ctmr_id=:ctmr_id)
    """
    
    return stmt
    

def stmt_sql_get_customer_order_info():
    """Retrieve detailed customer's order info"""

    stmt = """
    SELECT
        sv_ord.svc_ord_id AS ord_id,
        sv_ord.svc_ord_number AS ord_number,
        datetime(sv_ord.svc_ord_date) AS ord_date,
        datetime(sv_ord.svc_ord_appointment_date) AS ord_appointment_date,
        sv_ord.svcos_name AS ord_status,
        sv_ord.usr_login AS ord_beautician,
        sv_ord.svc_ord_ctmr_complaints AS ord_ctmr_complaints,
        sv_ord.svc_ord_skin_condition AS ord_skin_condition,
        sv_ord.svc_ord_description AS ord_description
    FROM service_orders AS sv_ord
    WHERE (sv_ord.svc_ord_id=:ord_id)
    """

    return stmt


def stmt_sql_get_services():
    """Select services or commodities which are available.
    Item is available if it's 'unavailability' flag (prod_na) is off, i.e. prod_na=0.
    prod_na=0 means that item is available."""

    stmt = """
    SELECT
        product.prod_name AS prod_name,
        product.prod_duration AS prod_duration,
        product.prod_details AS prod_details,
        product.prod_how_to_use AS prod_how_to_use,
        product.prod_img_path AS prod_img_path,
        prices.price AS price,
        MAX(prices.prc_date) AS prc_date
    FROM products AS product
    INNER JOIN product_prices AS prices
        ON product.prod_name = prices.prod_name
    WHERE prod_na=0
        AND (product.ptype_name=:ptype)
    GROUP BY product.prod_name
    """

    return stmt
