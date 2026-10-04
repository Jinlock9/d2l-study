import math
import time
import numpy as np
import torch
from d2l import torch as d2l

# vectorization for speed
n = 10000
a = torch.ones(n)
b = torch.ones(n)

c = torch.zeros(n)
t = time.time()
for i in range(n):
    c[i] = a[i] + b[i]
print(f'{time.time() - t:.5f} sec')

t = time.time()
d = a + b
print(f'{time.time() - t:.5f} sec')