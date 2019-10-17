import collections
from primes_era import sieve_of_eratosthenes


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