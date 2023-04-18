import sqlite3
 
import sqlite3

def register_user(username,password,email):
    print(username)
    print(password)
    print(email)
    try:
        connect = sqlite3.connect("/Users/mananshah/Downloads/Face Recognition/views/database/facerec.db")
        cursor = connect.cursor()
        cursor.execute("INSERT INTO users(Name,User,Password,Email) VALUES(?,?,?,?)", (username,username,password,email))
        #get_password = cursor.fetchone()
        # if password == get_password[0]:
        #     msg = "success"
        #     connect.close()
        #     return msg
        # else:
        #     msg = "failed"
        #     connect.close()
        #     return msg
        connect.commit()
        msg="success"
        connect.close()
        return msg
    except Exception as Error:
        print(Error)
        msg = "failed"
        return msg
 
 