

# creates list of configurations for k 'ones' in n 'zeros', returned as integers
def configurations(n, k):

    el = (1 << k) - 1
    out = [el]
    while el < (((1 << k) - 1) << n-k):
        el = next_perm(el)
        out.append(el)

    return out


def next_perm(v):
    """
    Generates next permutation with a given amount of set bits,
    given the previous lexicographical value.
    Taken from http://graphics.stanford.edu/~seander/bithacks.html
    """
    t = (v | (v - 1)) + 1
    w = t | ((((t & -t) / (v & -v)) >> 1) - 1)

    return w
