def connect_db(db_type='sqlite'):
    """
    连接数据库
    :param db_type: 数据库类型
    :return:
    """
    
    if db_type == 'sqlite':
        print("sqlite")
        import sqlite3
        con = sqlite3.connect('./instance/course.sqlite')
        cur = con.cursor()
    else:
        print("不支持的数据库类型")
        return
    
    return con, cur
