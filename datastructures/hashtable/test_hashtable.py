# coding: utf-8

from functools import partial
from pytest import raises
import string
import random

import hashtable


def get_random_string(len=20):
    return ''.join(random.choice(string.ascii_letters) for _ in range(len))


demo_values = {
    get_random_string(): get_random_string()
    for _ in range(100)
}


def _test_basic(hashtable_cls):
    h = hashtable_cls()

    for k, v in demo_values.items():
        h[k] = v

    for k, v in h.items():
        assert v == demo_values[k]


def _print_container(table):
    import pprint
    pprint.pprint(table._container, indent=2)


def _test_set_twice(cls):
    h = cls()

    h['lol'] = 'hello!'
    assert h['lol'] == 'hello!'

    h['lol'] = 'buongiorno!'

    assert h['lol'] == 'buongiorno!'


def _test_exception_on_missing_key(cls):
    h = cls()

    with raises(KeyError):
        h['im missing!']


def _test_delete_key(cls):
    h = cls()

    h['hey'] = 'ho'
    assert h['hey'] == 'ho'

    del h['hey']

    with raises(KeyError):
        h['hey']

    with raises(KeyError):
        del h['hey']


def _test_len(cls):
    h = cls()
    h['hey'] = 'there'
    assert len(h) == 1

    h['how'] = 'youdoing?'
    assert len(h) == 2


def _test_container_doesnt_shrink_below_initial_count(cls):
    h = cls()

    assert len(h._container) == h._INITIAL_CONTAINER_LEN

    h['hey'] = 'ho'
    del h['hey']

    assert len(h._container) == h._INITIAL_CONTAINER_LEN


def _test_container_grow_and_shrink(cls):
    h = cls()

    initial_container_count = len(h._container)

    for i in range(1000):
        h[i] = i

        if len(h._container) > initial_container_count:
            break

    else:
        raise AssertionError('Buckets count did not grow')

    # Check that the stuff is still retrievable
    assert h[i - 1] == i - 1

    buckets_count = len(h._container)

    for i in range(1000):
        del h[i]

        if len(h._container) < buckets_count:
            break

    else:
        raise AssertionError('Bucket count did not shrink')


test_basic_v1 = partial(_test_basic, hashtable.HashTableV1)
test_set_twice_v1 = partial(_test_set_twice, hashtable.HashTableV1)
test_exception_on_missing_key_v1 = partial(_test_exception_on_missing_key, hashtable.HashTableV1)
test_delete_key_v1 = partial(_test_delete_key, hashtable.HashTableV1)


test_basic_v2 = partial(_test_basic, hashtable.HashTableV2)
test_set_twice_v2 = partial(_test_set_twice, hashtable.HashTableV2)
test_exception_on_missing_key_v2 = partial(_test_exception_on_missing_key, hashtable.HashTableV2)
test_delete_key_v2 = partial(_test_delete_key, hashtable.HashTableV2)
test_container_doesnt_shrink_below_initial_count_v2 = partial(_test_container_doesnt_shrink_below_initial_count, hashtable.HashTableV2)
test_container_grow_and_shrink_v2 = partial(_test_container_grow_and_shrink, hashtable.HashTableV2)


test_basic_v3 = partial(_test_basic, hashtable.HashTableV3)
test_set_twice_v3 = partial(_test_set_twice, hashtable.HashTableV3)
test_exception_on_missing_key_v3 = partial(_test_exception_on_missing_key, hashtable.HashTableV3)
test_delete_key_v3 = partial(_test_delete_key, hashtable.HashTableV3)
test_container_doesnt_shrink_below_initial_count_v3 = partial(_test_container_doesnt_shrink_below_initial_count, hashtable.HashTableV3)
test_container_grow_and_shrink_v3 = partial(_test_container_grow_and_shrink, hashtable.HashTableV3)

test_basic_v4 = partial(_test_basic, hashtable.HashTableV4)
test_set_twice_v4 = partial(_test_set_twice, hashtable.HashTableV4)
test_exception_on_missing_key_v4 = partial(_test_exception_on_missing_key, hashtable.HashTableV4)
test_delete_key_v4 = partial(_test_delete_key, hashtable.HashTableV4)
test_container_doesnt_shrink_below_initial_count_v4 = partial(_test_container_doesnt_shrink_below_initial_count, hashtable.HashTableV4)
test_container_grow_and_shrink_v4 = partial(_test_container_grow_and_shrink, hashtable.HashTableV4)

test_basic_v5 = partial(_test_basic, hashtable.HashTableV5)
test_set_twice_v5 = partial(_test_set_twice, hashtable.HashTableV5)
test_exception_on_missing_key_v5 = partial(_test_exception_on_missing_key, hashtable.HashTableV5)
test_delete_key_v5 = partial(_test_delete_key, hashtable.HashTableV5)
test_container_doesnt_shrink_below_initial_count_v5 = partial(_test_container_doesnt_shrink_below_initial_count, hashtable.HashTableV5)
test_container_grow_and_shrink_v5 = partial(_test_container_grow_and_shrink, hashtable.HashTableV5)
