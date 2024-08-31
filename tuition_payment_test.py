#!/usr/bin/env python3

import tuition_payment
import unittest
from unittest.mock import patch, mock_open
from io import StringIO
import sys

class Test_check_name(unittest.TestCase):

    def test_existing(self):    # To test scenario when the input is existing to system
        test_case = "James Robert Thompson"
        result = tuition_payment.check_name(test_case)
        self.assertTrue(result)

    def test_not_existing(self):    # To test scenario when the input is not existing to system
        test_case = "jamAs robRrt thompson"
        result = tuition_payment.check_name(test_case)
        self.assertFalse(result)

    def test_jumble_letter_case(self):          # To test scenario when the input contain lower and upper case
        test_case = "jAmEs RoBErt thoMPsoN"     # To test if code ignore lower or upper case input
        result = tuition_payment.check_name(test_case)
        self.assertTrue(result)

    def test_integer_input(self):       # To test scenario when the input is integer
        test_case = "123 456 789"
        result = tuition_payment.check_name(test_case)
        self.assertFalse(result)

    def test_no_character_input(self):       # To test scenario when there is no any character input
        test_case = "\n\n"
        result = tuition_payment.check_name(test_case)
        self.assertFalse(result)

    @patch("builtins.open", new_callable=mock_open)
    def test_file_not_found(self, mock_open):
        mock_open.side_effect = FileNotFoundError()
        result = tuition_payment.check_name("John michael smith")   # Call the function
        self.assertEqual(result, "error")                              # Check the output
        mock_open.assert_called_once_with(tuition_payment.list_enrollee)    # Ensure the function tried to open the file

# Run Test_check_name tests
check_name_test_output = unittest.TextTestRunner().run(unittest.TestLoader().loadTestsFromTestCase(Test_check_name))
print(check_name_test_output)
print("\nTest_check_name()")
print("-" * 70)

class Test_check_status(unittest.TestCase):

    def test_match_status(self):        # To test scenario for match input status with a given input name
        result = tuition_payment.check_status("Olivia Grace Martinez", 1)
        self.assertTrue(result)

    def test_unmatch_status(self):      # To test scenario for umatch input status with a given input name
        result = tuition_payment.check_status("Olivia Grace Martinez", 2)
        self.assertFalse(result)

# Run Test_check_status tests
check_name_test_output = unittest.TextTestRunner().run(unittest.TestLoader().loadTestsFromTestCase(Test_check_status))
print(check_name_test_output)
print("\nTest_check_status()")
print("-" * 70)

class Test_payment(unittest.TestCase):

    def test_choice1(self):     # To test scenario if a user input is equal to 1 or for Full Scholarship Status
        captured_output = StringIO()
        sys.stdout = captured_output
        test_case = 1
        tuition_payment.payment(test_case)
        printed_text = captured_output.getvalue().strip()
        expected_output = "Balance to pay: ₱3,000.00"
        self.assertEqual(printed_text, expected_output)

        sys.stdout = sys.__stdout__

    def test_choice2(self):     # To test scenario if a user input is equal to 2 or for Half Scholarship Status
        captured_output = StringIO()
        sys.stdout = captured_output
        test_case = 2
        tuition_payment.payment(test_case)
        printed_text = captured_output.getvalue().strip()
        expected_output = "Balance to pay: ₱15,500.00"
        self.assertEqual(printed_text, expected_output)

        sys.stdout = sys.__stdout__

    def test_choice3(self):     # To test scenario if a user input is equal to 3 or for No Scholarship Status
        captured_output = StringIO()
        sys.stdout = captured_output
        test_case = 3
        tuition_payment.payment(test_case)
        printed_text = captured_output.getvalue().strip()
        expected_output = "Balance to pay: ₱28,000.00"
        self.assertEqual(printed_text, expected_output)

        sys.stdout = sys.__stdout__

# Run Test_paymaent tests
check_name_test_output = unittest.TextTestRunner().run(unittest.TestLoader().loadTestsFromTestCase(Test_payment))
print(check_name_test_output)
print("\nTest_payment()")
print("-" * 70)

class Test_generate_enrolled_students(unittest.TestCase):

    def setUp(self):
        # This method will run before each test
        self.mock_open_patcher = patch("builtins.open", new_callable=mock_open)
        self.mock_open = self.mock_open_patcher.start()

        # Setup any other state or resources needed for the tests
        self.mock_file = self.mock_open()

    def tearDown(self):
        # This method will run after each test
        self.mock_open_patcher.stop()

        # Clean up any other state or resources that need to be reset

    def test_approved(self):
        result = tuition_payment.generate_enrolled_students("John Michael Smith", "Y")
        self.assertTrue(result)

    def test_not_approved(self):
        result = tuition_payment.generate_enrolled_students("John Michael Smith", "N")
        self.assertFalse(result)

    @patch("builtins.open", new_callable=mock_open)
    def test_file_not_found(self, mock_open):
        mock_open.side_effect = FileNotFoundError()
        result = tuition_payment.generate_enrolled_students("John michael smith", "Y")   # Call the function
        self.assertEqual(result, "error")                                                # Check the output
        mock_open.assert_called_once_with(tuition_payment.list_enrolled_students, "a")   # Ensure the function tried to open the file

# Run Test_generate_enrolled_students tests
check_name_test_output = unittest.TextTestRunner().run(unittest.TestLoader().loadTestsFromTestCase(Test_generate_enrolled_students))
print(check_name_test_output)
print("\nTest_generate_enrolled_students()")
print("-" * 70)
