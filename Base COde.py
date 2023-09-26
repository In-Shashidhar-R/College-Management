import mysql.connector as mysql

db = mysql.connect(host="localhost",user="root",password="",database="college")
command_handler = db.cursor(buffered=True)

def admin_session():
    while 1:
        print("")
        print("Admin Menu")
        print("1.Register new Student")
        print("2.Register new Teacher")
        print("3.Delete Existing Student")
        print("4.Delete Existing Teacher")
        print("5.Logout")
        
        user_option = input(str("option : "))
        if user_option =="1":
            print("")
            print("Register New Student")
            username = input(str("Student username: "))
            password = input(str("Student Password : "))
            query_vals = (username,password)
            command_handler.execute("Insert Into user (username,password,privileage) VALUES (%s,%s,'student')",query_vals)
            db.commit()
            print(username + "has been registered as a student")
def auth_admin():
    print("")
    print("Admin Login")
    print("")
    username = input(str("Username : "))
    password = input(str("Password: "))
    if username == "admin":
        if password == "password":
            admin_session()
        else:
            print("Incorrect password !")
    else:
        print("Login Does ot exist")


def main():
    while 1:
        print("Welcome To the Amrita Managaement System")
        print("")
        print("1.Login as teacher")
        print("2.Login as Student")
        print("3.Login as admin ")
        
        user_option = input(str("Option : "))
        if user_option == "1":
            print("Teacher login")
        elif user_option == "2":
            print("Student login")
        elif user_option == "3":
            auth_admin()
        else:
            print("No Valid option")
            
main()