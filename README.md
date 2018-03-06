# pybloomf 

Implementation of Bloom filter algorithm. More details about algorithm [wikipedia](https://en.wikipedia.org/wiki/Bloom_filter)

### Installation
Two ways to install:

* Clone repo and execute
```
pip install .
```

* Pip install
```
pip install pybloomf
```

### Usage
* Create instance of BloomFilter class
```python
from pybloomf import BloomFilter
bf = BloomFilter(1000, 0.01)
```
* Add elements to filter
```python
bf.add('John')
bf.add('Smith')
```
* Check if element exists in filter
```python
'John' in bf
'Tom' in bf
```
* Get information about filter
```python
print(bf)
```

By default BloomFilter uses MurmurHashFunction class for hash generation. You can create your own custom hash generation function by subclassing BaseHashFunction. get_indexes method must be override with your custom logic. It must always return list of integers. These integers will be used as indexes for Bloom filter to set values to True.
```python
class CustomHash(BaseHashFunction):
    def __init__(self, num_of_filter_bits, num_of_hash_func):
        super().__init__(num_of_filter_bits, num_of_hash_func)

    def get_indexes(self, element):
        hash_list = []
        for i in range(self.num_of_hash_func):
            hash_list.append(abs((11 + i * len(element)) % self.num_of_filter_bits))

        return hash_list

bf = BloomFilter(20, 0.01)
bf.set_hash_function(CustomHash(bf.num_of_filter_bits, bf.num_of_hash_functions))
```

You can set number of bits to use in filter and number of hash functions to use.
```python
bf = BloomFilter(20, 0.01, num_of_filter_bits=30, num_of_hash_func=2)
```
If not set those values are calculated automatically by using expected number of items in filter and False Positive probability.