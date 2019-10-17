import collections
import math


#podzielic na osobne plki przed wgraniem!

def wallis_product(n):
    result = 1
    for x in range(1, n):
        result = result * (2 * x * 2 * x) / ((2 * x - 1) * (2 * x + 1))

    return result * 2


def euclidean_algorithm(first_number, second_number):
    a = first_number
    b = second_number
    while b != 0:
        c = a % b
        a = b
        b = c
    return a


def sieve_of_eratosthenes(n):
    possible_prime_numbers = list(range(2, n))
    for i in range(2, math.floor(math.sqrt(n))):
        if i in possible_prime_numbers:
            for j in range(2 * i, n, i):
                if j in possible_prime_numbers:
                    possible_prime_numbers.remove(j)
    return possible_prime_numbers


def prime_factor_distribution(number):
    prime_numbers = list()
    for x in sieve_of_eratosthenes(number):
        if x < (number / 2):
            prime_numbers.append(x)
    factors = list()

    for x in prime_numbers:
        while number % x == 0:
            factors.append(x)
            number = int(number / x)

    return collections.Counter(factors)


def least_common_multiple(first_number, second_number):
    first_number_factors = prime_factor_distribution(first_number)
    second_number_factors = prime_factor_distribution(second_number)
    lcm_dict = {**first_number_factors, **second_number_factors}

    for k, v in first_number_factors.items():
        if k in lcm_dict:
            if v > lcm_dict.get(k):
                lcm_dict[k] = v

    lcm = 1
    for k, v in lcm_dict.items():
        lcm = lcm * pow(k, v)

    print(lcm)


least_common_multiple(192, 348)
print(sieve_of_eratosthenes(100))
print(format(wallis_product(10), '.10f'))
print(euclidean_algorithm(84, 18))
