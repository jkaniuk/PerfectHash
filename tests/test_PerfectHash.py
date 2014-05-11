import unittest
import random
import sys

from PerfectHash import PerfectHash


class DataSource(object):
    chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'

    @classmethod
    def get_random_word(cls, wordLen):
        word = ''
        for i in range(wordLen):
            word += random.choice(cls.chars)
        return word

    @classmethod
    def get_random(cls, count):
        data = {}
        for i in xrange(count):
            val = random.randint(0, count)
            while True:
                key = cls.get_random_word(random.randint(2, 10))
                if key not in data:
                    break
            data[key] = val
        return data


class BigTest(unittest.TestCase):
    count = 10000
    data = DataSource.get_random(count)
    phash = PerfectHash(data)

    def test_equal(self):
        for key, val in self.data.iteritems():
            self.assertEqual(val, self.phash[key])

    def test_len(self):
        self.assertEqual(len(self.data), len(self.phash))
        self.assertEqual(len(self.data), self.count)

    def test_memory(self):
        print sys.getsizeof(self.data)
        self.assertGreater(sys.getsizeof(self.data),
                           sys.getsizeof(self.phash) * 3)
        self.assertGreater(sys.getsizeof(self.data), 512)


class MultipleTest(unittest.TestCase):
    counts = [7, 10, 20, 50, 100, 200, 500, 1000]
    data = {i: DataSource.get_random(i) for i in counts}
    phashes = {i: PerfectHash(d) for i, d in data.iteritems()}

    def test_len(self):
        for count in self.counts:
            self.assertEqual(len(self.data[count]), len(self.phashes[count]))

    def test_equal(self):
        for count in self.counts:
            for key, val in self.data[count].iteritems():
                self.assertEqual(val, self.phashes[count][key])

    def test_memory(self):
        for count in self.counts[4:]:
            self.assertGreater(sys.getsizeof(self.data[count]),
                               sys.getsizeof(self.phashes[count]) * 3)
            self.assertGreater(sys.getsizeof(self.data[count]), 512)


class BruteTest(unittest.TestCase):
    counts = [1, 2, 3, 4, 5]

    def test_brute(self):
        for i in xrange(100):
            for count in self.counts:
                data = DataSource.get_random(count)
                phash = PerfectHash(data)
                self.assertEqual(len(data), len(phash))
                for key, val in data.iteritems():
                    self.assertEqual(val, phash[key])


class SmallTest(unittest.TestCase):
    data = {
        'a': 15,
        'b': 7,
        'ab': 10,
    }
    phash = PerfectHash(data)

    def test_equal(self):
        for key, val in self.data.iteritems():
            self.assertEqual(val, self.phash[key])

    def test_len(self):
        self.assertEqual(len(self.data), len(self.phash))
        self.assertEqual(len(self.phash), 3)

    def test_empty(self):
        phash = PerfectHash({})
        self.assertEqual(len(phash), 0)


def main():
    unittest.main()

if __name__ == '__main__':
    main()
