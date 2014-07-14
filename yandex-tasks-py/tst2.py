import numpy
import array


a1 = array.array('I')
a2 = array.array('L')

a1.append(1)
a2.append(1)

print(bin(a1[0]))
print(bin(a2[0]))

a1.byteswap()
a2.byteswap()

print(bin(a1[0]))
print(bin(a2[0]))