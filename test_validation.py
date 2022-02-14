import unittest
import validation as val


class TestValidate(unittest.TestCase):
    """
    Verification of the user email and user name
    input values and types
    """
    def test_validate_email(self):
        self.assertTrue(val.validate_user_email('testemail@gmail.com'), True)

    def test_validate_wrong_email(self):
        self.assertEqual(val.validate_user_email('465432'), None)

    def test_validate_username(self):
        self.assertTrue(val.validate_username('Aleks'), True)

    def test_validate_wrong_username(self):
        self.assertEqual(val.validate_username('A1'), None)
        self.assertEqual(val.validate_username('AveryLongPlayername'), None)
        self.assertEqual(val.validate_username(123), False)


class TestUsersLogInOrRegistration(unittest.TestCase):
    """
    Verification of the input parameters
    for the players log in and registration
    """
    def test_log_in(self):
        self.assertTrue(val.log_in_players(['User1', 'User2']), True)
        self.assertEqual(val.log_in_players(123), None)

    def test_register_players(self):
        self.assertTrue(val.register_new_players(['User1', 'User2']), True)
        self.assertEqual(val.register_new_players(123), None)


if __name__ == '__main__':
    unittest.main()
