import csv
import GTC
import random
import keyboard

# file = ''
# with open(file, mode='a') as fp:

z = []
for i in range(10):
    y = random.randint(1, 50)
    z.append(y)
    print(z)
a = sum(z) / 10
print('Mean: {}'.format(a))



