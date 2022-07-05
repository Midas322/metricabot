from random import choice
from string import ascii_lowercase
n = 20


for i in range(1000):
    string_val = "".join(choice(ascii_lowercase) for j in range(n))
    print(string_val)