# Tuition_payment

TUITION PAYMENT
This script automates a simple tuition payment process. It is designed for use by administrators or personnel responsible for managing 
tuition payments.

Objectives
The script performs the following functions:

1. Student Enrollment Verification: Allows an admin to input the details of students (last name, first name, middle name) who wish to enroll. 
It first checks if these details match any records in the system.
2. Status Verification: If the student's details match, the program continues to check the selected scholarship status (full, half, or no scholarship). 
The script verifies if the student's name and selected status align with the data stored in List_enrollees.csv.
3. Error Handling: If there is a mismatch between the student's status and the system data, the script will notify the user and offer the 
option to return to the status selection.
4. Payment Calculation: If the details and status match, the script calculates the total amount to pay based on the scholarship status and 
displays it on the screen.
5. Approval Process: The admin has the option to approve or disapprove the transaction. If approved, the system updates the record of enrolled 
students and appends the new student details to an enrollment file. If disapproved, the process is aborted, and the user is given the option 
to start another transaction.

Users guide for running a program:

	filename = "tuition_payment.py"		# This is a main functional code for tuition payment

	FOR LINUX

	1. Run a program in CLI using "./<filename>" command.   """ Ensure that the python code file run inside of
								    Tuition_payment directory """
	
	2. The program run and just follow along the instruction on the screen.

	FOR WINDOWS

	1. Run a program in CLI using "python tuition_payment.py" command.	"""Ensure that the python code file run inside of
										   Tuition_payment directory"""
	
	2. The program run and just follow along the instruction on the screen.


""" Also check my test scripts for this functional code. I have two test scripts (tuition_payment_test.py, 
	tuition_payment_main_test.py) """

TESTING SCRIPTS
	
	The script includes unit tests and integration tests using the unittest framework. 
        The unit tests focus on individual functions, while integration tests verify the overall functionality of the script.
