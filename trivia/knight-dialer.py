# coding: utf-8

# Extracted from:
# https://hackernoon.com/google-interview-questions-deconstructed-the-knights-dialer-f780d516f029

# Problem:
# Imagine a telephone dialer like this:
#
#       1  2  3
#       4  5  6
#       7  8  9
#          0
#
# And a knight chess piece is placed on a given number, being able to move only in L shape.
#
# Given an starting number and a number of hops, count how many possible combinations of
# numbers is it possible to create.

from __future__ import unicode_literals, print_function

from timeit import default_timer as timer

edges = {
    1: [6, 8],
    2: [7, 9],
    3: [4, 8],
    4: [3, 9, 0],
    5: [],
    6: [1, 7, 0],
    7: [2, 6],
    8: [1, 3],
    9: [4, 2],
    0: [4, 6],
}


def sol_1(number, hops):
    # Generate each possible solution and then count them.
    # This is about O(n^2) in time since each extra hop kind of doubles
    # the recursion calls.

    # N N -> [[N]]
    def yield_solutions(number, hops):
        if not hops:
            yield [number]

        else:
            for next_number in edges[number]:
                for subsolution in yield_solutions(next_number, hops - 1):
                    yield [number] + subsolution

    return sum(1 for _ in yield_solutions(number, hops))


def sol_2(number, hops):
    # Don't generate solutions, just count them
    if not hops:
        return 1

    return sum(
        sol_2(next_number, hops - 1)
        for next_number in edges[number]
    )


def sol_3(number, hops):
    # Memoize to avoid repeated function calls.
    # Linear in time and space, although the stack may overflow.

    cache = {}

    def do_it(number, hops):
        if not hops:
            return 1

        call_args = number, hops

        if call_args not in cache:
            res = sum(
                do_it(next_number, hops - 1)
                for next_number in edges[number]
            )

            cache[call_args] = res

        return cache[call_args]

    return do_it(number, hops)


def sol_4(number, hops):
    # If you draw the recursion call tree, you get an extra layer for
    # each hop until you hit the zero-hops layers, where no more calls are needed,
    # and concrete numbers can be generated the edge case).
    #
    # With this approach the tree is built from bottom up, i.e. start with
    # the 0-hops-layer for all possible number inputs [0.. 9] (which is a list full of 1's),
    # and then knowing that the combination count of a number is the sum of the counts of
    # the numbers that land onto that initial number, we can build the 1-hops-layer.
    # Then rinse and repeat up to the desired layer. In other words the N-layer is
    # induced from the (N-1)-layer.
    #
    # This is constant in space and linear in time, and there is no risk of
    # stack overflow.

    NUMBER_COUNT = 10

    # Zero layer. If no hops, the count of combinations for each starting number is 1
    sol = [1] * NUMBER_COUNT

    for _ in range(hops):
        prev = sol.copy()

        for idx in range(NUMBER_COUNT):
            # The number of combinations starting from this number
            # is equal to the sum of combination that can jump onto
            # this number
            sol[idx] = sum(prev[source] for source in edges[idx])

    return sol[number]


def test(fn):
    start = timer()
    res = fn(1, 18)

    print('Function: %s, returned: %s, elapsed: %s secs' % (fn.__name__, res, timer() - start))


if __name__ == '__main__':
    test(sol_1)
    test(sol_2)
    test(sol_3)
    test(sol_4)
