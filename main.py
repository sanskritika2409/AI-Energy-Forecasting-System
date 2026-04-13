import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPRegressor
from sklearn.metrics import mean_absolute_error
import joblib

# Load dataset
data = pd.read_csv('data/energy.csv', parse_dates=['Datetime'], index_col='Datetime')

# Resample hourly
data = data.resample('h').mean()

# Fill missing values
data = data.ffill()

# Feature Engineering
data['hour'] = data.index.hour
data['day'] = data.index.dayofweek

# Prepare data
X = data[['hour', 'day']]
y = data['Energy']

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

# Model
model = MLPRegressor(hidden_layer_sizes=(64, 64), max_iter=500)
model.fit(X_train, y_train)

# Prediction
pred = model.predict(X_test)

# Evaluation
mae = mean_absolute_error(y_test, pred)
print("Mean Absolute Error:", mae)

# Save sample predictions
results = pd.DataFrame({
    "Actual": y_test.values[:50],
    "Predicted": pred[:50]
})

results.to_csv("outputs/sample_predictions.csv", index=False)
print("Saved sample_predictions.csv in outputs folder ✅")

# Save model
joblib.dump(model, 'models/energy_model.pkl')

# Plot
plt.plot(y_test.values, label="Actual")
plt.plot(pred, label="Predicted")
plt.legend()
plt.title("Actual vs Predicted Energy")
plt.savefig("outputs/result.png")
plt.show()

# Save graph instead of only showing
plt.figure(figsize=(10,5))
plt.plot(y_test.values[:100], label="Actual")
plt.plot(pred[:100], label="Predicted")
plt.legend()
plt.title("Actual vs Predicted Energy Consumption")

# Save image
plt.savefig("outputs/prediction_graph.png")

plt.show()