import unittest
from pybloomf.bloom_filter import BloomFilter, BaseHashFunction


class TestStaticFunctions(unittest.TestCase):
    def setUp(self):
        pass

    def test_number_of_filter_bits(self):
        self.assertEqual(BloomFilter.calc_num_of_filter_bits(100, 0.1), 480)
        self.assertEqual(BloomFilter.calc_num_of_filter_bits(1000, 0.001), 14378)

    def test_number_of_hash_functions(self):
        self.assertEqual(BloomFilter.calc_num_of_hash_func(480, 100), 3)
        self.assertEqual(BloomFilter.calc_num_of_hash_func(14378, 1000), 10)

    def test_element_add_to_filter(self):
        bf = BloomFilter(100, 0.001)
        self.assertNotEqual(bf.add('John'), None)
        self.assertNotEqual(bf.add('Smith'), None)

    def test_element_contains(self):
        bf = BloomFilter(100, 0.001)
        bf.add('John')

        self.assertEqual('John' in bf, True)
        self.assertEqual('Bill' in bf, False)

    def test_elements_count(self):
        bf = BloomFilter(100, 0.001)

        for i in range(10):
            bf.add('John' + str(i))

        self.assertEqual(len(bf), 10)

    def test_false_positive_calculation(self):
        bf = BloomFilter(100, 0.001)

        for i in range(200):
            bf.add('John' + str(i))

        self.assertEqual(bf.false_positive_probability(), 0.05716698536110719)

    def test_custom_hash_function(self):
        class CustomHash(BaseHashFunction):
            def __init__(self, num_of_filter_bits, num_of_hash_func):
                super().__init__(num_of_filter_bits, num_of_hash_func)

            def get_indexes(self, element):
                hash_list = []
                for i in range(self.num_of_hash_func):
                    hash_list.append(abs((11 + i * len(element)) % self.num_of_filter_bits))

                return hash_list

        bf = BloomFilter(20, 0.01, num_of_filter_bits=30, num_of_hash_func=2)
        bf.set_hash_function(CustomHash(bf.num_of_filter_bits, bf.num_of_hash_functions))

        self.assertEqual(bf.add('Tom'), [11, 14])
        self.assertEqual(bf.add('Peter'), [11, 16])


if __name__ == '__main__':
    unittest.main()
