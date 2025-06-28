import unittest

class Tests(unittest.TestCase):
    def test_1(self):
        self.assertEqual((1+1), 2)

if __name__ == '__main__':
    unittest.main()