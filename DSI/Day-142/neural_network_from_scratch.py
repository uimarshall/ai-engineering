# cspell:ignore numpy sklearn matplotlib make_moons tanh sigmoid relu backprop backpropagation
"""
Deep Learning - Artificial Neural Networks (Practical, Beginner)
===============================================================
Companion code for:
    Deep_Learning_Artificial_Neural_Networks.md

This script teaches neural networks TWO ways, using one classic problem:

    PROBLEM: Two interleaving half-moons (the "make_moons" dataset).
    It is deliberately NON-linearly-separable, so a straight line (logistic
    regression) fails, but a neural network can carve a curved boundary.

PART A - Build a neural network FROM SCRATCH with only NumPy.
         You implement the forward pass, the loss, and backpropagation by hand.
         This is how you truly understand what "learning" means.

PART B - The SAME problem solved with scikit-learn's MLPClassifier
         (a production-ready neural network in 3 lines).
         Compare the two to see that the library is doing exactly what
         Part A did, just faster and with more features.

Run with:
    python neural_network_from_scratch.py
"""

# -------------------------------------------------------------
# 0. Import libraries
# -------------------------------------------------------------
import os  # to locate the script's own folder

import matplotlib  # plotting library

# Use a non-interactive backend ONLY if there is no display (servers/CI).
# On a normal laptop this keeps interactive windows; on headless it avoids errors.
if not os.environ.get("DISPLAY") and os.name != "nt":
    matplotlib.use("Agg")

import matplotlib.pyplot as plt  # the plotting module
import numpy as np  # fast arrays + math (the ONLY tool Part A needs)
from sklearn.datasets import make_moons  # generates the two-moons dataset
from sklearn.metrics import accuracy_score  # to score predictions
from sklearn.model_selection import train_test_split  # split data
from sklearn.neural_network import MLPClassifier  # production neural network
from sklearn.preprocessing import StandardScaler  # scale features to mean 0, std 1

# Make every run produce the same numbers (reproducibility).
np.random.seed(42)

# -------------------------------------------------------------
# 1. Load and prepare the data
# -------------------------------------------------------------
# make_moons() returns:
#   X -> shape (n_samples, 2)  the two coordinates of each point
#   y -> shape (n_samples,)    the label: 0 = bottom moon, 1 = top moon
X, y = make_moons(n_samples=1200, noise=0.18, random_state=42)

# Split into training (75%) and test (25%). stratify=y keeps the same
# class balance in both sets. The test set is our "exam" - never trained on.
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=42, stratify=y
)

# Neural networks train much better when features share a similar scale.
# StandardScaler makes each feature have mean 0 and standard deviation 1.
# IMPORTANT: fit the scaler on TRAINING data only, then reuse it on test data.
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)  # learn mean/std from train, then transform
X_test = scaler.transform(X_test)  # apply the SAME transform to test (no leakage)

print("=" * 65)
print("DATA READY")
print("=" * 65)
print(f"Total samples : {len(X)}")
print(f"Train samples : {len(X_train)}  |  Test samples: {len(X_test)}")
print(f"Features      : {X_train.shape[1]}  (x1, x2 coordinates)")
print(f"Classes       : {np.unique(y)}  (0 = bottom moon, 1 = top moon)")
print(f"Class balance : {y.mean():.1%} are class 1")


# =============================================================
# PART A: NEURAL NETWORK FROM SCRATCH (NumPy only)
# =============================================================
#
# A neural network is just stacked layers of: weighted sum -> activation.
# Here is the architecture we build:   2 inputs -> 8 hidden (tanh) -> 1 output (sigmoid)
#
#            x1 ──┐
#                 ├── [ 8 hidden neurons, tanh activation ] ──┐
#            x2 ──┘                                           ├── [ 1 output, sigmoid ] -> probability
#
# Each connection has a WEIGHT (W) and each neuron has a BIAS (b).
# "Training" = nudging all those W and b values so the output gets closer
# to the true label. The algorithm that computes how to nudge them is
# called BACKPROPAGATION.

# ---- 1a. Initialize the weights and biases -----------------
def initialize_parameters(n_x, n_hidden, n_y):
    """Create random starting weights and zero biases.

    Args:
        n_x:      number of input features  (2 here)
        n_hidden: number of hidden neurons  (8 here)
        n_y:      number of output neurons  (1 here)

    Returns:
        A tuple (W1, b1, W2, b2) - the learnable parameters.
    """
    # Weights are small random numbers. Multiplying by 0.5 keeps them from
    # being too large (which would saturate tanh and stall learning).
    W1 = np.random.randn(n_hidden, n_x) * 0.5  # shape (8, 2)
    b1 = np.zeros((n_hidden, 1))  # biases start at 0, shape (8, 1)
    W2 = np.random.randn(n_y, n_hidden) * 0.5  # shape (1, 8)
    b2 = np.zeros((n_y, 1))  # shape (1, 1)
    return W1, b1, W2, b2


# ---- 1b. Activation functions ------------------------------
def sigmoid(z):
    """Squash any real number into the range (0, 1). Used at the output.

    sigmoid(z) = 1 / (1 + e^(-z))
    A big positive z -> near 1 (probability of class 1).
    A big negative z -> near 0 (probability of class 0).
    """
    return 1 / (1 + np.exp(-z))


# ---- 1c. Forward pass (prediction) -------------------------
def forward_propagation(parameters, X):
    """Push the input X through the network to get predictions.

    Args:
        parameters: (W1, b1, W2, b2)
        X:          input, shape (n_features, n_samples)  <- note: samples are columns

    Returns:
        A2:    predicted probability of class 1, shape (1, n_samples)
        cache: intermediate values needed later by backpropagation
    """
    W1, b1, W2, b2 = parameters

    # --- Layer 1 (hidden) ---
    Z1 = W1 @ X + b1  # linear step: weighted sum of inputs + bias
    A1 = np.tanh(Z1)  # activation: tanh squashes to (-1, 1), adds non-linearity

    # --- Layer 2 (output) ---
    Z2 = W2 @ A1 + b2  # linear step on the hidden activations
    A2 = sigmoid(Z2)  # sigmoid -> probability between 0 and 1

    # Keep everything so backprop can use it.
    cache = (X, Z1, A1, Z2, A2)
    return A2, cache


# ---- 1d. Loss function (how wrong are we?) -----------------
def compute_loss(A2, Y):
    """Binary cross-entropy loss - the standard cost for 0/1 classification.

    loss = - (1/m) * sum[ Y*log(A2) + (1-Y)*log(1-A2) ]

    Intuition: if the true label is 1, we want A2 near 1 (small -log(A2)).
    If the true label is 0, we want A2 near 0 (small -log(1-A2)).
    Lower loss = better predictions.
    """
    m = Y.shape[1]  # number of samples
    # +1e-8 avoids log(0) which would be -infinity.
    loss = -np.sum(Y * np.log(A2 + 1e-8) + (1 - Y) * np.log(1 - A2 + 1e-8)) / m
    return loss


# ---- 1e. Backward pass (gradients) -------------------------
def backward_propagation(parameters, cache, Y):
    """Compute the gradient of the loss w.r.t. every weight and bias.

    The gradient tells us which direction to nudge each parameter to
    REDUCE the loss. This is the heart of "learning".
    """
    W1, b1, W2, b2 = parameters
    X, Z1, A1, Z2, A2 = cache
    m = X.shape[1]  # number of samples

    # --- Output layer gradients ---
    # For sigmoid + cross-entropy, the gradient simplifies nicely to (A2 - Y).
    dZ2 = A2 - Y  # "how wrong" the output is, shape (1, m)
    dW2 = dZ2 @ A1.T / m  # gradient for W2
    db2 = np.sum(dZ2, axis=1, keepdims=True) / m  # gradient for b2

    # --- Hidden layer gradients ---
    dA1 = W2.T @ dZ2  # propagate the error back to the hidden layer
    dZ1 = dA1 * (1 - A1 ** 2)  # tanh'(z) = 1 - tanh(z)^2
    dW1 = dZ1 @ X.T / m  # gradient for W1
    db1 = np.sum(dZ1, axis=1, keepdims=True) / m  # gradient for b1

    return dW1, db1, dW2, db2


# ---- 1f. Train the network (gradient descent loop) ---------
def train_network(X, y, n_hidden=8, learning_rate=0.1, n_epochs=6000):
    """Run the full training loop and return the learned parameters + history.

    Each epoch:
        1. Forward pass  -> predictions
        2. Compute loss  -> how wrong
        3. Backward pass -> gradients
        4. Update params -> parameters = parameters - learning_rate * gradient
    """
    # Reshape data so samples are columns (standard math convention).
    X = X.T  # shape (2, n_samples)
    Y = y.reshape(1, -1)  # shape (1, n_samples)

    parameters = initialize_parameters(X.shape[0], n_hidden, 1)  # 2 -> 8 -> 1
    loss_history = []  # record the loss every so often so we can plot it

    for epoch in range(n_epochs):
        # 1. Forward pass
        A2, cache = forward_propagation(parameters, X)

        # 2. Compute loss
        loss = compute_loss(A2, Y)

        # 3. Backward pass -> gradients
        dW1, db1, dW2, db2 = backward_propagation(parameters, cache, Y)

        # 4. Gradient descent update: move each parameter opposite the gradient
        W1, b1, W2, b2 = parameters
        parameters = (
            W1 - learning_rate * dW1,
            b1 - learning_rate * db1,
            W2 - learning_rate * dW2,
            b2 - learning_rate * db2,
        )

        # Record progress occasionally
        if epoch % 500 == 0:
            loss_history.append(loss)
            acc = np.mean((A2 > 0.5).astype(int) == Y)  # training accuracy
            print(f"  epoch {epoch:5d} | loss {loss:.4f} | train acc {acc:.3f}")

    return parameters, loss_history


print("\n" + "=" * 65)
print("PART A: NEURAL NETWORK FROM SCRATCH (NumPy)")
print("=" * 65)
print("Training 2 -> 8 (tanh) -> 1 (sigmoid), learning_rate=0.1, epochs=6000")

scratch_params, loss_history = train_network(
    X_train, y_train, n_hidden=8, learning_rate=0.1, n_epochs=6000
)

# ---- 1g. Evaluate on the test set --------------------------
def predict(parameters, X):
    """Return 0/1 predictions for X (shape n_samples x 2)."""
    A2, _ = forward_propagation(parameters, X.T)  # transpose to (2, n_samples)
    return (A2 > 0.5).astype(int).flatten()  # threshold 0.5 -> 0 or 1


scratch_pred = predict(scratch_params, X_test)
scratch_acc = accuracy_score(y_test, scratch_pred)
print(f"\nFrom-scratch TEST accuracy: {scratch_acc:.3f}")


# =============================================================
# PART B: THE SAME PROBLEM WITH scikit-learn (production)
# =============================================================
#
# The library does EXACTLY what Part A did, but:
#   - uses better optimizers (Adam) and early stopping
#   - is written in optimized C/Fortran (much faster)
#   - handles many layers, regularization, etc.
#
# hidden_layer_sizes=(8,) means one hidden layer with 8 neurons - same as Part A.

print("\n" + "=" * 65)
print("PART B: SAME NETWORK WITH scikit-learn (MLPClassifier)")
print("=" * 65)

mlp = MLPClassifier(
    hidden_layer_sizes=(8,),  # one hidden layer, 8 neurons (same shape as Part A)
    activation="tanh",  # same activation as Part A
    solver="adam",  # modern optimizer (better than plain gradient descent)
    max_iter=2000,  # cap training iterations
    random_state=42,  # reproducible
)
mlp.fit(X_train, y_train)  # .fit() runs the whole training loop internally

mlp_pred = mlp.predict(X_test)
mlp_acc = accuracy_score(y_test, mlp_pred)
print(f"scikit-learn MLP TEST accuracy: {mlp_acc:.3f}")

# ---- 2a. Visualize the decision boundary -------------------
def plot_decision_boundary(model, X_all, y_all, title, predict_fn):
    """Draw the learned boundary and shade the two regions.

    We make a grid of points covering the plot, ask the model to predict each,
    and color the grid by prediction. The boundary is where colors meet.
    """
    x_min, x_max = X_all[:, 0].min() - 0.5, X_all[:, 0].max() + 0.5
    y_min, y_max = X_all[:, 1].min() - 0.5, X_all[:, 1].max() + 0.5
    # Create a meshgrid of points to evaluate
    xx, yy = np.meshgrid(
        np.linspace(x_min, x_max, 300), np.linspace(y_min, y_max, 300)
    )
    grid = np.c_[xx.ravel(), yy.ravel()]  # shape (90000, 2)
    Z = predict_fn(model, grid).reshape(xx.shape)  # predict each grid point

    plt.figure(figsize=(7, 5))
    plt.contourf(xx, yy, Z, alpha=0.3, cmap="coolwarm")  # shaded regions
    plt.scatter(X_all[y_all == 0, 0], X_all[y_all == 0, 1], c="blue", s=15, label="class 0")
    plt.scatter(X_all[y_all == 1, 0], X_all[y_all == 1, 1], c="red", s=15, label="class 1")
    plt.title(title)
    plt.xlabel("feature 1")
    plt.ylabel("feature 2")
    plt.legend()
    plt.tight_layout()
    plt.show()


# Combine train + test so the picture shows the whole dataset
X_all = np.vstack([X_train, X_test])
y_all = np.concatenate([y_train, y_test])

# Plot A: from-scratch network boundary
plot_decision_boundary(
    scratch_params,
    X_all,
    y_all,
    f"Part A - From-Scratch NN (test acc {scratch_acc:.3f})",
    predict_fn=lambda _m, grid: predict(scratch_params, grid),
)

# Plot B: scikit-learn boundary
plot_decision_boundary(
    mlp,
    X_all,
    y_all,
    f"Part B - scikit-learn MLP (test acc {mlp_acc:.3f})",
    predict_fn=lambda model, grid: model.predict(grid),
)

# ---- 2b. Plot the training loss curve ----------------------
plt.figure(figsize=(7, 4))
plt.plot(range(0, len(loss_history) * 500, 500), loss_history, marker="o")
plt.xlabel("epoch")
plt.ylabel("loss")
plt.title("Part A - Loss going down = the network is learning")
plt.grid(alpha=0.3)
plt.tight_layout()
plt.show()


# =============================================================
# PART C: SUMMARY
# =============================================================
print("\n" + "=" * 65)
print("SUMMARY")
print("=" * 65)
print(f"""
Both approaches solved the same non-linear problem:

  From scratch (NumPy) : {scratch_acc:.1%} test accuracy
  scikit-learn MLP      : {mlp_acc:.1%} test accuracy

What you just implemented by hand in Part A:
  1. initialize_parameters  -> random starting weights
  2. forward_propagation    -> predict (weighted sum -> tanh -> sigmoid)
  3. compute_loss           -> measure error (binary cross-entropy)
  4. backward_propagation   -> gradients (which way to nudge each weight)
  5. the training loop      -> repeat: predict, measure, adjust

That loop IS deep learning. scikit-learn just wraps it in a convenient,
fast, battle-tested package.
""")