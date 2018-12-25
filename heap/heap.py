# coding: utf-8


class Heap(object):

    def __init__(self, items, key=lambda x: x):
        """
        :param items: Initial elements of heap. More can be added later
        :param key: In the typical case of sorting objects according to some characteristic,
            this must be a function that gets an item and returns the value to sort on.

        """
        self._container = []
        self._key = key

        for item in items:
            self.add(item)

    def add(self, item):
        cont = self._container

        cont.append(item)

        idx = len(cont) - 1

        while idx != 0:
            parent_idx = self._get_parent_index(idx)

            # Heap condition satisfied
            if self._key(cont[idx]) < self._key(cont[parent_idx]):
                return

            # Swap nodes and keep going
            cont[idx], cont[parent_idx] = cont[parent_idx], cont[idx]

            idx = parent_idx

    @staticmethod
    def _get_parent_index(idx):
        if idx == 0:
            raise ValueError('Index 0 cannot have a parent')

        quotient, remainder = divmod(idx, 2)
        parent_idx = quotient if remainder else quotient - 1

        return parent_idx

    @staticmethod
    def _get_left_child_index(idx):
        return idx * 2 + 1

    @staticmethod
    def _get_right_child_index(idx):
        return idx * 2 + 2

    def pop(self):
        cont = self._container

        if not cont:
            raise IndexError('pop from empty heap')

        top_item = cont[0]

        last_item = cont.pop()

        # If there was only one item
        if not cont:
            return top_item

        cont[0] = last_item
        self._reorder_heap_from_top()

        return top_item

    def _reorder_heap_from_top(self):
        cont = self._container
        key = self._key

        idx = 0

        while True:
            left_idx = self._get_left_child_index(idx)

            # No further children, heap condition has been met
            if not self._container_has_index(left_idx):
                return

            right_idx = self._get_right_child_index(idx)

            # No right, compare with left and eventually swap.
            # If there is no right child, the left child cannot have children,
            # therefore we exit here
            if not self._container_has_index(right_idx):
                if key(cont[left_idx]) > key(cont[idx]):
                    cont[left_idx], cont[idx] = cont[idx], cont[left_idx]
                return

            # There are both left and right children. Get the highest, swap and keep going
            if key(cont[left_idx]) > key(cont[right_idx]):
                cont[left_idx], cont[idx] = cont[idx], cont[left_idx]
                idx = left_idx

            else:
                cont[right_idx], cont[idx] = cont[idx], cont[right_idx]
                idx = right_idx

    def _container_has_index(self, idx):
        return len(self._container) > idx

    def peek(self):
        try:
            return self._container[0]

        except IndexError:
            raise IndexError('peek on empty heap')

    def __len__(self):
        return len(self._container)
