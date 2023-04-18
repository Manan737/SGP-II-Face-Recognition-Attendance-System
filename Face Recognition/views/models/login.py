import sqlite3
 
def login_user(username, password):
    print(username)
    print(password)
    try:
        connect = sqlite3.connect("/Users/mananshah/Downloads/Face Recognition/views/database/facerec.db")
        cursor = connect.cursor()
        cursor.execute(
            "SELECT Password FROM users WHERE User =?", (username,))
        get_password = cursor.fetchone()
        if password == get_password[0]:
            msg = "success"
            connect.close()
            return msg
        else:
            msg = "failed"
            connect.close()
            return msg
 
    except Exception as Error:
        print(Error)
        msg = "failed"
        return msg
 
 
def login_session():
    try:
        connect = sqlite3.connect("/Users/mananshah/Downloads/Face Recognition/views/database/facerec.db")
        cursor = connect.cursor()
        cursor.execute("SELECT User FROM user_session WHERE id =?", (1,))
        get_user_online = cursor.fetchone()
        user_online = []
        for name in get_user_online:
            user_online.append(name)
        connect.close()
        return user_online[0]
    except Exception as error:
        user_online = "error"
        print(error)
        return user_online