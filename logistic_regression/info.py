import pandas as pd


orig_data = pd.read_csv("creditcard.csv")
training_data = pd.read_csv("training.csv")
testing_data = pd.read_csv("testing.csv")

print(f"original dataset length = {len(orig_data)}\n training dataset length = {
      len(training_data)}\n testing dataset length = {len(testing_data)}")
print(orig_data.info())
print(training_data.info())
print(testing_data.info())
