"""
Backpropagation worked example for beginners.

Network architecture:
    input layer:  2 neurons  (x1, x2)
    hidden layer: 2 neurons  (h1, h2), sigmoid activation
    output layer: 1 neuron   (y_hat), linear activation

This file implements:
    1. one detailed forward + backward step
    2. one gradient descent update
    3. a small training loop
    4. comments explaining what each line does
"""

import numpy as np  # NumPy gives us fast arrays and matrix math


# -----------------------------
# Activation function: sigmoid
# -----------------------------
def sigmoid(z):
    """Return the sigmoid of z.

    sigmoid(z) = 1 / (1 + e^(-z))
    This squashes any real number into the range (0, 1).
    """
    return 1.0 / (1.0 + np.exp(-z))  # np.exp computes e^z element-wise


def sigmoid_derivative_from_activation(a):
    """Return sigmoid'(z) when a = sigmoid(z) is already known.

    If a = sigmoid(z), then:
        sigmoid'(z) = a * (1 - a)
    This trick avoids recomputing sigmoid(z).
    """
    return a * (1.0 - a)  # element-wise multiplication works on arrays


# ---------------------------------------------
# Example 1: one detailed backpropagation step
# ---------------------------------------------
def one_training_step():
    """Perform one forward pass, one backward pass, and one parameter update."""

    print("=" * 60)
    print("ONE TRAINING STEP: detailed backpropagation")
    print("=" * 60)

    # -------------------------
    # Training example
    # -------------------------
    x = np.array([0.5, 0.8], dtype=float)  # input features x1 and x2
    y = 1.0                                # target value for regression

    # -------------------------
    # Initial parameters
    # -------------------------
    # W1 maps inputs to hidden layer: shape (2 inputs, 2 hidden neurons)
    W1 = np.array([
        [0.10, 0.20],   # row for x1: weights to h1 and h2
        [-0.10, 0.10],  # row for x2: weights to h1 and h2
    ], dtype=float)

    b1 = np.array([0.00, 0.00], dtype=float)  # biases for h1 and h2

    # W2 maps hidden layer to output: shape (2 hidden neurons, 1 output neuron)
    W2 = np.array([
        [0.50],   # weight from h1 to output
        [-0.50],  # weight from h2 to output
    ], dtype=float)

    b2 = np.array([0.00], dtype=float)  # bias for output neuron

    learning_rate = 0.5  # controls how large each parameter update is

    print("Input x:", x)
    print("Target y:", y)
    print("Initial W1:\n", W1)
    print("Initial b1:", b1)
    print("Initial W2:\n", W2)
    print("Initial b2:", b2)

    # -------------------------
    # Forward pass
    # -------------------------
    z1 = x @ W1 + b1              # hidden pre-activations: shape (2,)
    h1 = sigmoid(z1)              # hidden activations: shape (2,)
    z2 = h1 @ W2 + b2             # output pre-activation: shape (1,)
    y_hat = z2                    # linear output activation
    loss = 0.5 * (y - y_hat) ** 2 # squared error loss for one example

    print("\nForward pass")
    print("z1 = x @ W1 + b1 =", z1)
    print("h1 = sigmoid(z1) =", h1)
    print("z2 = h1 @ W2 + b2 =", z2)
    print("y_hat = z2 =", y_hat)
    print("loss =", loss)

    # -------------------------
    # Backward pass
    # -------------------------
    # dL/dy_hat = y_hat - y
    dL_dy_hat = y_hat - y

    # Output layer is linear, so dz2/dy_hat = 1
    delta_out = dL_dy_hat  # this is dL/dz2

    # Gradients for W2 and b2
    dL_dW2 = np.outer(h1, delta_out)  # because z2 = h1 @ W2 + b2
    dL_db2 = delta_out                # because z2 = h1 @ W2 + b2

    # Propagate delta back into hidden layer
    # delta_h = (delta_out @ W2.T) * sigmoid'(z1)
    delta_h = (delta_out @ W2.T) * sigmoid_derivative_from_activation(h1)

    # Gradients for W1 and b1
    dL_dW1 = np.outer(x, delta_h)  # because z1 = x @ W1 + b1
    dL_db1 = delta_h               # because z1 = x @ W1 + b1

    print("\nBackward pass")
    print("dL/dy_hat =", dL_dy_hat)
    print("delta_out =", delta_out)
    print("dL/dW2 =\n", dL_dW2)
    print("dL/db2 =", dL_db2)
    print("delta_h =", delta_h)
    print("dL/dW1 =\n", dL_dW1)
    print("dL/db1 =", dL_db1)

    # -------------------------
    # Gradient descent update
    # -------------------------
    W2 = W2 - learning_rate * dL_dW2  # move W2 opposite its gradient
    b2 = b2 - learning_rate * dL_db2  # move b2 opposite its gradient
    W1 = W1 - learning_rate * dL_dW1  # move W1 opposite its gradient
    b1 = b1 - learning_rate * dL_db1  # move b1 opposite its gradient

    print("\nAfter one update")
    print("Updated W1:\n", W1)
    print("Updated b1:", b1)
    print("Updated W2:\n", W2)
    print("Updated b2:", b2)


# ---------------------------------------
# Example 2: train for multiple steps
# ---------------------------------------
def train_for_multiple_steps():
    """Train the same network for several iterations on one example."""

    print("\n" + "=" * 60)
    print("TRAINING LOOP: multiple gradient descent steps")
    print("=" * 60)

    x = np.array([0.5, 0.8], dtype=float)  # fixed input example
    y = np.array([1.0], dtype=float)       # fixed target value

    W1 = np.array([
        [0.10, 0.20],
        [-0.10, 0.10],
    ], dtype=float)

    b1 = np.array([0.00, 0.00], dtype=float)

    W2 = np.array([
        [0.50],
        [-0.50],
    ], dtype=float)

    b2 = np.array([0.00], dtype=float)

    learning_rate = 0.5
    steps = 20  # number of gradient descent updates
    y_hat = b2.copy()  # initialized in case the training loop has zero steps

    for step in range(steps):
        # Forward pass
        z1 = x @ W1 + b1
        h1 = sigmoid(z1)
        z2 = h1 @ W2 + b2
        y_hat = z2
        loss = np.mean(0.5 * (y - y_hat) ** 2)  # scalar loss for this one example

        # Backward pass
        delta_out = y_hat - y
        dL_dW2 = np.outer(h1, delta_out)
        dL_db2 = delta_out
        delta_h = (delta_out @ W2.T) * sigmoid_derivative_from_activation(h1)
        dL_dW1 = np.outer(x, delta_h)
        dL_db1 = delta_h

        # Gradient descent update
        W2 -= learning_rate * dL_dW2
        b2 -= learning_rate * dL_db2
        W1 -= learning_rate * dL_dW1
        b1 -= learning_rate * dL_db1

        # Print progress occasionally so the output stays readable
        if step == 0 or (step + 1) % 5 == 0:
            print(f"step {step + 1:2d} | loss = {loss:.6f} | y_hat = {y_hat.item():.6f}")

    print("\nFinal prediction after training:", y_hat.item())
    print("Target was:", y[0])


# Run both examples when the script is executed directly
if __name__ == "__main__":
    one_training_step()       # show the detailed math on one example
    train_for_multiple_steps()  # show repeated updates reducing the loss