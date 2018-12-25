# coding: utf-8

from __future__ import unicode_literals, absolute_import, division

import itertools


class HashTableV1(object):
    """
    Simple HashTable/Dict with fixed buckets

    """

    def __init__(self):
        self._container = [[] for _ in range(8)]

    def __setitem__(self, key, value):
        bucket = self._get_bucket_for_key(key)

        for idx, (item_key, item_value) in enumerate(bucket):
            if key == item_key:
                bucket[idx] = key, value
                return

        bucket.append((key, value))

    def __getitem__(self, item):
        for key, val in self._get_bucket_for_key(item):
            if key == item:
                return val

        raise KeyError(item)

    def _get_bucket_for_key(self, key):
        return self._container[hash(key) % len(self._container)]

    def items(self):
        for bucket in self._container:
            for pair in bucket:
                yield pair

    def __delitem__(self, key):
        bucket = self._get_bucket_for_key(key)

        for idx, (stored_key, stored_val) in enumerate(bucket):
            if key == stored_key:
                bucket[idx:] = bucket[idx + 1:]
                return

        raise KeyError(key)

    def __len__(self):
        return sum(map(len, self._container))


class HashTableV2(object):
    """
    HashTable/Dict with growing/shrinking buckets

    """

    def __init__(self):
        self._container = [[] for _ in range(self._INITIAL_CONTAINER_LEN)]

    _INITIAL_CONTAINER_LEN = 8

    def __setitem__(self, key, value):
        self._grow_if_necessary()
        bucket = self._get_bucket_for_key(key)

        for idx, (item_key, item_value) in enumerate(bucket):
            if key == item_key:
                bucket[idx] = key, value
                return

        bucket.append((key, value))

    def _get_used_buckets_count(self):
        return sum(1 for bucket in self._container if bucket)

    def _grow_if_necessary(self):
        """
        Multiplies the amount of buckets by two and resettles all elements

        """
        if self._get_used_buckets_count() < 2 * len(self._container) / 3:
            return

        existing_entries = list(self.items())

        self._container = [[] for _ in range(len(self._container) * 2)]

        for key, val in existing_entries:
            self[key] = val

    def __getitem__(self, item):
        for key, val in self._get_bucket_for_key(item):
            if key == item:
                return val

        raise KeyError(item)

    def _get_bucket_for_key(self, key):
        return self._container[hash(key) % len(self._container)]

    def items(self):
        for bucket in self._container:
            for pair in bucket:
                yield pair

    def __delitem__(self, key):
        self._shrink_if_necessary()

        bucket = self._get_bucket_for_key(key)

        for idx, (stored_key, stored_val) in enumerate(bucket):
            if key == stored_key:
                bucket[idx:] = bucket[idx + 1:]
                return

        raise KeyError(key)

    def _shrink_if_necessary(self):
        if len(self._container) == self._INITIAL_CONTAINER_LEN:
            return

        if self._get_used_buckets_count() > 2 * len(self._container) / 3:
            return

        pairs = list(self.items())

        self._container = [[] for _ in range(len(self._container) // 2)]

        for key, val in pairs:
            self[key] = val

    def __len__(self):
        return sum(map(len, self._container))


class HashTableV3(object):
    """
    HashTable/Dict that caches the hash values for improved performance when growing/shrinking,
    and also uses this hash for a more efficient key matching

    """

    def __init__(self):
        # Now bucket items consist of 3-tuple of (key, key-hash, value)
        self._container = [[] for _ in range(self._INITIAL_CONTAINER_LEN)]

    _INITIAL_CONTAINER_LEN = 8

    def __setitem__(self, key, value):
        self._grow_if_necessary()

        key_hash = hash(key)
        bucket = self._get_bucket_for_hash(key_hash)

        for idx, (stored_key, stored_key_hash, stored_value) in enumerate(bucket):
            if self._key_match(key, key_hash, stored_key, stored_key_hash):
                bucket[idx] = key, key_hash, value
                return

        bucket.append((key, key_hash, value))

    @staticmethod
    def _key_match(key_1, key_1_hash, key_2, key_2_hash):
        """
        Returns whether the keys match

        """
        # Since the keys can be any object implementing __eq__, we should delay
        # performing a comparison as much as possible, as the operation may be
        # very expensive.

        # First we check key identity: if keys are the same, they MUST be equal.
        # (you are equal to yourself, right?)
        # For purists: NaN will match itself
        if key_1 is key_2:
            return True

        # If two objects are equal, then they necessarily have the same hash,
        # therefore if two objects have different hashes, then they necessarily
        # are unequal objects
        if key_1_hash != key_2_hash:
            return False

        return key_1 == key_2

    def _get_used_buckets_count(self):
        return sum(1 for bucket in self._container if bucket)

    def _grow_if_necessary(self):
        """
        Multiplies the amount of buckets by two and resettles all elements

        """
        if self._get_used_buckets_count() < 2 * len(self._container) / 3:
            return

        self._resize_buckets(len(self._container) * 2)

    def __getitem__(self, key):
        key_hash = hash(key)

        for stored_key, stored_hash, stored_val in self._get_bucket_for_hash(key_hash):
            if self._key_match(key, key_hash, stored_key, stored_hash):
                return stored_val

        raise KeyError(key)

    def _get_bucket_for_hash(self, key_hash):
        return self._container[hash(key_hash) % len(self._container)]

    def items(self):
        for bucket in self._container:
            for key, _, val in bucket:
                yield key, val

    def __delitem__(self, key):
        self._shrink_if_necessary()

        key_hash = hash(key)

        bucket = self._get_bucket_for_hash(key_hash)

        for idx, (stored_key, stored_hash, stored_val) in enumerate(bucket):
            if self._key_match(key, key_hash, stored_key, stored_hash):
                bucket[idx:] = bucket[idx + 1:]
                return

        raise KeyError(key)

    def _resize_buckets(self, n):
        new_buckets = [[] for _ in range(n)]

        # Since we have the hashes, we don't need to recalculate them,
        # just transfer from the old bucket to the new one
        for bucket in self._container:
            for key, hash, val in bucket:
                new_buckets[hash % n].append((key, hash, val))

        self._container = new_buckets

    def _shrink_if_necessary(self):
        bucket_count = len(self._container)

        if bucket_count == self._INITIAL_CONTAINER_LEN:
            return

        if self._get_used_buckets_count() < bucket_count / 3:
            self._resize_buckets(bucket_count // 2)

    def __len__(self):
        return sum(map(len, self._container))


class HashTableV4(object):
    """
    HashTable/Dict not based on buckets/clusters but open addressing, i.e. a flat list,
    and clash resolution based on linear probing

    (This should be very close to Knuth's Algorithm D)

    """

    def __init__(self):
        self._container = [self._FREE_MARK for _ in range(self._INITIAL_CONTAINER_LEN)]

    _INITIAL_CONTAINER_LEN = 8

    def __setitem__(self, key, value):
        self._grow_if_necessary()

        key_hash = hash(key)

        pos = self._find_position_for_key_and_hash(key, key_hash)
        self._container[pos] = key, key_hash, value

    @staticmethod
    def _key_match(key_1, key_1_hash, key_2, key_2_hash):
        """
        Returns whether the keys match

        """
        # Since the keys can be any object implementing __eq__, we should delay
        # performing a comparison as much as possible, as the operation may be
        # very expensive.

        # First we check key identity: if keys are the same, they MUST be equal.
        # (you are equal to yourself, right?)
        # For purists: NaN will match itself
        if key_1 is key_2:
            return True

        # If two objects are equal, then they necessarily have the same hash,
        # therefore if two objects have different hashes, then they necessarily
        # are unequal objects
        if key_1_hash != key_2_hash:
            return False

        return key_1 == key_2

    def _grow_if_necessary(self):
        """
        Multiplies the amount of buckets by two and resettles all elements

        """
        if len(self) > 2 * len(self._container) / 3:
            self._resize_container(len(self._container) * 2)

    # NOTE: it would be better to have singletons for these markers like object()
    # but this makes debugging easier
    _FREE_MARK = 'FREE'
    _DELETED_MARK = 'DELETED'

    def __getitem__(self, key):
        key_hash = hash(key)

        pos = self._find_position_for_key_and_hash(key, key_hash)

        entry = self._container[pos]

        if not self._is_valid_entry(entry):
            raise KeyError(key)

        _, _, stored_val = entry

        return stored_val

    def _find_position_for_key_and_hash(self, key, hash):
        """
        Given a key and its hash, returns the position of the container where the entry
        should be stored/retrieved.

        """
        # Hash could be calculated here, but it is required for better perf.

        first_seen_deleted = None
        pos = hash % len(self._container)

        while True:
            entry = self._container[pos]

            if entry is self._DELETED_MARK:
                if first_seen_deleted is None:
                    first_seen_deleted = pos

            elif entry is self._FREE_MARK:
                if first_seen_deleted is not None:
                    return first_seen_deleted

                return pos

            elif self._key_match(key, hash, entry[0], entry[1]):
                return pos

            pos = (pos + 1) % len(self._container)

    def items(self):
        for entry in self._container:
            if self._is_valid_entry(entry):
                key, _, value = entry
                yield key, value

    def __delitem__(self, key):
        self._shrink_if_necessary()

        key_hash = hash(key)

        pos = self._find_position_for_key_and_hash(key, key_hash)

        entry = self._container[pos]

        if not self._is_valid_entry(entry):
            raise KeyError(key)

        self._container[pos] = self._DELETED_MARK

    def _resize_container(self, n):
        old_container = list(self._container)
        self._container = [self._FREE_MARK for _ in range(n)]

        for entry in old_container:
            if not self._is_valid_entry(entry):
                continue

            key, hash, _ = entry

            self._container[self._find_position_for_key_and_hash(key, hash)] = entry

    @classmethod
    def _is_valid_entry(cls, item):
        """
        Returns whether the passed item taken from the container is valid, in
        the sense that it is not empty or marked as deleted

        """
        return item is not cls._FREE_MARK and item is not cls._DELETED_MARK

    def _shrink_if_necessary(self):
        container_length = len(self._container)

        if container_length == self._INITIAL_CONTAINER_LEN:
            return

        if len(self) < container_length / 3:
            self._resize_container(container_length // 2)

    def __len__(self):
        return sum(1 for item in self._container if self._is_valid_entry(item))


class HashTableV5(HashTableV4):
    """
    HashTable based on open addressing and clash resolution consists of probing but not linearly,
    in order to avoid piling a lot of entries in the same region of the array.
    The next probing position is calculated with a congruential random number generator and
    dropping in some bits of the hash to jump to a seemingly random position.

    """

    def _find_position_for_key_and_hash(self, key, hash):
        """
        Given a key and its hash, returns the position of the container where the entry
        should be stored/retrieved.

        """
        first_seen_deleted = None
        pos = hash % len(self._container)

        perturbation = hash

        while True:
            entry = self._container[pos]

            if entry is self._DELETED_MARK:
                if first_seen_deleted is None:
                    first_seen_deleted = pos

            elif entry is self._FREE_MARK:
                if first_seen_deleted is not None:
                    return first_seen_deleted

                return pos

            elif self._key_match(key, hash, entry[0], entry[1]):
                return pos

            # Here comes the magic. In case of clash, we get some bits from the
            # hash, and mix it with a congruential random number generator.
            # This is reproducible, meaning we will always jump the same way for a
            # given hash and container length. At some point we will exhaust the
            # perturbation and only the RNG which is guaranteed to jump to every
            # position, so we will find a position no matter what.
            pos = (5 * pos + 1 + perturbation) % len(self._container)

            # Drop some bits to generate some pseudo randomness for the next time.
            # Why 5? that was the value I saw somewhere else, but should work perfectly
            # with only 1 bit.
            perturbation >>= 5
