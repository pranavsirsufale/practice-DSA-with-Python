# 5x5 input image
image = [
    [1, 2, 3, 0, 1],
    [4, 5, 6, 1, 2],
    [7, 8, 9, 2, 3],
    [1, 3, 5, 4, 6],
    [2, 4, 6, 5, 7]
]

# 3x3 filter (kernel)
kernel = [
    [1, 0, -1],
    [1, 0, -1],
    [1, 0, -1]
]

# Output will be 3x3
output = [[0 for _ in range(3)] for _ in range(3)]

# Convolution operation
for i in range(3):        # rows of output
    for j in range(3):    # cols of output
        sum_val = 0

        # Apply kernel
        for ki in range(3):
            for kj in range(3):
                sum_val += image[i + ki][j + kj] * kernel[ki][kj]

        output[i][j] = sum_val

# Print result
print("Output Image:")
for row in output:
    print(row)