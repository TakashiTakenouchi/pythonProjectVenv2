import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import minimize_scalar

def profit(price_jacket, price_pants, discount_jacket, discount_pants):
    price_jacket_discounted = price_jacket * (1 - discount_jacket / 100)
    price_pants_discounted = price_pants * (1 - discount_pants / 100)

    sales_jacket = 25 * (1 + discount_jacket / 100)
    sales_pants = 50 * (1 + discount_pants / 100)

    return (price_jacket_discounted * sales_jacket + price_pants_discounted * sales_pants) - (25000 + 10000)

def optimal_price_and_discount(price_jacket, price_pants):
    def objective(discount_jacket):
        discount_pants = 10
        return -profit(price_jacket, price_pants, discount_jacket, discount_pants)

    res = minimize_scalar(objective, bounds=(0, 30), method='bounded')
    return res.x, 10

def simulate(price_jacket, price_pants, discount_jacket, discount_pants):
    jacket_sales = []
    pants_sales = []
    profit_values = []
    for i in range(3):
        if i == 0:
            jacket_sales.append(25 * (1 + discount_jacket / 100))
            pants_sales.append(50 * (1 + discount_pants / 100))
        else:
            jacket_sales.append(0)
            pants_sales.append(0)
        profit_values.append(profit(price_jacket, price_pants, discount_jacket, discount_pants))

    return jacket_sales, pants_sales, profit_values

def plot_results(price_jacket, price_pants, discount_jacket, discount_pants):
    jacket_sales, pants_sales, profit_values = simulate(price_jacket, price_pants, discount_jacket, discount_pants)

    fig, ax1 = plt.subplots()
    color = 'tab:red'
    ax1.set_xlabel('Month')
    ax1.set_ylabel('Jacket Sales', color=color)
    ax1.plot(np.arange(3) + 1, jacket_sales, color=color)
    ax1.tick_params(axis='y', labelcolor=color)
