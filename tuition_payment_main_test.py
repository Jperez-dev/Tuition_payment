#!/usr/bin/env python3

import unittest
import tuition_payment
from unittest.mock import patch, mock_open
from io import StringIO
import os
import tempfile

class Test_main(unittest.TestCase):

    def setUp(self):
        self.line = "-" * 72        # set this variable to avoid repeatition of variables
        # Create a temporary file
        self.test_file = tempfile.NamedTemporaryFile(delete=False)
        self.test_file_path = self.test_file.name
        self.test_file.close()

        # Set the list_enrolled_students to the temporary file path
        tuition_payment.list_enrolled_students = self.test_file_path

    def tearDown(self):
        # Remove the temporary file
        if os.path.exists(self.test_file_path):
            os.remove(self.test_file_path)


    # full transaction without any invalid inputs (one cycle process)
    @patch("builtins.input", side_effect=["Smith", "John", "Michael", 1, "Y", "N"])
    @patch("sys.stdout", new_callable=StringIO)
    def test_main_full_transaction(self, mock_stdout, mock_stdin):
        tuition_payment.main()
        output = mock_stdout.getvalue().strip()
        self.assertIn("Checking your information.....", output)
        self.assertIn("Your information is verified. You can proceed to payment.", output)
        self.assertIn("Balance to pay:", output)
        self.assertIn("If this person completed the payment process, kindly proceed to approval process.", output)
        self.assertIn("Smith, John Michael has been successfully enrolled.", output)
        self.assertIn("Transaction finished.", output)
        self.assertIn("THANK YOU", output)


    # full transaction without any invalid inputs (two cycle processess)
    @patch("builtins.input", side_effect=["Davis", "Sophia", "Marie", 2, "Y", "Y",
                                          "Martinez", "Olivia", "Grace", 1, "Y", "N"])
    @patch("sys.stdout", new_callable=StringIO)
    def test_main_morethan_onecycle_full_transaction(self, mock_stdout, mock_stdin):
        tuition_payment.main()
        output = mock_stdout.getvalue().strip()
        self.assertIn("Checking your information.....", output)
        self.assertIn("Your information is verified. You can proceed to payment.", output)
        self.assertIn("Balance to pay:", output)
        self.assertIn("If this person completed the payment process, kindly proceed to approval process.", output)
        self.assertIn("Davis, Sophia Marie has been successfully enrolled.", output)
        self.assertIn("Transaction finished.", output)
        self.assertIn("Checking your information.....", output)
        self.assertIn("Your information is verified. You can proceed to payment.", output)
        self.assertIn("Balance to pay:", output)
        self.assertIn("If this person completed the payment process, kindly proceed to approval process.", output)
        self.assertIn("Martinez, Olivia Grace has been successfully enrolled.", output)
        self.assertIn("Transaction finished.", output)
        self.assertIn("THANK YOU", output)

    # test if a name already on a list of enrolled students. Should notify that it is already enrolled.
    @patch("builtins.input", side_effect=["Davis", "Sophia", "Marie", 2, "Y", "Y",
                                          "Davis", "Sophia", "Marie", 2, "Y", "N"])
    @patch("sys.stdout", new_callable=StringIO)
    def test_main_name_on_enrolled_list(self, mock_stdout, mock_stdin):
        tuition_payment.main()
        output = mock_stdout.getvalue().strip()
        self.assertIn("Checking your information.....", output)
        self.assertIn("Your information is verified. You can proceed to payment.", output)
        self.assertIn("Balance to pay:", output)
        self.assertIn("If this person completed the payment process, kindly proceed to approval process.", output)
        self.assertIn("Davis, Sophia Marie has been successfully enrolled.", output)
        self.assertIn("Transaction finished.", output)
        self.assertIn("Checking your information.....", output)
        self.assertIn("Your information is verified. You can proceed to payment.", output)
        self.assertIn("Balance to pay:", output)
        self.assertIn("If this person completed the payment process, kindly proceed to approval process.", output)
        self.assertIn("Davis, Sophia Marie is already enrolled.", output)
        self.assertIn("THANK YOU", output)

    # not existing name on data
    @patch("builtins.input", side_effect=["Sophia", "Marie", "Davis", "N"])     # On this scenario, the inputs sequence is firstname
    @patch("sys.stdout", new_callable=StringIO)                                 # middlename and lastname but the correct is sequence
    def test_main_no_name(self, mock_stdout, mock_stdin):                       # lastname firstname and middlename so it makes the
        tuition_payment.main()                                                  # data is incorrect and doesn't match to anyone on system
        output = mock_stdout.getvalue().strip()
        self.assertIn("Checking your information.....", output)
        self.assertIn(self.line, output)
        self.assertIn("THANK YOU", output)
        self.assertIn(self.line, output)


    # unmatch status
    @patch("builtins.input", side_effect=["Davis", "Sophia", "Marie", 1, "N", "N"])     # The status selected doesn't match to the input
    @patch("sys.stdout", new_callable=StringIO)                                         # name. The system check if the status match to
    def test_main_unmatch_status(self, mock_stdout, mock_stdin):                        # the name of student.
        tuition_payment.main()
        output = mock_stdout.getvalue().strip()
        self.assertIn("Checking your information.....", output)
        self.assertIn("Your information is verified. You can proceed to payment.", output)
        self.assertIn("SOPHIA MARIE DAVIS isn't compatible on your selected status.", output)
        self.assertIn(self.line, output)
        self.assertIn("THANK YOU", output)


    # unmatch status edge case1
    @patch("builtins.input", side_effect=["Davis", "Sophia", "Marie", "", "N", "N"])    # This is a scenario when user didn't provide
    @patch("sys.stdout", new_callable=StringIO)                                         # any input in status selection
    def test_main_unmatch_status_edge_case1(self, mock_stdout, mock_stdin):
        tuition_payment.main()
        output = mock_stdout.getvalue().strip()
        self.assertIn("Checking your information.....", output)
        self.assertIn("Your information is verified. You can proceed to payment.", output)
        self.assertIn("Invalid input. Please enter a valid number.", output)
        self.assertIn(self.line, output)
        self.assertIn("THANK YOU", output)


    # unmatch status edge case2
    @patch("builtins.input", side_effect=["Davis", "Sophia", "Marie", 5, "N", "N"])     # The user input for status selection is out of
    @patch("sys.stdout", new_callable=StringIO)                                         # range
    def test_main_unmatch_status_edge_case2(self, mock_stdout, mock_stdin):
        tuition_payment.main()
        output = mock_stdout.getvalue().strip()
        self.assertIn("Checking your information.....", output)
        self.assertIn("Your information is verified. You can proceed to payment.", output)
        self.assertIn("Invalid choice. Please enter a number between (1-3).", output)
        self.assertIn(self.line, output)
        self.assertIn("THANK YOU", output)


    # unmatch status edge case3
    @patch("builtins.input", side_effect=["Davis", "Sophia", "Marie", "$$", "N", "N"])      # The user provides uncommon character as an
    @patch("sys.stdout", new_callable=StringIO)                                             # for status selection
    def test_main_unmatch_status_edge_case3(self, mock_stdout, mock_stdin):
        tuition_payment.main()
        output = mock_stdout.getvalue().strip()
        self.assertIn("Checking your information.....", output)
        self.assertIn("Your information is verified. You can proceed to payment.", output)
        self.assertIn("Invalid input. Please enter a valid number.", output)
        self.assertIn(self.line, output)
        self.assertIn("THANK YOU", output)


    # not approved process
    @patch("builtins.input", side_effect=["Davis", "Sophia", "Marie", 2, "N", "N"])     # When assigned personnel not approved a student
    @patch("sys.stdout", new_callable=StringIO)
    def test_main_not_approved(self, mock_stdout, mock_stdin):
        tuition_payment.main()
        output = mock_stdout.getvalue().strip()
        self.assertIn("Checking your information.....", output)
        self.assertIn("Your information is verified. You can proceed to payment.", output)
        self.assertIn("Balance to pay:", output)
        self.assertIn("If this person completed the payment process, kindly proceed to approval process.", output)
        self.assertIn("Not approved by assigned personnel !!", output)
        self.assertIn("THANK YOU", output)


    # user continously hit enter key. the inputs remain missing (" ")
    @patch("builtins.input", side_effect=["\n", "\n", "\n", "\n",])  # Not provide any input. Leave inputs missing.
    @patch("sys.stdout", new_callable=StringIO) 
    def test_main_continous_no_inputs(self, mock_stdout, mock_stdin):
        tuition_payment.main()
        output = mock_stdout.getvalue().strip()
        self.assertIn("Checking your information.....", output)
        self.assertIn("THANK YOU", output)


    """ Complex scenario. Multiple process with different inputs(some valid, some invalid). Also scenario if name is already
    on the list of enrolled students. Multiple cycle test. """
    @patch("builtins.input", side_effect=["Davis", "Sophia", "Marie", 1, "y", 2, "y", "y",
                                          "Martinez", "Olivia", "Grace", 1, "n", "y", 
                                          "thompson", "james", "robert", 2, "y", "y", 
                                          "johnson", "Emily","annE", 3, "y", "y",
                                          "thompson", "james", "robert", 2, "y", "n"])
    @patch("sys.stdout", new_callable=StringIO)
    def test_main_complex_scenario_with_multiple_cycles(self, mock_stdout, mock_stdin):
        tuition_payment.main()
        output = mock_stdout.getvalue().strip()
        self.assertIn("Checking your information.....", output)
        self.assertIn("Your information is verified. You can proceed to payment.", output)
        self.assertIn("SOPHIA MARIE DAVIS isn't compatible on your selected status.", output)
        self.assertIn("Balance to pay:", output)
        self.assertIn("If this person completed the payment process, kindly proceed to approval process.", output)
        self.assertIn("Davis, Sophia Marie has been successfully enrolled.", output)
        self.assertIn("Transaction finished.", output)
        self.assertIn("Checking your information.....", output)
        self.assertIn("Your information is verified. You can proceed to payment.", output)
        self.assertIn("Balance to pay:", output)
        self.assertIn("If this person completed the payment process, kindly proceed to approval process.", output)
        self.assertIn("Not approved by assigned personnel !!", output)
        self.assertIn("Checking your information.....", output)
        self.assertIn("Your information is verified. You can proceed to payment.", output)
        self.assertIn("Balance to pay:", output)
        self.assertIn("If this person completed the payment process, kindly proceed to approval process.", output)
        self.assertIn("Thompson, James Robert has been successfully enrolled.", output)
        self.assertIn("Transaction finished.", output)
        self.assertIn("Checking your information.....", output)
        self.assertIn("Your information is verified. You can proceed to payment.", output)
        self.assertIn("Balance to pay:", output)
        self.assertIn("If this person completed the payment process, kindly proceed to approval process.", output)
        self.assertIn("Johnson, Emily Anne has been successfully enrolled.", output)
        self.assertIn("Checking your information.....", output)
        self.assertIn("Your information is verified. You can proceed to payment.", output)
        self.assertIn("Balance to pay:", output)
        self.assertIn("If this person completed the payment process, kindly proceed to approval process.", output)
        self.assertIn("Thompson, James Robert is already enrolled.", output)
        self.assertIn("THANK YOU", output)

# Run Test_main tests
main_test_output = unittest.TextTestRunner().run(unittest.TestLoader().loadTestsFromTestCase(Test_main))
print(main_test_output)
print("\nTest_main()")
print("-" * 70)