import unittest
import validation as val


class TestValidate(unittest.TestCase):
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

if __name__ == '__main__':
    unittest.main()
