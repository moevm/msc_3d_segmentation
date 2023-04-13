import numpy as np

# Define a 3D numpy array
arr = np.random.randint(0, 10, size=(5, 5, 5))

# Define the number of zero elements to add at each end
n = 2

# Add zero elements at the start of each dimension
new_arr = np.zeros((arr.shape[0]+n*2, arr.shape[1]+n*2, arr.shape[2]+n*2), dtype=arr.dtype)
new_arr[n:-n, n:-n, n:-n] = arr

# Print the original and the new arrays
print("Original array:")
print(arr)
print("\nNew array with zero elements at all ends:")
print(new_arr)