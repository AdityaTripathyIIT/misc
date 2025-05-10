import pandas as pd

dataset = pd.read_csv("creditcard.csv")
mid_index = len(dataset)//2

training_data = dataset.iloc[:mid_index]
testing_data = dataset.iloc[mid_index:]

training_data.to_csv("training.csv", index=False)
testing_data.to_csv("testing.csv", index=False)
