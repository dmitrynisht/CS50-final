
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
