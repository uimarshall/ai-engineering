# Backpropagation — A Complete Beginner Tutorial with a Worked Example

Backpropagation is the algorithm that trains neural networks. It answers one practical question:

> “Given the error at the output, how much should each weight change?”

By the end of this tutorial you will understand:

- What a neural network computes forward
- What a loss function measures
- What a gradient means
- How the chain rule produces gradients for every weight
- A tiny fully worked numerical example
- Python code that trains the same network

---

## 1. The smallest useful neural network

We will use a network with:

- **2 inputs**
- **1 hidden layer with 2 neurons**
- **1 output neuron**

That is a **2-2-1 network**:

```text
x1 ──(w1)──▶ h1 ──(w5)──▶ y_hat
x1 ──(w2)──▶ h2 ──(w6)──▶ y_hat

x2 ──(w3)──▶ h1 ──(w5)──▶ y_hat
x2 ──(w4)──▶ h2 ──(w6)──▶ y_hat
```

Each hidden neuron also has a bias:

- hidden neuron 1 has bias `b1`
- hidden neuron 2 has bias `b2`
- output neuron has bias `b3`

So we have **7 parameters** total:

```text
w1, w2, w3, w4, b1, b2    # input → hidden
w5, w6, b3                 # hidden → output
```

Wait: that is 9 parameters. Let us list them carefully.

Input-to-hidden weights:

```text
w1: x1 → h1
w2: x1 → h2
w3: x2 → h1
w4: x2 → h2
```

Hidden biases:

```text
b1: bias for h1
b2: bias for h2
```

Hidden-to-output weights:

```text
w5: h1 → y_hat
w6: h2 → y_hat
```

Output bias:

```text
b3: bias for y_hat
```

Total parameters:

```text
w1, w2, w3, w4, b1, b2, w5, w6, b3
```

That is **9 learnable numbers**.

---

## 2. Activation functions

We need two activation choices.

### Hidden layer: sigmoid

The sigmoid squashes any number into the range `(0, 1)`:

```text
sigmoid(z) = 1 / (1 + e^(-z))
```

Its derivative is very convenient:

```text
sigmoid'(z) = sigmoid(z) * (1 - sigmoid(z))
```

### Output layer: linear

For regression, it is easiest to make the output layer linear:

```text
y_hat = z_out
```

That keeps the worked example simple.

---

## 3. Forward pass: from inputs to prediction

Suppose we have one training example:

```text
x1 = 0.5
x2 = 0.8
true target y = 1.0
```

Choose initial parameters:

```text
w1 = 0.10
w2 = 0.20
w3 = -0.10
w4 = 0.10
b1 = 0.00
b2 = 0.00
w5 = 0.50
w6 = -0.50
b3 = 0.00
```

---

### Step 1: hidden pre-activations

For hidden neuron 1:

```text
z_h1 = w1*x1 + w3*x2 + b1
     = 0.10*0.5 + (-0.10)*0.8 + 0.00
     = 0.05 - 0.08
     = -0.03
```

For hidden neuron 2:

```text
z_h2 = w2*x1 + w4*x2 + b2
     = 0.20*0.5 + 0.10*0.8 + 0.00
     = 0.10 + 0.08
     = 0.18
```

---

### Step 2: hidden activations

Apply sigmoid:

```text
h1 = sigmoid(-0.03)
   = 1 / (1 + e^(0.03))
   ≈ 0.4925
```

```text
h2 = sigmoid(0.18)
   ≈ 0.5448
```

---

### Step 3: output pre-activation

Because the output layer is linear:

```text
z_out = w5*h1 + w6*h2 + b3
      = 0.50*0.4925 + (-0.50)*0.5448 + 0.00
      = 0.24625 - 0.27240
      = -0.02615
```

So the prediction is:

```text
y_hat = -0.02615
```

The target was `y = 1.0`, so the prediction is bad. That is good for learning: now backprop has something to fix.

---

## 4. Loss function: measure the mistake

Use mean squared error for one example:

```text
L = 1/2 * (y - y_hat)^2
```

The `1/2` is only there to cancel the exponent when differentiating.

Compute the loss:

```text
L = 1/2 * (1.0 - (-0.02615))^2
  = 1/2 * (1.02615)^2
  ≈ 1/2 * 1.0530
  ≈ 0.5265
```

We want to make `L` smaller by changing the parameters.

---

## 5. The key idea: derivatives tell us direction and size

For a parameter `p`, the derivative

```text
dL/dp
```

means:

> “If I increase `p` a tiny amount, how fast does the loss change?”

Gradient descent updates each parameter like this:

```text
p_new = p_old - learning_rate * dL/dp
```

- If `dL/dp` is positive, increasing `p` increases loss, so we decrease `p`.
- If `dL/dp` is negative, increasing `p` decreases loss, so we increase `p`.

The learning rate controls step size.

---

## 6. Backpropagation with the chain rule

Backpropagation is not magic. It is just the chain rule applied in an efficient order.

We want gradients for:

```text
w5, w6, b3, w1, w2, w3, w4, b1, b2
```

The smartest order is:

1. Compute `dL/dy_hat`
2. Compute `dL/dz_out`
3. Compute gradients for `w5`, `w6`, `b3`
4. Use those to compute gradients for hidden-layer parameters
5. Update all parameters

---

## 7. Output layer gradients

### 7.1 Gradient of loss with respect to prediction

Given:

```text
L = 1/2 * (y - y_hat)^2
```

Then:

```text
dL/dy_hat = -(y - y_hat) = y_hat - y
```

Numerically:

```text
dL/dy_hat = -0.02615 - 1.0 = -1.02615
```

Interpretation: to reduce loss, we should increase `y_hat`, because its gradient is negative.

---

### 7.2 Gradient with respect to output pre-activation

Since output is linear:

```text
y_hat = z_out
```

so:

```text
dL/dz_out = dL/dy_hat = -1.02615
```

Define:

```text
delta_out = dL/dz_out = -1.02615
```

---

### 7.3 Gradients for `w5`, `w6`, and `b3`

The output pre-activation is:

```text
z_out = w5*h1 + w6*h2 + b3
```

Therefore:

```text
dL/dw5 = dL/dz_out * dz_out/dw5
       = delta_out * h1
       = -1.02615 * 0.4925
       ≈ -0.5054
```

```text
dL/dw6 = delta_out * h2
       = -1.02615 * 0.5448
       ≈ -0.5590
```

```text
dL/db3 = delta_out * 1
       = -1.02615
```

These already tell us something important: both `w5` and `w6` should increase because their gradients are negative.

---

## 8. Hidden layer gradients

Now we propagate the error backward into the hidden layer.

For hidden neuron 1:

```text
z_h1 = w1*x1 + w3*x2 + b1
h1 = sigmoid(z_h1)
```

Its contribution to the output is through:

```text
z_out = w5*h1 + w6*h2 + b3
```

By the chain rule:

```text
dL/dh1 = dL/dz_out * dz_out/dh1
       = delta_out * w5
       = -1.02615 * 0.50
       = -0.513075
```

Then:

```text
dL/dz_h1 = dL/dh1 * dh1/dz_h1
         = delta_out * w5 * h1 * (1 - h1)
         = -0.513075 * 0.4925 * (1 - 0.4925)
         = -0.513075 * 0.4925 * 0.5075
         ≈ -0.1283
```

Define:

```text
delta_h1 = dL/dz_h1 ≈ -0.1283
```

Similarly for hidden neuron 2:

```text
dL/dh2 = delta_out * w6
       = -1.02615 * (-0.50)
       = 0.513075
```

```text
dL/dz_h2 = delta_out * w6 * h2 * (1 - h2)
         = 0.513075 * 0.5448 * (1 - 0.5448)
         = 0.513075 * 0.5448 * 0.4552
         ≈ 0.1272
```

Define:

```text
delta_h2 = dL/dz_h2 ≈ 0.1272
```

Notice the signs changed because `w6` is negative. This is the “credit assignment” part of backprop: the network figures out which hidden neurons helped or hurt the output.

---

### 8.1 Gradients for input-to-hidden weights

The hidden pre-activation for `h1` is:

```text
z_h1 = w1*x1 + w3*x2 + b1
```

So:

```text
dL/dw1 = delta_h1 * x1
       = -0.1283 * 0.5
       ≈ -0.06415
```

```text
dL/dw3 = delta_h1 * x2
       = -0.1283 * 0.8
       ≈ -0.10264
```

For `h2`:

```text
dL/dw2 = delta_h2 * x1
       = 0.1272 * 0.5
       ≈ 0.0636
```

```text
dL/dw4 = delta_h2 * x2
       = 0.1272 * 0.8
       ≈ 0.1018
```

Biases:

```text
dL/db1 = delta_h1 ≈ -0.1283
dL/db2 = delta_h2 ≈ 0.1272
```

---

## 9. Gradient summary

All gradients for this one example are approximately:

```text
dL/dw1 ≈ -0.06415
dL/dw2 ≈  0.06360
dL/dw3 ≈ -0.10264
dL/dw4 ≈  0.10180
dL/db1 ≈ -0.12830
dL/db2 ≈  0.12720
dL/dw5 ≈ -0.50540
dL/dw6 ≈ -0.55900
dL/db3 ≈ -1.02615
```

Now update parameters with gradient descent.

Use learning rate:

```text
learning_rate = 0.5
```

---

## 10. Parameter update example

Update rule:

```text
p_new = p_old - learning_rate * dL/dp
```

### Output weights

```text
w5_new = 0.50 - 0.5*(-0.5054) = 0.50 + 0.2527 = 0.7527
w6_new = -0.50 - 0.5*(-0.5590) = -0.50 + 0.2795 = -0.2205
b3_new = 0.00 - 0.5*(-1.02615) = 0.513075
```

### Hidden weights and biases

```text
w1_new = 0.10 - 0.5*(-0.06415) = 0.132075
w2_new = 0.20 - 0.5*(0.0636)   = 0.1682
w3_new = -0.10 - 0.5*(-0.10264)= -0.04868
w4_new = 0.10 - 0.5*(0.1018)   = 0.0491
b1_new = 0.00 - 0.5*(-0.1283)  = 0.06415
b2_new = 0.00 - 0.5*(0.1272)   = -0.0636
```

After one update, the network is slightly better aligned with reducing the loss.

---

## 11. The backpropagation recipe

For this network, the full algorithm is:

1. Forward pass

- compute `z_h1`, `z_h2`
- compute `h1 = sigmoid(z_h1)`, `h2 = sigmoid(z_h2)`
- compute `z_out = w5*h1 + w6*h2 + b3`
- prediction `y_hat = z_out`

2. Compute loss

- `L = 1/2 * (y - y_hat)^2`

3. Output delta

- `delta_out = y_hat - y`

4. Output gradients

- `dL/dw5 = delta_out * h1`
- `dL/dw6 = delta_out * h2`
- `dL/db3 = delta_out`

5. Hidden deltas

- `delta_h1 = delta_out * w5 * h1 * (1 - h1)`
- `delta_h2 = delta_out * w6 * h2 * (1 - h2)`

6. Hidden gradients

- `dL/dw1 = delta_h1 * x1`
- `dL/dw2 = delta_h2 * x1`
- `dL/dw3 = delta_h1 * x2`
- `dL/dw4 = delta_h2 * x2`
- `dL/db1 = delta_h1`
- `dL/db2 = delta_h2`

7. Gradient descent update

- subtract `learning_rate * gradient` from each parameter

8. Repeat for many examples or batches until loss decreases

---

## 12. Intuition: what backprop is really doing

Backpropagation does three things:

### A. Assign blame

The output error is measured first. Then the algorithm asks:

> “Which weights caused this error?”

### B. Split responsibility

If a hidden neuron strongly influenced a wrong output, it gets more blame. If it barely influenced the output, it gets little blame.

That is why the hidden deltas include terms like:

```text
delta_out * w5
```

A hidden neuron matters more if its outgoing weight is large.

### C. Update in the direction that reduces loss

If increasing a weight increases loss, gradient descent decreases it. If increasing a weight decreases loss, gradient descent increases it.

---

## 13. Common beginner confusions

### Confusion 1: “Is backpropagation the same as gradient descent?”

No.

- **Backpropagation** computes gradients.
- **Gradient descent** uses those gradients to update weights.

### Confusion 2: “Why do we need the chain rule?”

Because the loss depends on parameters indirectly.

Example:

```text
w1 affects z_h1
z_h1 affects h1
h1 affects z_out
z_out affects y_hat
y_hat affects loss
```

So `dL/dw1` must multiply several derivatives together.

### Confusion 3: “Why do we compute gradients from output back to input?”

Because each layer’s gradient depends on the next layer’s gradient. It is cheaper to reuse earlier computations than recompute everything from scratch.

### Confusion 4: “Why use sigmoid in this example?”

Because its derivative is easy:

```text
sigmoid'(z) = sigmoid(z)(1 - sigmoid(z))
```

In real deep networks, people often use ReLU, but sigmoid is easier for a first worked example.

---

## 14. Mini exercise

Try changing one number in the worked example and recompute one gradient.

For example, set:

```text
w5 = 0.8
```

Then:

```text
dL/dh1 = delta_out * w5
       = -1.02615 * 0.8
       = -0.82092
```

So `h1` receives more blame than before.

That is the heart of backprop: **weights determine how responsibility flows backward**.

---

## 15. What the Python code does

The accompanying Python file `backprop_worked_example.py` contains:

- the exact same 2-2-1 network
- a forward pass
- a backward pass
- parameter updates
- a tiny training loop
- comments explaining each line

Run it to see the loss go down.

---

## 16. Final takeaway

Backpropagation is just repeated application of the chain rule from the loss back to every parameter.

Once you can compute:

```text
delta_out = y_hat - y
```

and then propagate deltas backward with weights and activation derivatives, you understand the core of neural network training.

The rest is scale: more layers, more neurons, better optimizers, and more data.
