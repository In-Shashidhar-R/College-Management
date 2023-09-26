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
            print("\n Delete Existing Student Acount")
            username = input(str("Student username : "))
            query_vals = (username,"student")
            command_handler.execute("Delete FROM users where username = %s AND privileage = %s",query_vals)
            db.commit()
            if command_handler.rowcount<1:
                print("User not Found")
            else:
                print(username + " Deleted ")
                
            
        elif user_option == "4":
         
            pass
        elif user_option == "5":
            break
        else:
            print("Invalid option")

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
            print("Teacher login")
        elif user_option == "2":
            print("Student login")
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
