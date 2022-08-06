
import random
import timeit
import csv

def radix_sort(num_list, b):
    """
    :param num_list: numbers in a list can be empty
    :param b: base
    :return: a sorted list
    time complexity: O((N+b)M)
    N := is the time complexity of radix pass
    b := base
    M := the number of digits in the largest number in the input list, represents in b
    """
    if len(num_list) == 0:          # O(1) check the array is empty
        return []
    count = max(num_list)           # choose the max value from the num_list
    exp = 0                         # exponential growth
    holder = []
    while b ** exp <= count:        # base ** growth must be smaller than count
        if exp == 0:                # when exp == 0 input: num_list
            holder = radix_pass(num_list, b, exp)
        else:
            holder = radix_pass(holder, b, exp)     # after the first pass use holder
        exp += 1                    # will run for b**exp time
    return holder                   # Overall time complexity O((N+b)M)

def radix_pass(num_list, b, exp):
    """
    :param num_list: passed by radix sort
    :param b: base
    :param exp: 10 to provide the correct digit
    time complexity: O(N)
    N := total number of integers in the input list
    """
    count_array = [0] * b                     # insert the value for each count
    aux_array = [0] * len(num_list)           # tmp array to store the numbers
    for i in range(len(num_list)):            # loop for finding the decimal value
        digit = (num_list[i] // (b**exp)) % b # the decimal value will increase by exp
        count_array[digit] += 1               # insert the number in the count_array to keep track
    count_array[0] -= 1                       # let the first count_array minus one
    for j in range(1, len(count_array)):      # loop to add count_array[j] = count_array[j] + count_array[j-1](previous)
        count_array[j] += count_array[j-1]
    counter = len(num_list) - 1               # reverse pointer
    for k in range(len(aux_array)):
        digits = (num_list[counter] // (b**exp)) % b # the decimal value will increase by exp
        aux_array[count_array[digits]] = num_list[counter]  # find the correct bucket
        count_array[digits] -= 1
        counter -= 1
    return aux_array                # each for loop will run for O(n) time for each call


def time_radix_sort():
    """
    :param: None
    test time taken for radix sort
    for five different bases try out with the test data
    and write directly to the file
    then return output
    """
    output = []
    test_data = [random.randint(1, (2**64)-1) for _ in range(100000)]
    base = [2, 3, 5, 1999, 1457630, 9000000]
    for k in range(len(base)):
        start = timeit.default_timer()
        radix_sort(test_data, base[k])
        fin = timeit.default_timer() - start
        output.append((base[k], fin))
        with open('Assignment1', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(output)
    return output


def find_rotations(string_list, p):
    if len(string_list) == 0:           # O(1) check the string_list if empty or not
        return []
    final = []  # O(1)
    for k in range(len(string_list)):   # find empty strings and append to output
        if string_list[k] == "":        # if the current string is empty
            final.append(string_list[k])    # add the result straight to final which is the return variable
            try:                            # handle index error exception
                string_list[k] = string_list.pop()  # then replace the last element to the k-th place O(1) accessing
            except IndexError:
                pass                        # when the array consist one element only that is empty string
            break
    int_array, count_array = convert(string_list)   # O(NM)  go to convert
    if count_array == [] and int_array == []:       # handle empty strings
        return final
    copy = []                                      # O(1)
    for i in range(len(int_array)):             # O(N)
        copy.append(int_array[i])
    aug = rotate(int_array, count_array, p)     # O(N) go to rotate
    ori = join_functions(copy, count_array)     # O(NM) go to join function
    agm = join_functions(aug, count_array)      # O(NM)
    for i in ori:                               # O(N)
        agm.append(i)
    result = radix_sort(agm, 10)                # O(NM)
    t = 0
    k = 1
    order = []                           # O(1)
    while k < len(result):               # O(N) time taken to loop through result once
        if result[t] == result[k]:       # find the same integer
            order.append(result[t])
        t += 1
        k += 1
    counter = 0
    count_array = []
    done = []
    res = []
    previous = 0
    for j in order:                                     # O(n) loop in order
        for z in str(j):                                # convert j into string to loop it
            res.append(z)                               # add the str in location
            if len(res) == 2 and previous != 1:         # location len == 2 and previous value isn't 1
                location = "".join(res)
                done.append(int(location))              # append location into done
                res = []                                # clear location
                counter += 1                            # counter is the length of the character in a string
            elif len(res) == 3:
                location = "".join(res)
                done.append(int(location))              # same as above but append for length three location
                res = []
                counter += 1
            previous = int(z)                           # keep track of 1
        count_array.append(counter)                     # append length
        counter = 0                                     # clear counter
    out = rotate_back(done, count_array, p)             # O(N)
    fin = []
    b = 0
    for i in out:                                       # inside the numbers
        fin.append(str(chr(i)))                         # for every number will convert to chr
        counter += 1                                    # then counter will keep track of the total length of chr
        if count_array[b] == counter:                   # if the length matches the the count_array[current]
            output = "".join(fin)                       # then append the result and clear counter and fin
            final.append(output)
            fin = []
            counter = 0
            b += 1                                      # b will be incremented to the next char length
    return final

def convert(string_list):
    """
    :param string_list
    :return: result is the character converted to int, and the length of each character
    time complexity: O(NM) length of string_list * length of character
    """
    result = []                     # result the character that has been converted to int
    counter = 0                     # count the length of each character
    count_array = []                # append the length of each character
    for i in string_list:
        for k in i:                 # it will point to the single character in the string
            result.append(ord(k))   # append ord(character)
            counter += 1            # count the total length of the string
        count_array.append(counter) # after done with counting append count length to count_array
        counter = 0                 # reset counter
    return result, count_array

def join_functions(to_join, count_array):
    """
    :param to_join: characters that represents as numbers
    :param count_array: the length of the character
    :return: joined number
    time complexity: O(NM) length of string_list * length of character
    """
    res = []                # result array
    output = []             # output array
    t = 0                   # pointer
    previous = 0            # previous is to add the previous length in the count_array
    i = 0
    while i < len(to_join) + 1:                 # depends on the numbers in the to_join array
        if i == count_array[t] + previous:      # if the count_array[current] + count_array[previous]
            done = "".join(res)                 # join together
            output.append(int(done))            # append it as integer
            res = []                            # erase res
            if len(to_join) == i:               # avoid over looping
                pass
            else:
                res.append((str(to_join[i])))   # continue to append str(int) to res
                previous += count_array[t]      # previous has been incremented to find the next character
                t += 1                          # t is the pointer to the length in count_array
        else:
            res.append(str(to_join[i]))         # otherwise append str(int) to res
        i += 1                                  # i pointer to the to_join array
    return output

def rotate(int_array, count_array, p):
    """
    :param int_array: array of integer
    :param count_array: array of length
    :param p: rotation
    :return: rotated int array
    time complexity: O(N) rotation time taken
    """
    previous = 0
    for i in range(len(count_array)):               # O(count_array) = O(N) liner time
        if p % count_array[i] == 0:                 # if rotation of p % count_array[current] == 0
            previous += count_array[i]              # don't rotate and append the count_array[current] to previous
        else:
            var = p % count_array[i]                        # var will be > than count_array[current]
            while var > 0:                                  # loop for var times O(var)
                tmp = int_array[previous]    # take the first element from the int_array, previous is the next character
                for k in range(count_array[i]):             # O(count_array[current])
                    if len(int_array) == k + previous + 1:  # if len(int_array) == last element
                        pass
                    else:
                        int_array[k+previous] = int_array[k+previous+1]      # int_array[current] = int_array[current+1]
                int_array[count_array[i]+previous-1] = tmp      # insert the tmp to the last element
                var -= 1
            previous += count_array[i]          # increment previous with count_array[current]
    return int_array

def rotate_back(int_array, count_array, p):
    """"
    :param int_array: array of integer
    :param count_array: array of length
    :param p: rotation
    :return: rotated int array
    time complexity: O(N) rotation time taken
    IMPORTANT!! Everything is same as rotate but the var
    """
    previous = 0
    for i in range(len(count_array)):
        var = count_array[i] - (p % count_array[i])         # it will find the rotation needed to rotate back
        while var > 0:
            tmp = int_array[previous]
            for k in range(count_array[i]):
                if len(int_array) == k + previous + 1:
                    pass
                else:
                    int_array[k+previous] = int_array[k+previous+1]
            int_array[count_array[i]+previous-1] = tmp
            var -= 1
        previous += count_array[i]
    return int_array

# num_list = [170, 45, 75, 90, 802, 24, 2, 66]
# num_list = [30,60,93,87,28,89,19,99]
# b = 4
# num_list = [18446744073709551615,
#             18446744073709551614,
#             1, 11111111111111111111,
#             2111111111111111111,
#             311111111111111111]
# print(radix_sort(num_list, b))

# print(time_radix_sort())
# string_list = ["aaa", "abc", "cab", "acb", "wxyz", "yzwx"]
# p = 1
# print(find_rotations(string_list, p))


