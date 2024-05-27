# Import necessary libraries
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

df = pd.read_csv('MDS.csv')
# Data Preprocessing
X = df[['Litres', 'Lt.fat', 'Lt.snf']]
y_fat = df['Fat']
y_snf = df['Snf']

# Split the data into training and testing sets
X_train, X_test, y_fat_train, y_fat_test, y_snf_train, y_snf_test = train_test_split(X, y_fat, y_snf, test_size=0.2, random_state=42)

# Train Decision Tree Regressor for Fat
fat_model = DecisionTreeRegressor()
fat_model.fit(X_train, y_fat_train)

# Predict Fat for the next 10 days
fat_predictions = fat_model.predict(X_test)

# Evaluate Fat model using Mean Squared Error
fat_mse = mean_squared_error(y_fat_test, fat_predictions)

# Print Fat model MSE
print(f"Fat Model Mean Squared Error: {fat_mse}")

# Train Decision Tree Regressor for SNF
snf_model = DecisionTreeRegressor()
snf_model.fit(X_train, y_snf_train)

# Predict SNF for the next 10 days
snf_predictions = snf_model.predict(X_test)

# Evaluate SNF model using Mean Squared Error
snf_mse = mean_squared_error(y_snf_test, snf_predictions)

# Print SNF model MSE
print(f"SNF Model Mean Squared Error: {snf_mse}")

# Predict Fat and SNF for the next 10 days using the trained models
future_data = {
    'Litres': [2200, 2185, 2150, 2100, 2050, 2000, 1980, 2025, 2075, 2125],  # Example future litres values
    'Lt.fat': [94.5, 92.8, 91.2, 89.6, 88.3, 86.7, 85.1, 86.5, 88.2, 90.0],  # Example future Lt.fat values
    'Lt.snf': [172.5, 170.8, 169.2, 167.6, 166.3, 164.7, 163.1, 163.8, 165.2, 166.7]  # Example future Lt.snf values
}

# Create a DataFrame with the future data and use an index
future_df = pd.DataFrame(future_data, index=range(len(future_data['Litres'])))

# Predict Fat and SNF for the next 10 days using the trained models
future_fat_predictions = fat_model.predict(future_df)
future_snf_predictions = snf_model.predict(future_df)

# Print predicted Fat and SNF for the next 10 days
print("Predicted Fat for Next 10 Days:", future_fat_predictions)
print("Predicted SNF for Next 10 Days:", future_snf_predictions)

# Line Chart for Daily Milk Production
plt.figure(figsize=(10, 6))
sns.lineplot(x='Date', y='Litres', data=df)
plt.title('Daily Milk Production Over Time')
plt.xlabel('Date')
plt.ylabel('Litres')
plt.xticks(rotation=45)
plt.show()

# Scatter Plot for Fat and SNF Relationship
plt.figure(figsize=(8, 6))
sns.scatterplot(x='Fat', y='Snf', data=df)
plt.title('Scatter Plot: Fat vs. SNF Relationship')
plt.xlabel('Fat Content')
plt.ylabel('SNF Content')
plt.show()

# Bar Chart for Mean Fat and SNF Content
mean_values = df[['Fat', 'Snf']].mean()
plt.figure(figsize=(8, 6))
mean_values.plot(kind='bar', color=['blue', 'orange'])
plt.title('Mean Fat and SNF Content Over Time')
plt.ylabel('Mean Value')
plt.show()

# Time Series Plot for Predicted Fat and SNF
plt.figure(figsize=(10, 6))
plt.plot(range(len(future_df)), future_fat_predictions, label='Predicted Fat')
plt.plot(range(len(future_df)), future_snf_predictions, label='Predicted SNF')
plt.title('Time Series Plot: Predicted Fat and SNF for Next 10 Days')
plt.xlabel('Index')
plt.ylabel('Predicted Value')
plt.legend()
plt.show()

predicted_litres = [2200, 2185, 2150, 2100, 2050, 2000, 1980, 2025, 2075, 2125]
predicted_lt_fat = [94.5, 92.8, 91.2, 89.6, 88.3, 86.7, 85.1, 86.5, 88.2, 90.0]
predicted_lt_snf = [172.5, 170.8, 169.2, 167.6, 166.3, 164.7, 163.1, 163.8, 165.2, 166.7]

# Generate an array for the x-axis (days)
days = np.arange(1, len(predicted_litres) + 1)

# Bar chart for predicted Litres
plt.figure(figsize=(10, 6))
plt.bar(days, predicted_litres, color='blue', label='Predicted Litres')
plt.title('Predicted Litres for Next 10 Days')
plt.xlabel('Day')
plt.ylabel('Predicted Litres')
plt.xticks(days)
plt.legend()
plt.show()