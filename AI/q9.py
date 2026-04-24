
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
# Output data
y = np.array([4, 5, 6, 7])
# Create model
model = Sequential()
model.add(SimpleRNN(10, activation='relu', input_shape=(3, 1)))
model.add(Dense(1))
# Compile model
model.compile(optimizer='adam', loss='mse')
# Train model
model.fit(X, y, epochs=200, verbose=0)
# Test prediction
test_input = np.array([[[5], [6], [7]]])
prediction = model.predict(test_input)


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
print("Predicted Output:", prediction)