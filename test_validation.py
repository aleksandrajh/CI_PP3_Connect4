import unittest
import validation

class TestValidate(unittest.TestCase):
    def test_validate_email(self):
        self.assertTrue(validation.validate_user_email('testemail@gmail.com'), True)

    def test_validate_wrong_email(self):
        self.assertEqual(validation.validate_user_email('465432'), None)

if __name__ == '__main__':
    unittest.main()