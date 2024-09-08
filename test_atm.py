import unittest
from unittest.mock import patch, MagicMock
from atm import ATM

class TestATM(unittest.TestCase):
    def setUp(self):
        self.atm = ATM('account_info_test.json')

    def test_validate_account_info_success(self):
        result = self.atm.validate_account_info("card_one", "1234", "checking")
        self.assertTrue(result)

    def test_validate_account_info_failure(self):
        result = self.atm.validate_account_info("card_one", "3333", "checking")
        self.assertFalse(result)

    def test_get_balance_initial(self):
        balance = self.atm.get_balance("card_one", "1234", "checking")
        self.assertEqual(balance, 500)

    def test_deposit_success(self):
        deposit_result = self.atm.deposit("card_one", "1234", "checking", 500)
        balance = self.atm.get_balance("card_one", "1234", "checking")
        self.assertTrue(deposit_result)
        self.assertEqual(balance, 1000)

    def test_withdraw_success(self):
        withdraw_result = self.atm.withdraw("card_two", "0000", "checking", 500)
        balance = self.atm.get_balance("card_two", "0000", "checking")
        self.assertTrue(withdraw_result)
        self.assertEqual(balance, 3500)

    def test_withdraw_failure(self):
        withdraw_result = self.atm.withdraw("card_two", "0000", "checking", 9000)
        self.assertFalse(withdraw_result)

    @patch('builtins.input', side_effect=["withdraw", "card_one", "1234", "checking", 50, "y",
                                          "deposit", "card_one", "1234", "checking", 500, "y",
                                          "withdraw", "card_two", "0000", "checking", 50, "n"])
    def test_user_interaction_flow_deposit_and_withdraw(self, mock_input):
        self.atm.user_interaction_flow()  
        current_balance_card_one_checking = self.atm.get_balance("card_one", "1234", "checking")
        current_balance_card_one_saving = self.atm.get_balance("card_one", "1234", "saving")
        current_balance_card_two_checking = self.atm.get_balance("card_two", "0000", "checking")
        self.assertEqual(current_balance_card_one_checking, 950)
        self.assertEqual(current_balance_card_one_saving, 9000)
        self.assertEqual(current_balance_card_two_checking, 3950)

if __name__ == '__main__':
    unittest.main()