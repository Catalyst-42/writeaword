import random

numbers = '0123456789'
symbols = '%*-+='


def generate_number():
    number = ''

    for n in range(random.randint(1, 5)):
        number += numbers[random.randint(0, len(numbers) - 1)]

    if random.randint(1, 5) == 1:
        number = '(' + number + ')' 
    
    return number


def generate_line():
    line = ''

    for n in range(10):
        line += generate_number() + ' ' + symbols[random.randint(0, len(symbols) - 1)] + ' '
    
    line += generate_number()
    
    return line


# generate all numline text file
with open('nl-text.txt', 'w') as f:
    for n in range(100):
        f.write(generate_line() + '\n')
