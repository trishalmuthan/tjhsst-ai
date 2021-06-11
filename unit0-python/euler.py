#Done
def is_prime(num):
    if num == 2:
        return True
    if num % 2 == 0 or num == 1:
        return False
    for i in range(2, int(num ** 0.5)+1):
        if num % i == 0:
            return False
    return True

#Done
def problem1():
    return sum([num for num in range(1000) if num % 3 == 0 or num % 5 == 0])

#Done
def problem2():
    fib1 = 1
    fib2 = 1
    total = 0
    while fib2 <= 4000000:
        if fib2 % 2 == 0:
            total += fib2
        fib1, fib2 = fib2, fib1+fib2
    return total

#Done
def problem3():
    number1 = 600851475143

    i1 = 2

    while i1 < number1:
        if number1 % i1 == 0:
            number1 = number1//i1
            i1 = 1
        i1 += 1

    return number1

#Done
def problem4():
    arr = list()
    for i in range(999, 99, -1):
        for j in range(999, 99, -1):
            multi = i*j
            if str(multi) == str(multi)[::-1]:
                arr.append(multi)
    return max(arr)

#Done
def problem8():
    num = "7316717653133062491922511967442657474235534919493496983520312774506326239578318016984801869478851843858615607891129494954595017379583319528532088055111254069874715852386305071569329096329522744304355766896648950445244523161731856403098711121722383113622298934233803081353362766142828064444866452387493035890729629049156044077239071381051585930796086670172427121883998797908792274921901699720888093776657273330010533678812202354218097512545405947522435258490771167055601360483958644670632441572215539753697817977846174064955149290862569321978468622482839722413756570560574902614079729686524145351004748216637048440319989000889524345065854122758866688116427171479924442928230863465674813919123162824586178664583591245665294765456828489128831426076900422421902267105562632111110937054421750694165896040807198403850962455444362981230987879927244284909188845801561660979191338754992005240636899125607176060588611646710940507754100225698315520005593572972571636269561882670428252483600823257530420752963450"
    largest = 0
    for i in range(0, len(num)-12):
        numbers = list(num[i:i+13])
        for j in range(len(numbers)):
            numbers[j] = int(numbers[j])
        value = 1
        for k in numbers:
            value *= k
        if value > largest:
            largest = value
    return largest

#Done
def problem9():
    for c in range(0, 1001):
        for b in range(0, c):
            for a in range(0, b):
                if a + b + c == 1000:
                    if a**2 + b**2 == c**2:
                        return a * b * c

#Done    
def problem7():
    count = 0
    for i in range(1, 1000000):
        if is_prime(i):
            count += 1
        if count == 10001:
            return i

print(problem7())
print(problem1())
print(problem2())
print(problem3())
print(problem4())
print(problem8())
print(problem9())