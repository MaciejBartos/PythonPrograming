
def wallis_product(n):
    result = 1
    for x in range(1, n):
        result = result * (2 * x * 2 * x) / ((2 * x - 1) * (2 * x + 1))

    return result * 2


print(format(wallis_product(10), '.10f'))