import mysql.connector
from datetime import datetime

''' 
Before running this program, create a MySQL database named 'school_management_system' and define the necessary tables with the columns:
students (student_id, first_name, last_name, date_of_birth, gender, class)
teachers (teacher_id, first_name, last_name, date_of_birth, gender, subject_taught)
'''


def connect_to_database():
    return mysql.connector.connect(host="localhost",user="root",password="mysql",database="school_management_system")

def get_string(statement):
    while True:
        value = input(statement)
        try:
            if value.isalpha():
                if len(value) >= 3 and len(value) <= 30:
                    break
                else:
                    print("Invalid. Value should be between 3 - 30 characters!")
                    raise ValueError
            else:
                print("Invalid. Name can contain only alphabets!")
                raise ValueError
        except ValueError:
            continue
    print("Entered Value :", value)
    return value

def get_gender(statement):
    while True:
        value = input(statement)
        try:
            if value in (['Male','Female','Other']):
                break
            else:
                raise ValueError
        except ValueError:
            print("Invalid. Gender should only be Male, Female or Other. ")
            continue
    print(f" Entered Value : {value}")
    return value

def get_date(statement):
    while True:
        value = input(statement)
        try:
            if value != datetime.strptime(value, "%Y-%m-%d").strftime('%Y-%m-%d'):
                raise ValueError
            break
        except ValueError:
            print("Invalid. Incorrect data format, should be YYYY-MM-DD")
            continue
    print("Entered Value :", value)
    return value

def get_class(statement):
    while True:
        value = input(statement)
        try:
            if value in (['I','II','III','IV','V','VI','VII','VIII','IX','X','XI','XII']):
                break
            else:
                raise ValueError
        except ValueError:
            print("Invalid. Class should be I-XII in Roman Numerals. ")
            continue
    print("Entered Value :", value)
    return value

def get_subject(statement):
    while True:
        value = input(statement)
        try:
            if value in (['English','Physics','Chemistry','Mathematics','Physical Education','Computer Science',
                          'Biology','Economics','Accounts','Business Studies','Information Practices','Psychology'
                          'History','Geography','Political Science','Fine Arts']):
                break
            else:
                raise ValueError
        except ValueError:
            print("Invalid. Enter Valid Subject. ")
            continue
    print("Entered Value :", value)
    return value


# Function to add a new student
def add_student():
    connection = connect_to_database()
    cursor = connection.cursor()
    first_name = get_string("Enter first name of the student: ")
    last_name = get_string("Enter last name of the student: ")    
    date_of_birth = get_date("Enter the date of birth (YYYY-MM-DD): ")
    gender = get_gender("Enter the gender of the student (Male/Female/Other): ") 
    class_name = get_class("Enter the class of the student: ")
    query = "INSERT INTO students (first_name, last_name, date_of_birth, gender, class)VALUES (%s, %s, %s, %s, %s)"
    values = (first_name, last_name, date_of_birth, gender, class_name)
    cursor.execute(query, values)
    connection.commit()

    # Displaying Student ID
    student_id = cursor.lastrowid
    print("Student added successfully! Student ID is", student_id)
    cursor.close()
    connection.close()

# Function to add a new teacher
def add_teacher():
    connection = connect_to_database()
    cursor = connection.cursor()
    first_name = get_string("Enter the first name of the teacher: ")
    last_name = get_string("Enter the last name of the teacher: ")
    date_of_birth = get_date("Enter the date of birth (YYYY-MM-DD): ")
    gender = get_gender("Enter the gender of the teacher (Male/Female/Other): ")
    subject_taught = get_subject("Enter the subject taught by the teacher: ")
    query = "INSERT INTO teachers (first_name, last_name, date_of_birth, gender, subject_taught)VALUES (%s, %s, %s, %s, %s)"
    values = (first_name, last_name, date_of_birth, gender, subject_taught)
    cursor.execute(query, values)
    connection.commit()

    #Displaying the Teacher ID
    teacher_id = cursor.lastrowid
    print("Teacher added successfully! Teacher ID is", teacher_id)
    cursor.close()
    connection.close()

# Function to update student information
def update_student():
    connection = connect_to_database()
    cursor = connection.cursor()
    student_id = input("Enter the student ID to update: ")

    print("\nUpdate Student Information Menu:")
    print("1. Update First Name")
    print("2. Update Last Name")
    print("3. Update Date of Birth")
    print("4. Update Gender")
    print("5. Update Class")
    print("6. Back to Main Menu")

    choice = input("Enter your choice (1-6): ")

    if choice == "1":
        new_first_name = input("Enter the new first name: ")
        query = "UPDATE students SET first_name = %s WHERE student_id = %s"
        values = (new_first_name, student_id)
    elif choice == "2":
        new_last_name = input("Enter the new last name: ")
        query = "UPDATE students SET last_name = %s WHERE student_id = %s"
        values = (new_last_name, student_id)
    elif choice == "3":
        new_date_of_birth = input("Enter the new date of birth (YYYY-MM-DD): ")
        query = "UPDATE students SET date_of_birth = %s WHERE student_id = %s"
        values = (new_date_of_birth, student_id)
    elif choice == "4":
        new_gender = input("Enter the new gender (Male/Female/Other): ")
        query = "UPDATE students SET gender = %s WHERE student_id = %s"
        values = (new_gender, student_id)
    elif choice == "5":
        new_class_name = input("Enter the new class: ")
        query = "UPDATE students SET class = %s WHERE student_id = %s"
        values = (new_class_name, student_id)
    elif choice == "6":
        return  # Go back to the main menu
    else:
        print("Invalid choice. Please enter a number between 1 and 6.")
        return

    cursor.execute(query, values)
    connection.commit()

    print("Student information updated successfully!")

    cursor.close()
    connection.close()

#Function to display existing records
def display_student_records():
    connection = connect_to_database()
    cursor = connection.cursor()

    student_id = input("Enter the student ID to display records: ")

    query_student = "SELECT * FROM students WHERE student_id = %s"
    values_student = (student_id,)
    cursor.execute(query_student, values_student)
    student_info = cursor.fetchone()

    if not student_info:
        print("Student not found.")
        cursor.close()
        connection.close()
        return

    print("\nStudent Information:")
    print("Student ID:", student_info[0])
    print("First Name:", student_info[1])
    print("Last Name:", student_info[2])
    print("Date of Birth:", student_info[3])
    print("Gender:", student_info[4])
    print("Class:", student_info[5])

def delete_student():
    connection = connect_to_database()
    cursor = connection.cursor()
    student_id = input("Enter the student ID to delete: ")
    query_check_student = "SELECT * FROM students WHERE student_id = %s"
    values_check_student = (student_id,)
    cursor.execute(query_check_student, values_check_student)
    existing_student = cursor.fetchone()

    if not existing_student:
        print("Student not found.")
        cursor.close()
        connection.close()
        return

    query_delete_student = "DELETE FROM students WHERE student_id = %s"
    cursor.execute(query_delete_student, values_check_student)
    print("Record Deleted!")


# Main menu
while True:
    print("\nSchool Management System Main Menu:")
    print("1. Add Student")
    print("2. Add Teacher")
    print("3. Update Student Information")
    print("4. Display Student Records")
    print("5. Delete Student")
    print("6. Exit")

    choice = input("Enter your choice (1-6): ")
    if choice == "1":
        add_student()
    elif choice == "2":
        add_teacher()
    elif choice == "3":
        update_student()
    elif choice == "4":
        display_student_records()
    elif choice == "5":
        delete_student()
    elif choice == "6":
        print("Exiting the program. Thanks!")
        break
    else:
        print("Invalid choice. Please enter a number between 1 and 6.")
