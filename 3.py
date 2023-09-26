import mysql.connector as mysql

db = mysql.connect(host="localhost", user="root", password="", database="college")
command_handler = db.cursor(buffered=True)

command_handler.execute(
    """CREATE TABLE IF NOT EXISTS user (
        id INT AUTO_INCREMENT PRIMARY KEY,
        username VARCHAR(255) NOT NULL,
        password VARCHAR(255) NOT NULL,
        privilege ENUM('admin', 'teacher', 'student') NOT NULL
    )"""
)
db.commit()

def teacher_session():
     while True:
        print("\nTeacher's Menu")
        print("1. Mark Student Register")
        print("2. View Register")
        print("3. Logout")
        
        user_option = input(str("Option : "))
        if user_option == "1":
            print("")
            print("Mark student register")
            command_handler.execute("SELECT username FROM user WHERE privilege = 'student'")
            records = command_handler.fetchall()
            date = input(str("Date : DD/MM/YYYY : "))
            for record in records:
                record = str(record).replace("'","")
                record = str(record).replace(",","")
                record = str(record).replace("(","")
                record = str(record).replace(")","")
                #Present | Absent | Late 
                status = input(str("Status for " + str(record)+ " P/A/L : "))
                qurey_vals = (str(record),date,status)
                command_handler.execute("INSERT INTO attendance (username,date,status) VALUES(%s,%s,%s)",qurey_vals)
                db.commit()
                print(record + " Marked as " + status)
        elif user_option == "2":
            print("")
            print("Viewing all student registers")
            command_handler.execute("SELECT username,date,status FROM attendance")
            records = command_handler.fetchall()
            for record in records:
                print(record)
        elif user_option == "3":
            break
        else:
            print("Invalid Option")
            
def student_session(username):
    while 1:
        print("")
        print("1. View Register")
        print("2. Download the Register")
        print("3. Logout")
        
        user_option = input(str("Option: "))
        if user_option =="1":
            username = (str(username),)
            command_handler.execute("SELECT date, username, status FROM attendance WHERE username = %s",username)
            records = command_handler.fecthall()
            for record in records:
                print(record)
        
            
            
def admin_session():
    while True:
        print("\nAdmin Menu")
        print("1. Register new Student")
        print("2. Register new Teacher")
        print("3. Delete Existing Student")
        print("4. Delete Existing Teacher")
        print("5. Logout")
        
        user_option = input("Option: ")
        
        if user_option == "1":
            print("\nRegister New Student")
            username = input("Student username: ")
            password = input("Student Password: ")
            query_vals = (username, password)
            command_handler.execute(
                "INSERT INTO user (username, password, privilege) VALUES (%s, %s, 'student')",
                query_vals
            )
            db.commit()
            print(username + " has been registered as a student")
            
        elif user_option == "2":
            print("\nRegister New Teacher\n")
            username = input("Teacher username: ")
            password = input("Teacher Password: ")
            query_vals = (username, password)
            command_handler.execute(
                "INSERT INTO user (username, password, privilege) VALUES (%s, %s, 'teacher')",
                query_vals
            )
            db.commit()
            print(username + " has been registered as a teacher")
            
        elif user_option == "3":
            print("\n Delete Existing Student Account")
            username = input("Student username: ")
            query_vals = (username, "student")
            command_handler.execute("DELETE FROM user WHERE username = %s AND privilege = %s", query_vals)
            db.commit()
            if command_handler.rowcount < 1:
                print("User not Found")  
            else:
                print(username + " Deleted ")
                
        elif user_option == "4":
            print("\n Delete Existing Teacher Account")
            username = input("Teacher username: ")
            query_vals = (username, "teacher")
            command_handler.execute("DELETE FROM user WHERE username = %s AND privilege = %s", query_vals)
            db.commit()
            if command_handler.rowcount < 1:
                print("User not Found")
            else:
                print(username + " Deleted ")
        elif user_option == "5":
            break
        else:
            print("Invalid option")

def auth_teacher():
    print("")
    print("Teacher's Login")
    print("")
    username = input("Username : ")
    password = input("Password : ")
    query_vals = (username, password)
    command_handler.execute("SELECT * FROM user WHERE username = %s AND password = %s AND privilege = 'teacher'", query_vals)
    if command_handler.rowcount <= 0:
        print("Login not Recognized")
    else:
        teacher_session()
        
def auth_student():
    print("")
    print("Student's Login")
    print("")
    username = input(str("Username : "))
    password = input(str("Password: "))
    qurey_vals = (username,password)
    command_handler.execute("SELECT username FROM users WHERE username = %s AND password=%s AND privileage = %s",qurey_vals)
    username = command_handler.fecthone()
    if command_handler.rowcount<=0:
        print("Invalid login details")
    else:
        student_session(username)
    

def auth_admin():
    print("\nAdmin Login")
    username = input("Username: ")
    password = input("Password: ")
    if username == "admin" and password == "password":
        admin_session()
    else:
        print("Incorrect username or password!")

def main():
    while True:
        print("\nWelcome To the Amrita Management System")
        print("1. Login as teacher")
        print("2. Login as Student")
        print("3. Login as admin")
        print("4. Quit")
        
        user_option = input("Option: ")
        if user_option == "1":
            auth_teacher()
        elif user_option == "2":
            auth_student()
        elif user_option == "3":
            auth_admin()
        elif user_option == "4":
            print("Goodbye!")
            break
        else:
            print("Invalid option")

if __name__ == "__main__":
    main()

db.close()
