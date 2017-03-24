
def nativeSum(x):
    counts = x['values']
    return reduce(lambda a, b: a + b, 0, counts)
