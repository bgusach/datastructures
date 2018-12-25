# coding: utf-8


from pytest import raises
from heap import Heap


#                             0
#              1                                2
#       3               4               5               6
#   7       8       9       10      11      12      13      14
# 15  16  17  18  19  20  21  22  23  24  25  26  27  28  29  30


def test_parent_index():
    for idx, expected_result in [
        (1, 0),
        (2, 0),
        (3, 1),
        (13, 6),
        (14, 6),
        (26, 12),
        (19, 9),
    ]:
        result = Heap._get_parent_index(idx)
        assert result == expected_result

    with raises(ValueError):
        Heap._get_parent_index(0)


def test_children_indices():
    for idx, left, right in [
        (0, 1, 2),
        (1, 3, 4),
        (5, 11, 12),
        (8, 17, 18),
        (14, 29, 30),
    ]:
        assert left == Heap._get_left_child_index(idx)
        assert right == Heap._get_right_child_index(idx)


def test_container_has_index():
    heap = Heap([1, 2])

    assert heap._container_has_index(0)
    assert heap._container_has_index(1)
    assert not heap._container_has_index(2)
    assert not heap._container_has_index(200)


def test_peek():
    assert Heap([1, 10, 7]).peek() == 10
    assert Heap([1, 3, 7, 89, 3, 2]).peek() == 89

    h = Heap([1, 3, 7, 89, 3, 2])
    pre_len = len(h)
    h.peek()

    assert pre_len == len(h)


def test_pop():
    initial = [1, 10, 23, 45]
    h = Heap(initial)

    for item in sorted(initial, reverse=True):
        assert h.pop() == item


def test_add():
    h = Heap([7, 8, 1])
    assert h.peek() == 8

    h.add(23)
    assert h.peek() == 23


def test_len():
    items = [7, 8, 1]
    assert len(items) == len(Heap(items))


def test_heap_by_key():
    items = [
        {'name': 'lol', 'val': 54},
        {'name': 'troll', 'val': 13},
        {'name': 'n00b', 'val': 89},
    ]

    h = Heap(
        items=items,
        key=lambda x: x['val'],
    )

    assert h.pop() == items[2]
    assert h.pop() == items[0]
    assert h.pop() == items[1]


