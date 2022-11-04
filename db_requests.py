
def get_user():
    """Search for user by username provided"""

    # # Named argument doesnt work. It seems like limitation of CS50
    stmt = "SELECT * FROM users WHERE usr_login=:usr_login"
    # rows = db.execute(stmt, {"username": username})
    # stmt = """
    # SELECT
    #     *
    # FROM users
    # WHERE
    #     usr_login = ?
    # """

    return stmt