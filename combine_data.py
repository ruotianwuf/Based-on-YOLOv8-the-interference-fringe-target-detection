import pandas as pd
import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
from sklearn.metrics import r2_score

# Load the data
file_path = 'adjusted_output.csv'
data = pd.read_csv(file_path)

# Define the combined logarithmic and exponential function
def combined_func(x, a, b, c, d):
    return a * np.log(x) + b * np.exp(c * x) + d

# Extract the data for fitting
x_data = data['Temperature']
y_data = data['Stripe Change Count']

# Adjusting the initial guess to potentially improve convergence
adjusted_initial_guess = (0.1, 0.001, 0.01, 0.1)
popt_combined, pcov_combined = curve_fit(combined_func, x_data, y_data, p0=adjusted_initial_guess, maxfev=5000)

# Calculate the fitted values using the combined model
fitted_y_combined = combined_func(x_data, *popt_combined)

# Plot the original data and the combined fit
plt.figure(figsize=(10, 6))
plt.scatter(x_data, y_data, label='Original Data', color='blue')
plt.plot(x_data, fitted_y_combined, label='Combined Logarithmic & Exponential Fit', color='green')
plt.xlabel('Temperature (℃)')
plt.ylabel('Stripe Change Count (times)')
plt.xticks(np.arange(30, np.ceil(x_data.max()) + 1, 1))  # Set x-axis ticks starting from 30 with an interval of 1
plt.xlim(left=30)  # Start the x-axis from 30
plt.title('Combined Logarithmic & Exponential Fit of Stripe Change Count vs Temperature')
plt.legend()
plt.grid(True)
plt.show()

# Evaluate the fit
# Calculate residuals
residuals = y_data - fitted_y_combined
# Calculate R-squared
r_squared = r2_score(y_data, fitted_y_combined)

# Print the fitting parameters and evaluation metrics
print("Fitting Parameters: a = {}, b = {}, c = {}, d = {}".format(*popt_combined))
print(f"R-squared: {r_squared}")
