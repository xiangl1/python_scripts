#!/usr/bin/env python3

import numpy as np
x, y = np.loadtxt('test.txt',unpack=True)

sumup = np.zeros(y.size+1)

for i in range(0,y.size-5):
	sumup[i] = np.sum(y[i:i+5])
print(sumup)	
