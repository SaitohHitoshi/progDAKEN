import numpy as np

# data = np.random.randn(2,3)
# print(data)
# data = data*10
# print(data)

data1=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10.1, 12,2]

arr1=np.array(data1)
print(arr1)
print(arr1.dtype)

arr1_toint32=arr1.astype(np.int32)
print(arr1_toint32)