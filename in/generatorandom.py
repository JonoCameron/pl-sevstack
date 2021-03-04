import os
import random

print('hello random')

file = open('randomnumbers.txt', 'w')

for i in range(1024):
    line = str(random.randrange(0, 999)) + "\n"
    file.write(line)

file.close()