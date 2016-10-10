#!/usr/bin/env python
# coding: utf-8
"""
Semi-optimized Collatz sequence generator.

Used as sample CPU-heavy code to test profiling.
"""


def collatz_seq(n):
    u"""
    Iterate over a sequence starting with `n`.

    Rules:

    The sequence starts with a seed and the following numbers are calculated
    with following formulas:

        n → n/2 (if n is even)
        n → 3n + 1 (if n is odd)

    The sequence ends when it reaches one 1. It is an open problem whether
    the sequence reaches one for all numbers.

    E.g. starting with 13:

        13 → 40 → 20 → 10 → 5 → 16 → 8 → 4 → 2 → 1

    :param int n: Collatz sequence beginning, positive integer > 0
    :rtype: generator object
    :return: a generator object over the Collatz sequence starting with `n`
    """
    assert n > 0, 'n must be a positive integer'
    while True:
        yield n
        if n == 1:
            return
        elif n % 2 == 0:
            n = n / 2
        else:
            n = 3 * n + 1


def seqs_lenghts_cached(max_n):
    """
    Calculate lengths of the series starting with integers ranging from zero to `max_n`.

    :param int max_n:
    :return: dict with keys of starting numbers of sequences and values
        of lengths of sequences
    """
    cache = {}  # key: first seq number, val: seq length

    for n in range(1, max_n + 1):
        seq_length = 0
        for i in collatz_seq(n):
            if i in cache:
                seq_length += cache[i]
                break
            else:
                seq_length += 1
        cache[n] = seq_length
    return cache


def longest_sequence(max_n):
    """Find the number that produces the longest sequence, from 1 to `max_n`, closed."""
    lengths = seqs_lenghts_cached(max_n)

    longest_chain = 0
    starting_number = 0
    for k, v in lengths.items():
        if v > longest_chain:
            starting_number = k
            longest_chain = v

    return starting_number


if __name__ == '__main__':
    from schaap import profiling
    with profiling(0.01):
        print longest_sequence(1000000)
