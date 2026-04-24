import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

np.random.seed(0)

data = pd.DataFrame({
    "Gender": ["Male", "Female", "Female", "Male", "Male", "Female"],
    "Age": [22, 25, 30, 28, 35, 27],
    "AdType": ["Video", "Banner", "Video", "Popup", "Banner", "Video"],
    "TimeSpent": [5, 3, 6, 4, 2, 7],
    "ClickRate": [80, 45, 120, 60, 30, 150]
})

print("Data set Preview:\n")
print(data)


data['Clicked'] = data["clickRate"].apply(lambda x: 1 if x > 70 else 0)

dataEncoded = pd.get_dummies(data, drop_first=True)

print("\n Statistical Summary :\n")
print(data.describe())


