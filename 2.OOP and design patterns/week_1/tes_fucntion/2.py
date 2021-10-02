import unittest

def factorize(x):
    """
    Factorize positive integer and return its factors.
    :type x: int,>=0
    :rtype: tuple[N],N>0
    """
    # raise TypeError
    pass

class TestFactorize(unittest.TestCase):
    def test_wrong_types_raise_exception(self):
        list_ = ['string',  1.5]
        for x in list_:
            with self.subTest(i=x):
                self.assertRaises(TypeError, factorize, x)

    def test_negative(self):
        list_ = [ -1,  -10,  -100]
        for x in list_:
            with self.subTest(i=x):
                self.assertRaises(ValueError, factorize, x)

    def test_zero_and_one_cases(self):
        list_ = [(0, (0,)),  (1, (1,))]
        for x, ans in list_:
            with self.subTest(i=x):
                self.assertEqual(factorize(x), ans)
    #
    def test_simple_numbers(self):
        list_ = [(3, (3,)),  (13, (13,)), (29, (29,))]
        for x, ans in list_:
            with self.subTest(i=x):
                self.assertEqual(factorize(x), ans)

    def test_two_simple_multipliers(self):
        list_ = [(6, (2, 3)), (26, (2, 13)), (121, (11, 11))]
        for x, ans in list_:
            with self.subTest(i=x):
                self.assertEqual(factorize(x), ans)

    def test_many_multipliers(self):
        list_ = [(1001, (7, 11, 13)), (9699690 , (2, 3, 5, 7, 11, 13, 17, 19))]
        for x, ans in list_:
            with self.subTest(i=x):
                self.assertEqual(factorize(x), ans)