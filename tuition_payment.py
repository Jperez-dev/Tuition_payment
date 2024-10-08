#!/usr/bin/env python3

import csv
import os
import pandas as pd

list_enrollee = os.path.abspath('List_enrollees.csv')
list_enrolled_students = "Enrolled_students.txt"

def check_name(fullname):   # To check if the input name is in our system
    
    try:
        with open(list_enrollee) as file:
            reader = csv.DictReader(file)
            for row in reader:
                if fullname.lower() in row["Name"].lower():
                    return True
                    
            return False
        
    except FileNotFoundError:
        return "error"

def check_status(fullname, choice):     # To check if the selected status complement the given name
    if choice == 1:
        status = "Full Scholarship"
    if choice == 2:
        status = "Half Scholarship"
    if choice == 3:
        status = "No Scholarship"

    with open(list_enrollee) as file:
        reader = csv.DictReader(file)
        for row in reader:
            if fullname.lower() == row["Name"].lower() and status.lower() == row["status"].lower():
                return True
        return False

def payment(choice):   # To compute the exact amount to pay depends to the status of given name

    tuition_fee = 25000
    miscellaneous_fee = 3000
    if choice == 1:
        print(f"Balance to pay: ₱{miscellaneous_fee:,.2f}")
    if choice == 2:
        balance = (tuition_fee * 0.5) + miscellaneous_fee
        print(f"Balance to pay: ₱{balance:,.2f}")
    if choice == 3:
        balance = tuition_fee + miscellaneous_fee
        print(f"Balance to pay: ₱{balance:,.2f}")

def generate_enrolled_students(alphabetical_name):  # To generate file to all students who already enrolled and approved
                                                                     # by assigned personnel 
    student_data = {
        "NAME": [alphabetical_name.title()],
        "STATUS": ["ENROLLED"]
    }
    initial_df = pd.DataFrame(student_data)
        
    if not os.path.exists(list_enrolled_students):
        with open(list_enrolled_students, "a") as file:
            df_string = initial_df.to_string(index=False, col_space=40, justify='left')
            file.write(df_string)
            file.write('\n')
            return True

    df_string = initial_df.to_string(index=False, header=False, col_space=40, justify='left')
    with open(list_enrolled_students, "r") as file:
        existing_lines = file.readlines()

    if any(df_string in line for line in existing_lines):
        return False

    with open(list_enrolled_students, "a") as file:   
        file.write(df_string)
        file.write('\n')
        return True

def main():     # Start of the main program
    print("*************** Hello Welcome To Tuition Payment Process ***************")
    print("-" * 72)

    while True:
        print("Before proceeding to payment, please provide your information.")
        lastname = input("Enter your Last Name: ")
        firstname = input("Enter your First Name: ")
        middlename = input("Enter your Middle Name: ")

        fullname = f"{firstname} {middlename} {lastname}"
        alphabetical_name = f"{lastname}, {firstname} {middlename}"

        print("Checking your information.....")

        if check_name(fullname) == "error":         # To avoid file path conflicts. The program discontinue if there is any error
            print(f"An error occurred while reading the file")
            print("It is possible that you are not on the right directory when running this code...")
            return             
                             
        if not check_name(fullname):
            print("The system doesn't recognize this name !!")
            print("-" * 72)
            use_again = input("Want to make another transaction? (Y/N): ").upper()
            print("-" * 72)

            if use_again != 'Y':
                break
            
            continue

        print("Your information is verified. You can proceed to payment.")
        print("-" * 72)

        while True:
            print("Choose Scholarship Status")
            print("1. Full Scholarship")
            print("2. Half Scholarship")
            print("3. No Scholarship")
            choice = input("Enter your scholarship status (1-3): ")
            try:
                choice = int(choice)
                if not 1 <= choice <= 3:
                    print("Invalid choice. Please enter a number between (1-3).")
                    use_again = input("Want to go back on status selection? (Y/N): ").upper()

                    if use_again != 'Y':
                        break
                    continue
                
                if not check_status(fullname, choice):
                    print(f"{fullname.upper()} isn't compatible on your selected status.")
                    use_again = input("Want to go back on status selection? (Y/N): ").upper()

                    if use_again != 'Y':
                        break
                    continue

                payment(choice)
                print("-" * 72)
                print("If this person completed the payment process, kindly proceed to approval process.")
                print("-" * 72)
                approver_choice = input("Want to approve this person? (Y/N): ").upper()

                if approver_choice == "Y":
                    
                    if generate_enrolled_students(alphabetical_name):
                        print(f"{alphabetical_name.title()} has been successfully enrolled.")
                        print("Transaction finished.")
                        break

                    print(f"{alphabetical_name.title()} is already enrolled.")
                    break


                print("Not approved by assigned personnel !!")
                break

            except ValueError:
                    print("Invalid input. Please enter a valid number.")
                    use_again = input("Want to go back on status selection? (Y/N): ").upper()
                    if use_again != 'Y':
                        break

        use_again = input("Want to make another transaction? (Y/N): ").upper()
        print("-" * 72)

        if use_again != 'Y':
            break


    print("****************************** THANK YOU *******************************")
    print("-" * 72)

        


if __name__ == "__main__":
    main()