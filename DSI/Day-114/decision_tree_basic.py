import numpy as np
import pandas as pd
from sklearn.tree import DecisionTreeRegressor, plot_tree
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

# Create a small made-up lemonade stand dataset
rng = np.random.default_rng(42)
n = 200
temp = rng.uniform(5, 36, n)
rain = rng.integers(0, 2, n)
lemons = 3 * temp + 20 - 30 * rain + rng.normal(0, 8, n)
data = pd.DataFrame({"temp": temp, "rain": rain, "lemons": lemons})

# Split into input variables (X) and output variable (y)
X = data[["temp", "rain"]]
y = data["lemons"]

# Hold back 20% of the rows to test the model on unseen data
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Create and train the model; max_depth stops the tree growing forever
model = DecisionTreeRegressor(max_depth=3, random_state=42)
model.fit(X_train, y_train)

# Predict on the unseen test rows and measure accuracy
y_pred = model.predict(X_test)
print("R-squared:", round(r2_score(y_test, y_pred), 3))

# Predict for tomorrow: 27 degrees, raining
tomorrow = pd.DataFrame({"temp": [27], "rain": [1]})
print("Lemons for tomorrow:", round(model.predict(tomorrow)[0]))

# Draw the tree
plt.figure(figsize=(14, 6))
plot_tree(model, feature_names=["temp", "rain"], filled=True)
plt.savefig("decision_tree_basic.png", bbox_inches="tight")
