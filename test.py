import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import psutil as ps
from sklearn.linear_model import LinearRegression

base_csv = pd.read_csv('salary.csv', skipinitialspace=True)

filled_csv = base_csv.dropna()

x = filled_csv[["workedYears"]]
y = filled_csv[["salaryBrutto"]]
LinReg = LinearRegression()
LinReg.fit(x, y)

predict_data = base_csv[["workedYears"]]
predicted_salary = pd.DataFrame(LinReg.predict(predict_data))
predicted_salary.columns = {"salaryBrutto"}
base_csv.salaryBrutto.fillna(predicted_salary.salaryBrutto, inplace=True)

print("Table of dependence between salary brutto and worked years supplemented by predictions for missing data")
print(base_csv)

plt.scatter(x, y, color='black')
plt.plot(predict_data, predicted_salary, color='blue', linewidth=3)

plt.title("Comparison of existing data to predictions obtained by linear regression.")
plt.xlabel("workedYears")
plt.ylabel("salaryBrutto")

plt.show()
