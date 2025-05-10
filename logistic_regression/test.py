from sklearn.linear_model import LogisticRegression as SklearnLogisticRegression
from sklearn.metrics import accuracy_score
from imblearn.over_sampling import SMOTE
import numpy as np
import pandas as pd


class LogisticRegressionIRLS:
    def __init__(self, n_iterations=10000, tol=1e-6):
        self.n_iter = n_iterations
        self.tol = tol
        self.weights = None

    def sigmoid(self, z):
        return 1 / (1 + np.exp(-z))

    def fit(self, X, y):
        X = np.hstack([np.ones((X.shape[0], 1)), X])
        self.weights = np.zeros(X.shape[1])
        for _ in range(self.n_iter):
            linear_model = np.dot(X, self.weights)
            y_pred = self.sigmoid(linear_model)
            r = y_pred * (1 - y_pred)
            RX = X * r[:, np.newaxis]
            gradient = np.dot(X.T, (y_pred - y))
            hessian = X.T @ RX
            delta = np.linalg.solve(hessian, gradient)
            self.weights -= delta
            if np.linalg.norm(delta) < self.tol:
                print(f"Converged after {_+1} iterations")
                break
        lambda_reg = 1.0  # You can tune this
        hessian += lambda_reg * np.identity(X.shape[1])
        gradient += lambda_reg * self.weights

    def predict(self, X, threshold=0.5):
        X = np.hstack([np.ones((X.shape[0], 1)), X])
        y_pred = self.sigmoid(np.dot(X, self.weights))
        y_pred = np.clip(y_pred, 1e-8, 1 - 1e-8)
        return (y_pred >= threshold).astype(int)


def standardiseData():
    global X_train, X_test
    means = np.mean(X_train, axis=0)
    stds = np.std(X_train, axis=0)
    stds[stds == 0] = 1  # avoid division by zero
    X_train = (X_train - means) / stds
    X_test = (X_test - means) / stds


def recall_performance(pred_values, target_values):
    if len(pred_values) != len(target_values):
        return -1
    target_positives = 0
    pred_positives = 0
    for i in range(len(target_values)):
        if target_values[i]:
            target_positives += 1
            if pred_values[i]:
                pred_positives += 1
    return pred_positives / target_positives


# --- Load data ---
training_data = pd.read_csv("training.csv")
X_train = training_data.iloc[:, :-1].values
y_train = training_data.iloc[:, -1].values
testing_data = pd.read_csv("testing.csv")
X_test = testing_data.iloc[:, :-1].values
y_test = testing_data.iloc[:, -1].values

# --- Apply SMOTE to balance the training data ---
smote = SMOTE(random_state=42)
X_train, y_train = smote.fit_resample(X_train, y_train)

# --- Standardize the data after resampling ---
standardiseData()

# --- Train and evaluate Custom IRLS model ---
custom_model = LogisticRegressionIRLS()
custom_model.fit(X_train, y_train)
custom_preds = custom_model.predict(X_test)
custom_acc = accuracy_score(y_test, custom_preds)
custom_recall = recall_performance(custom_preds, y_test)
print(f"Custom Logistic Regression (IRLS) Accuracy: {custom_acc:.4f}")
print(f"Custom Logistic Regression (IRLS) Recall: {custom_recall:.4f}")

# --- Train and evaluate Sklearn Logistic Regression ---
sklearn_model = SklearnLogisticRegression()
sklearn_model.fit(X_train, y_train)
sklearn_preds = sklearn_model.predict(X_test)
sklearn_acc = accuracy_score(y_test, sklearn_preds)
sklearn_recall = recall_performance(sklearn_preds, y_test)
print(f"Sklearn Logistic Regression Accuracy: {sklearn_acc:.4f}")
print(f"Sklearn Logistic Regression Recall: {sklearn_recall:.4f}")
