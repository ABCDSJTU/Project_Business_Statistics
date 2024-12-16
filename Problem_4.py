import pandas as pd
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.formula.api import ols

# Set matplotlib to use TkAgg for the backend
import matplotlib
matplotlib.use('TkAgg')

# File paths for the data
file_path_day = 'day.csv'
file_path_hour = 'hour.csv'

# Read data
data = pd.read_csv(file_path_day)

def solve_problem():
    # Display summary statistics for selected columns
    print(data[['atemp', 'hum', 'windspeed', 'cnt']].describe())

    # Plot distributions for selected variables
    fig, axes = plt.subplots(1, 3, figsize=(18, 5), dpi=300)
    sns.histplot(data['atemp'], kde=True, ax=axes[0], bins=50, color='skyblue')
    axes[0].set_title('Distribution of atemp')
    sns.histplot(data['hum'], kde=True, ax=axes[1], bins=50, color='lightgreen')
    axes[1].set_title('Distribution of hum')
    sns.histplot(data['windspeed'], kde=True, ax=axes[2], bins=50, color='salmon')
    axes[2].set_title('Distribution of windspeed')
    plt.tight_layout()
    plt.show()

    # Plot distribution of the target variable 'cnt' (bike usage)
    plt.figure(figsize=(8, 6))
    sns.histplot(data['cnt'], kde=True, bins=30, color='skyblue')
    plt.title('Distribution of Bike Usage (cnt)')
    plt.xlabel('Bike Usage')
    plt.ylabel('Frequency')
    plt.show()

    # Scatter plot for the relationship between temperature ('temp') and bike usage ('cnt')
    plt.figure(figsize=(8, 6))
    sns.scatterplot(x='temp', y='cnt', data=data, color='darkorange')
    plt.title('Relationship between Temperature and Bike Usage')
    plt.xlabel('Temperature')
    plt.ylabel('Bike Usage')
    plt.show()

    # Function to plot quadratic fit and perform statistical analysis
    def plot_fit_and_data(temperature, bike_usage):
        # Create DataFrame and add squared term for quadratic fit
        df = pd.DataFrame({'temp': temperature, 'bike_usage': bike_usage})
        df['temp_squared'] = df['temp'] ** 2

        # Fit quadratic regression model
        model = ols('bike_usage ~ temp + temp_squared', data=df).fit()

        # Print the quadratic fit equation
        a = model.params['temp_squared']
        b = model.params['temp']
        c = model.params['Intercept']
        print(f"Fitted quadratic equation: y = {a:.2f}x^2 + {b:.2f}x + {c:.2f}")

        # Print the R-squared value
        r_squared = model.rsquared
        print(f"R-squared: {r_squared:.2f}")

        # Generate x-values for plotting the fitted curve
        x = np.linspace(min(temperature), max(temperature), 100)
        y_hat = a * x ** 2 + b * x + c

        # Plot the original data and the fitted quadratic curve
        plt.figure(figsize=(8, 6), dpi=300)
        plt.scatter(temperature, bike_usage, label='Observed Data', alpha=0.6)
        plt.plot(x, y_hat, 'r-', label='Fitted Curve', linewidth=2)
        plt.xlabel('Temperature')
        plt.ylabel('Bike Usage')
        plt.title('Quadratic Fit: Temperature vs Bike Usage')
        plt.legend()
        plt.show()

        # Perform F-test for the model's significance
        f_test_result = model.f_test("temp = 0, temp_squared = 0")
        print(f"F-test statistic: {f_test_result.fvalue:.2f}, p-value: {f_test_result.pvalue:.4f}")

        # Perform t-test for the quadratic term
        t_test_result = model.t_test("temp_squared = 0")
        print(f"T-test statistic for quadratic term: {t_test_result.tvalue[0][0]:.2f}, p-value: {t_test_result.pvalue:.4f}")

    # Perform quadratic fit analysis on 'temp' vs 'cnt'
    plot_fit_and_data(data['temp'], data['cnt'])

