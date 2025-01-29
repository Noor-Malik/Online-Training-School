# Dictionaries
import operator
from itertools import count

#
# my_dict = dict(name='Noor', age=54, color="green")
# my_dict1 = { "name":'Noor', "age": 54, "color" : "green" }
# my_type = type(my_dict)
# my = my_dict.keys()
# my2 = my_dict.values()
# my1 = my_dict1.keys()
# my3 = my_dict.items()
# print(my, my1, my_type, my_dict1, my2)
# print(my3)
#
# for x in my_dict:
#     print(my_dict[x])
# name= my_dict["name"]
# print(name)
# for x in my_dict:
#     print(my_dict[x])
#
myfamily = {
  "child1" : {
    "name" : "Emil",
    "year" : 2004
  },
  "child2" : {
    "name" : "Tobias",
    "year" : 2007
  },
  "child3" : {
    "name" : "Linus",
    "year" : 2011
  }
}

for x, obj in myfamily.items():
    print(x)
    for y in obj:
        print(y + ':', obj[y])

# 1. Write a Python script to sort (ascending and descending) a dictionary by value.

# Import the 'operator' module, which provides functions for common operations like sorting.

# Create a dictionary 'd' with key-value pairs.
d = {1: 2, 3: 4, 4: 3, 2: 1, 0: 0}

# Print the original dictionary 'd'.
print('Original dictionary : ', d)

# Sort the items (key-value pairs) in the dictionary 'd' based on the values (1st element of each pair).
# The result is a list of sorted key-value pairs.
sorted_d = sorted(d.items(), key=operator.itemgetter(1))

# Print the dictionary 'sorted_d' in ascending order by value.
print('Dictionary in ascending order by value : ', sorted_d)

# Convert the sorted list of key-value pairs back into a dictionary.
# The 'reverse=True' argument sorts the list in descending order by value.
sorted_d = dict(sorted(d.items(), key=operator.itemgetter(1), reverse=True))

# Print the dictionary 'sorted_d' in descending order by value.
print('Dictionary in descending order by value : ', sorted_d)
d = {1: 10, 2: 20, 3: 30, 4: 40, 5: 50, 6: 60}

def is_key_present(x):
    if x in d:
        print('Key is present in the dictionary')
    else:
        print('Key is not present in the dictionary')

is_key_present(6)

# 5. Write a Python program to iterate over dictionaries using for loops.

a = {1: 2, 3: 4, 4: 3, 2: 1, 0: 0}

for i, j in a.items():
    print(i, j)

# practice Questions

input = [1,2,3,4,4,4,5,0,6,6,6,3,7,7,8,7]

def frequency_counter(input):
    empty = {}
    for x in input:
        empty[x] = count(x)
    return empty

frequency_counter(input)
print(frequency_counter)