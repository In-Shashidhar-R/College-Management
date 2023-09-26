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
        
        user_option = input("Option: ")
        if user_option == "1":
            print("")
            print("Mark student register")
            command_handler.execute("SELECT username FROM user WHERE privilege = 'student'")
            records = command_handler.fetchall()
            date = input("Date: DD/MM/YYYY: ")
            for record in records:
                record = str(record).replace("'","")
                record = str(record).replace(",","")
                record = str(record).replace("(","")
                record = str(record).replace(")","")
                status = input("Status for " + str(record) + " (P/A/L): ")
                query_vals = (str(record), date, status)
                command_handler.execute("INSERT INTO attendance (username, date, status) VALUES(%s, %s, %s)", query_vals)
                db.commit()
                print(record + " Marked as " + status)
        elif user_option == "2":
            print("")
            print("Viewing all student registers")
            command_handler.execute("SELECT username, date, status FROM attendance")
            records = command_handler.fetchall()
            for record in records:
                print(record)
        elif user_option == "3":
            break
        else:
            print("Invalid Option")
            
def student_session(username):
    while True:
        print("\nStudent's Menu")
        print("1. View Register")
        print("2. Download the Register")
        print("3. Logout")
        
        user_option = input("Option: ")
        if user_option == "1":
            print(username + "Attendance Report")
            username = (str(username),)
            command_handler.execute("SELECT date, username, status FROM attendance WHERE username = %s", username)
            records = command_handler.fetchall()
            for record in records:
                print(record)
        elif user_option == "2":
            print("Downloadind the Register")
            username = (str(username),)
            command_handler.execute("SELECT date, username, status FROM attendance WHERE username = %s", username)
            records = command_handler.fetchall()
            for record in records:
                with open("C:/Users/mailt/OneDrive/Desktop/Study/Projects/Python Project/Attendance Reports/register.txt", "w") as f:
                    f.write(str(records)+"\n")
                f.close()
            print("All records Saved")
            
        elif user_option == "3":
            break
        else:
            print("Invalid Option")

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
            print("\nDelete Existing Student Account")
            username = input("Student username: ")
            query_vals = (username, "student")
            command_handler.execute("DELETE FROM user WHERE username = %s AND privilege = %s", query_vals)
            db.commit()
            if command_handler.rowcount < 1:
                print("User not Found")  
            else:
                print(username + " Deleted ")
                
        elif user_option == "4":
            print("\nDelete Existing Teacher Account")
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
    print("\nTeacher's Login")
    username = input("Username: ")
    password = input("Password: ")
    query_vals = (username, password)
    command_handler.execute("SELECT * FROM user WHERE username = %s AND password = %s AND privilege = 'teacher'", query_vals)
    if command_handler.rowcount <= 0:
        print("Login not Recognized")
    else:
        teacher_session()
        
def auth_student():
    print("\nStudent's Login")
    username = input("Username : ")
    password = input("Password: ")
    query_vals = (username, password, "student")
    command_handler.execute("SELECT username FROM user WHERE username = %s AND password = %s AND privilege = %s", query_vals)
    result = command_handler.fetchone()
    if result is None:
        print("Invalid login details")
    else:
        student_session(result[0])

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
