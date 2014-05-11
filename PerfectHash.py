import numpy as np


def find_next_prime(x):
    x = int(x)
    if x <= 2:
        return 2
    if x % 2 == 0:
        x += 1
    while True:
        for n in xrange(3, int(x ** 0.5) + 2, 2):
            if x % n == 0:
                break
        else:
            return x
        x += 2


class PerfectHash(object):

    maxd = 2 ** 31 - 1

    def __init__(self, data, debug=False):
        self.size = len(data)
        self._create(data, debug=debug)

    def _hash(self, item, d=None):
        if d is None:
            return hash(item) & 0xffffffff
        else:
            if not isinstance(item, basestring):
                item = str(hash(item) & 0xffffffff)
            seed = str(d)
            return hash(seed + item + seed) & 0xffffffff

    def _create(self, data, tfactor=1.23, debug=False):

        tsize = find_next_prime(tfactor * len(data) + 1)
        gsize = find_next_prime(tsize / 5)

        # Marker for empty slot
        empty_marker = float('-inf')

        # Intermediate table
        g = [0] * gsize
        # Values table
        t = [empty_marker] * tsize
        # Clusters of keys based on 1st level hash
        clusters = [[] for i in xrange(gsize)]
        # Needed for processing single item clusters
        empty_slots = []

        for key in data.iterkeys():
            clusters[self._hash(key) % gsize].append(key)

        # Iterate based on number of keys, descending
        for keys in sorted(clusters, key=len, reverse=True):

            # If more keys, find seed matching all
            if len(keys) >= 2:
                # Find d for which all keys have empty slots
                found = False
                for d in xrange(1, self.maxd):
                    slots = {}
                    for key in keys:
                        slot = self._hash(key, d=d) % tsize
                        assert slot >= 0
                        if t[slot] != empty_marker or slot in slots:
                            break
                        slots[slot] = key
                    else:
                        found = True
                    if found:
                        break
                else:
                    if debug:
                        print 'keys', keys, 'slots', slots
                        for i in [1, d]:
                            print [self._hash(x, i) for x in keys], 'd=', i
                    raise Exception("Perfect hash creation failed")

                # Update t table
                for slot, key in slots.iteritems():
                    t[slot] = data[key]
                # Update g table
                g[self._hash(keys[0]) % gsize] = d

            # For single items different behaviour:
            # assign first non empty field
            elif len(keys) == 1:
                # Only once: find empty slots
                if not empty_slots:
                    for idx, val in enumerate(t):
                        if val == empty_marker:
                            # Convert to negative offset
                            empty_slots.append(idx - tsize)

                # Get any empty slot
                slot = empty_slots.pop()
                # Update t table
                t[slot] = data[keys[0]]
                # Update g table
                g[self._hash(keys[0]) % gsize] = slot

            # Break when single item starts
            else:
                break

        # Pack tables
        self.g = np.array(g)
        for idx, val in enumerate(t):
            if val == empty_marker:
                t[idx] = False
        self.t = np.array(t)

    def __getitem__(self, key):
        d = self.g[self._hash(key) % len(self.g)]
        # If negative use as direct index
        if d < 0:
            return self.t[d]
        return self.t[self._hash(key, d=d) % len(self.t)]

    def __len__(self):
        return self.size
