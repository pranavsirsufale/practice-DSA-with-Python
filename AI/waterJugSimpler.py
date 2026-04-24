"""
Algorithm: 
1. Initialize two variables a and b as empty jar
2. repeat until a = 2 (taraget),
    a) if jug b is empty fill it completely
    b) else if jub a is full, empty it.
    c) otherwise, pour water from jug b to jug a until (either a is full or b becomes empty)
"""


x, y, target = 4, 3, 2
a, b = 0, 0 
while a != target:
    if b == 0:
        b = y
        print(a, b)
    
    elif a == x:
        a = 0
        print(a, b)
    
    else:
        pour = min(b, x-a)
        b -= pour
        a += pour
        print(a, b)