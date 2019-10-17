import math


def sieve_of_eratosthenes(n):
    possible_prime_numbers = list(range(2, n))
    for i in range(2, math.floor(math.sqrt(n))):
        if i in possible_prime_numbers:
            for j in range(2 * i, n, i):
                if j in possible_prime_numbers:
                    possible_prime_numbers.remove(j)
    return possible_prime_numbers


print(sieve_of_eratosthenes(100))