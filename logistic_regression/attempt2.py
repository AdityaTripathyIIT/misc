import numpy as np
import pandas as pd
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression as SklearnLogisticRegression
from sklearn.metrics import accuracy_score

# --------------------------
# Your Custom LogisticRegression
# --------------------------


class LogisticRegression:
    def __init__(self, learning_rate=0.01, n_iterations=1000):
        self.lr = learning_rate
        self.n_iter = n_iterations
        self.weights = None
        self.bias = None

    def sigmoid(self, z):
        return 1 / (1 + np.exp(-z))

    def fit(self, X, y):
        n_samples, n_features = X.shape
        self.weights = np.zeros(n_features)
        self.bias = 0

        for _ in range(self.n_iter):
            linear_model = np.dot(X, self.weights) + self.bias
            y_predicted = self.sigmoid(linear_model)

            dw = (1 / n_samples) * np.dot(X.T, (y_predicted - y))
            db = (1 / n_samples) * np.sum(y_predicted - y)

            self.weights -= self.lr * dw
            self.bias -= self.lr * db

    def predict(self, X):
        linear_model = np.dot(X, self.weights) + self.bias
        y_predicted = self.sigmoid(linear_model)
        return (y_predicted > 0.5).astype(int)


# --------------------------
# Dataset Preparation
# --------------------------
'''
X, y = make_classification(
    n_samples=1000, n_features=10, n_classes=2, random_state=42)
X = StandardScaler().fit_transform(X)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42)
'''

training_data = pd.read_csv("training.csv")
X_train = training_data.iloc[:, :-1].values
y_train = training_data.iloc[:, -1].values
testing_data = pd.read_csv("testing.csv")
X_test = testing_data.iloc[:, :-1].values
y_test = testing_data.iloc[:, -1].values
print(sum(y_train), sum(y_test))

# --------------------------
# Custom Logistic Regression
# --------------------------
custom_model = LogisticRegression(learning_rate=0.1, n_iterations=1000)
custom_model.fit(X_train, y_train)
custom_preds = custom_model.predict(X_test)
print(sum(custom_preds))
custom_acc = accuracy_score(y_test, custom_preds)
print(f"Custom Logistic Regression Accuracy: {custom_acc:.4f}")

# --------------------------
# Sklearn Logistic Regression
# --------------------------
sklearn_model = SklearnLogisticRegression()
sklearn_model.fit(X_train, y_train)
sklearn_preds = sklearn_model.predict(X_test)
sklearn_acc = accuracy_score(y_test, sklearn_preds)
print(f"Sklearn Logistic Regression Accuracy: {sklearn_acc:.4f}")
print(sum(sklearn_preds))

'''

testing_data = pd.read_csv("testing.csv")
X_test = testing_data.iloc[:, :-1].values
Y_test = testing_data.iloc[:, -1].values

model.fit(X_train, Y_train)
predictions = model.predict(X_test)
print(predictions)
'''
