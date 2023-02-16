"""
### いま、ジャケットとパンツに使える生地が200メートルある。色はネイビー。ジャケットに必要なのは2メートル。パンツに必要なのは1.5メートル。
### ジャケット製造に必要なコストは25000円。パンツ製造に必要なコストは10000円。この3か月の平均販売数量はジャケットが1か月で25着販売している。
### パンツは1っか月平均50本販売している。東京の気温が平均して20度を超えると、この記事でのジャケットおよびパンツは販売できない。
### 現在は2月13日だ。東京の平均気温は4度。3月で12度。4月で17度。5月で22度に達する。ジャケットの定価は55000円。パンツの定価は20000円。
### ジャケットは30％値引きすると、20％は販売数量が増加する。パンツは20％値引きしても１０％ほどしか販売数は増えない。
### 利益最大化と廃棄金額を最小化するにはジャケットとパンツをこれから何着製造して、いくらで販売すればよいかstreamlitおよびpulpを使用したPythonコードを生成
### ジャケットとパンツの販売予測グラフを可視化し、値引き率による増減をスライダーで調整可能にしてほしい。同時に、ジャケットとパンツの利益金額をグラフで可視化し、
### 値引き率による利益増減をスライダーで調整可能にしてほしい。最適化された価格に印をつけて表示

"""
import streamlit as st
from pulp import LpVariable, LpProblem, LpMaximize, LpMinimize, LpInteger
import matplotlib.pyplot as plt
import numpy as np

st.title("Profit Maximization and Waste Minimization")

# Define the inputs
cost_jacket = 25000
cost_pants = 10000
price_jacket = 55000
price_pants = 20000
jacket_discount = 30
pants_discount = 20
jacket_increase = 20
pants_increase = 10
jacket_demand = 25
pants_demand = 50
fabric_available = 200
jacket_required = 2
pants_required = 1.5
temperature_data = [4, 12, 17, 22]

# Create the sliders for jacket and pants discount
jacket_discount_slider = st.slider("Jacket Discount Percentage", 0, 50, 30, jacket_discount)
pants_discount_slider = st.slider("Pants Discount Percentage", 0, 50,30, pants_discount)

# Update the jacket and pants discount
jacket_discount = jacket_discount_slider
pants_discount = pants_discount_slider

# Define the optimization problem
prob = LpProblem("Profit Maximization and Waste Minimization", LpMaximize)

# Define the decision variables
jacket_production = LpVariable("jacket_production", 0, None, LpInteger)
pants_production = LpVariable("pants_production", 0, None, LpInteger)
waste = LpVariable("waste", 0, None, "Continuous")

# Define the objective function
prob += (price_jacket * (1 - jacket_discount / 100) * (1 + jacket_increase / 100) * jacket_production +
         price_pants * (1 - pants_discount / 100) * (1 + pants_increase / 100) * pants_production -
         cost_jacket * jacket_production - cost_pants * pants_production - waste, "Objective")

# Define the constraints
prob += jacket_production * jacket_required + pants_production * pants_required <= fabric_available - waste
prob += jacket_production <= jacket_demand
prob += pants_production <= pants_demand

# Solve the optimization problem
prob.solve()

# Calculate the profit
profit = price_jacket * (1 - jacket_discount / 100) * (1 + jacket_increase / 100) * jacket_production.value() + \
         price_pants * (1 - pants_discount / 100) * (1 + pants_increase / 100) * pants_production.value() - \
         cost_jacket * jacket_production.value() - cost_pants * pants_production.value() - waste.value()

# Plot the profit with the new jacket and pants discount
x = [jacket_discount, pants_discount]
y = [profit, profit]
# plt.plot(x, y, 'ro')
# plt.xlabel("Discount Percentage")
# plt.ylabel("Profit")
# st.pyplot()
fig, ax = plt.subplots()
ax.plot(x, y, 'ro')
ax.set_xlabel("Discount Percentage")
ax.set_ylabel("Profit")
st.pyplot(fig)

# Plot the sales quantity actual and prediction
x = np.array([0, 1, 2, 3])
y_actual = np.array([jacket_demand, pants_demand, jacket_demand, pants_demand])
y_predict = np.array([jacket_production.value(), pants_production.value(), jacket_production.value(), pants_production.value()])
fig, ax = plt.subplots()
ax.plot(x, y_actual, 'ro', label='Actual Sales Quantity')
ax.plot(x, y_predict, 'b--', label='Predicted Sales Quantity')
ax.legend()
ax.set_xlabel("Product")
ax.set_ylabel("Sales Quantity")
st.pyplot(fig)

# Print the results
st.write("Optimal Solution: $", prob.objective.value())
st.write("Jacket Production: ", int(jacket_production.value()))
st.write("Pants Production: ", int(pants_production.value()))
st.write("Waste: ", waste.value())

# jacket_demand = 25の時系列予測を実行

