import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import SimpleRNN, Dense
# Input data (sequence)
X = np.array([
[[1], [2], [3]],
[[2], [3], [4]],
[[3], [4], [5]],
[[4], [5], [6]]
])

y = np.array([4, 5, 6, 7])

model = Sequential()
model.add(SimpleRNN(10, activation='relu', input_shape=(3, 1)))
model.add(Dense(1))

model.compile(optimizer='adam', loss='mse')

model.fit(X, y, epochs=200, verbose=0)

testInput = np.array([[[5], [7]]])
prediction = model.predict(testInput)

print("Predicted Output", prediction)

# Algorithm
# 1. Import required libraries (NumPy, TensorFlow/Keras).
# 2. Prepare input data as sequences (X) and corresponding outputs (y).
# 3. Initialize the RNN model.
# 4. Add SimpleRNN layer with suitable number of neurons.
# 5. Add Dense layer for output.
# 6. Compile the model using optimizer and loss function.
# 7. Train the model using training data.
# 8. Test the model with new input.
# 9. Display predicted output.