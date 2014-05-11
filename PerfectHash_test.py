import unittest
import random

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


class MultipleTest(unittest.TestCase):
    counts_small = [1, 2, 3, 4, 5]
    counts_big = [7, 10, 20, 50, 100, 200, 500, 1000]

    def test_equal(self):
        for count in self.counts_big:
            data = DataSource.get_random(count)
            phash = PerfectHash(data)
            self.assertEqual(len(data), len(phash))
            for key, val in data.iteritems():
                self.assertEqual(val, phash[key])

    def test_brute(self):
        for i in xrange(100):
            for count in self.counts_small:
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
