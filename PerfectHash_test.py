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


class HashTest(unittest.TestCase):
    count = 1000
    data = DataSource.get_random(count)
    phash = PerfectHash(data)

    def test_equal(self):
        for key, val in self.data.iteritems():
            self.assertEqual(val, self.phash[key])

    def test_len(self):
        self.assertEqual(len(self.data), len(self.phash))
        self.assertEqual(len(self.data), self.count)


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
