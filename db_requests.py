
def stmt_sql_get_user():
    """Search for user by username provided"""

    stmt = "SELECT * FROM users WHERE usr_login=:usr_login"

    return stmt


def stmt_sql_get_customers():
    """Search for user by username provided"""

    stmt = """
    SELECT
        customers.ctmr_id AS id,
        customers.ctmr_first_name AS fname,
        customers.ctmr_last_name AS lname,
        customers.ctmr_email AS email
    FROM customers
    """

    return stmt