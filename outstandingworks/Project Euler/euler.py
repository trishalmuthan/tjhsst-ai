import time
import math

#problem 11
def problem11():
    grid = list()
    string_grid = '''
    08 02 22 97 38 15 00 40 00 75 04 05 07 78 52 12 50 77 91 08
    49 49 99 40 17 81 18 57 60 87 17 40 98 43 69 48 04 56 62 00
    81 49 31 73 55 79 14 29 93 71 40 67 53 88 30 03 49 13 36 65
    52 70 95 23 04 60 11 42 69 24 68 56 01 32 56 71 37 02 36 91
    22 31 16 71 51 67 63 89 41 92 36 54 22 40 40 28 66 33 13 80
    24 47 32 60 99 03 45 02 44 75 33 53 78 36 84 20 35 17 12 50
    32 98 81 28 64 23 67 10 26 38 40 67 59 54 70 66 18 38 64 70
    67 26 20 68 02 62 12 20 95 63 94 39 63 08 40 91 66 49 94 21
    24 55 58 05 66 73 99 26 97 17 78 78 96 83 14 88 34 89 63 72
    21 36 23 09 75 00 76 44 20 45 35 14 00 61 33 97 34 31 33 95
    78 17 53 28 22 75 31 67 15 94 03 80 04 62 16 14 09 53 56 92
    16 39 05 42 96 35 31 47 55 58 88 24 00 17 54 24 36 29 85 57
    86 56 00 48 35 71 89 07 05 44 44 37 44 60 21 58 51 54 17 58
    19 80 81 68 05 94 47 69 28 73 92 13 86 52 17 77 04 89 55 40
    04 52 08 83 97 35 99 16 07 97 57 32 16 26 26 79 33 27 98 66
    88 36 68 87 57 62 20 72 03 46 33 67 46 55 12 32 63 93 53 69
    04 42 16 73 38 25 39 11 24 94 72 18 08 46 29 32 40 62 76 36
    20 69 36 41 72 30 23 88 34 62 99 69 82 67 59 85 74 04 36 16
    20 73 35 29 78 31 90 01 74 31 49 71 48 86 81 16 23 57 05 54
    01 70 54 71 83 51 54 69 16 92 33 48 61 43 52 01 89 19 67 48
    '''
    string_grid = string_grid.strip()
    for line in string_grid.splitlines():
        cur_line = [int(number) for number in line.split()]
        grid.append(cur_line)
    current_max = 0
    for y_coord, row in enumerate(grid):
        for x_coord, col in enumerate(row):
            for xdirection in [-1, 0, 1]:
                for ydirection in [-1, 0, 1]:
                    if not (xdirection == 0 and ydirection == 0): 
                        current_product = 1
                        for num in range(0, 4):
                            x_pos = num * xdirection + x_coord
                            y_pos = num * ydirection + y_coord
                            if x_pos < 0 or y_pos < 0 or y_pos >= len(grid) or x_pos >= len(row): 
                                break
                            current_product *= grid[y_pos][x_pos]
                        if current_product > current_max:
                            current_max = current_product
    print(f'Problem 11: {current_max}')

#problem 12
def problem12():
    def num_divisors(number):
        num_factors = 0
        for i in range(1, int(math.ceil(number**0.5))+1):
            if number % i == 0:
                num_factors += 2
            if i*i==number:
                num_factors -= 1
        return num_factors

    x = 1
    for y in range(2,1000000):
        x += y
        if num_divisors(x) >= 500:
            print(f'Problem 12: {x}')
            break

#problem 14
def problem14():
    def collatz_length(n):
        count = 1
        while n > 1:
            if n % 2 == 0:
                n = n/2
                count += 1
            else:
                n = 3 * n + 1
                count += 1
            if n == 1:
                return count

    max_num = 0
    max_length = 0
    for i in range(1000000, 1, -1):
        cur_length = collatz_length(i)
        if cur_length > max_length:
            largest_number = i
            max_num = i
            max_length = cur_length
    
    print(f'Problem 14: {max_num}')

#problem 17
def problem17():
    number_lengths = dict()
    number_lengths[0] = 0
    number_lengths[1] = 3
    number_lengths[2] = 3
    number_lengths[3] = 5
    number_lengths[4] = 4
    number_lengths[5] = 4
    number_lengths[6] = 3
    number_lengths[7] = 5
    number_lengths[8] = 5
    number_lengths[9] = 4
    number_lengths[10] = 3
    number_lengths[11] = 6
    number_lengths[12] = 6
    number_lengths[13] = 8
    number_lengths[14] = 8
    number_lengths[15] = 7
    number_lengths[16] = 7
    number_lengths[17] = 9
    number_lengths[18] = 8
    number_lengths[19] = 8
    number_lengths[20] = 6
    number_lengths[30] = 6
    number_lengths[40] = 5
    number_lengths[50] = 5
    number_lengths[60] = 5
    number_lengths[70] = 7
    number_lengths[80] = 6
    number_lengths[90] = 6
    for num1 in range(21, 100):
        tens_dig = int(num1/10)*10
        ones_dig = num1 - tens_dig
        number_lengths[num1] = number_lengths[tens_dig] + number_lengths[ones_dig]
    for num2 in range(100,1000):
        hundreds = int(num2/100) #said as a single number
        tens_and_ones = num2 - (hundreds*100)
        if tens_and_ones == 0: #just the word hundred
            number_lengths[num2] = number_lengths[hundreds] + 7#hundred
        else:
            number_lengths[num2] = number_lengths[hundreds] + 10 + number_lengths[tens_and_ones]#hundredand
    number_lengths[1000] = 11 #onethousand
    total = 0
    for key, value in number_lengths.items():
        total += value
    print(f'Problem 17: {total}')

#problem 21
def problem21():
    def d(n):
        divisors = [x for x in range(1, int(n/2)+1) if n % x == 0]
        return sum(divisors)
    amicable = list()
    for num in range(1, 10000):
        divisors_a = d(num)
        divisors_b = d(divisors_a)
        if divisors_a != divisors_b and num == divisors_b:
            amicable.append(num)
    total = sum(amicable)
    print(f'Problem 21: {total}')

#problem 30
def problem30():
    def fifth_power(num_string):
        powers = [int(num_string[i])**5 for i in range(len(num_string))]
        return sum(powers)
    total = 0
    for num in range(10, 1000000):
        num_string = str(num)
        summed = fifth_power(num_string)
        if summed == num:
            total += summed
    print(f'Problem 30: {total}')


start = time.perf_counter()

problem11()
problem12()
problem14()
problem17()
problem21()
problem30()

end = time.perf_counter()

print(f'Total Time: {end - start} sec.')