
def euclidean_algorithm(first_number, second_number):
    a = first_number
    b = second_number
    while b != 0:
        c = a % b
        a = b
        b = c
    return a


print(euclidean_algorithm(84, 18))