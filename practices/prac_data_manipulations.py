import torch

x = torch.arange(12, dtype=torch.float)
print(x)
print(x.numel())
print(x.shape)

x1 = x.reshape(3, 4)
x2 = x.reshape(-1, 4)
x3 = x.reshape(3, -1)
print(x)
print(x1)
print(x2)
print(x3)

print(torch.zeros((2, 3, 4)))
print(torch.ones((2, 3, 4)))
print(torch.randn(3, 4))
print(torch.tensor([[2, 1, 4, 3], [1, 2, 3, 4], [4, 3, 2, 1]]))

# indexing and slicing
print(x1[-1])
print(x1[1:3])

x1[1, 2] = 17
print(x1)
x1[:2, :] = 12
print(x1)

# operations
x4 = torch.exp(x)
print(x4)

x = torch.tensor([1.0, 2, 4, 8])
y = torch.tensor([2, 2, 2, 2])
print(x + y, x - y, x * y, x / y, x ** y)

X = torch.arange(12, dtype=torch.float32).reshape((3,4))
Y = torch.tensor([[2.0, 1, 4, 3], [1, 2, 3, 4], [4, 3, 2, 1]])
print(torch.cat((X, Y), dim=0))
print(torch.cat((X, Y), dim=1))
print(X == Y)
print(X.sum())

# broadcasting
a = torch.arange(3).reshape((3, 1))
b = torch.arange(2).reshape((1, 2))
print(a, b)
print(a + b)

# saving memory
before = id(Y)
Y = Y + X
print(id(Y) == before)

Z = torch.zeros_like(Y)
print('id(Z):', id(Z))
Z[:] = X + Y
print('id(Z):', id(Z))

before = id(X)
X += Y
print(id(X) == before)

# conversion to other python objects
A = X.numpy()
B = torch.from_numpy(A)
print(type(A), type(B))

a = torch.tensor([3.5])
print(a, a.item(), float(a), int(a))