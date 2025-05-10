from sklearn.linear_model import LogisticRegression as SklearnLogisticRegression
import numpy as np
import pandas as pd
from sklearn.metrics import accuracy_score
from imblearn.over_sampling import SMOTE


class LogisticRegressionIRLS:
    def __init__(self, n_iterations=10000, tol=1e-6):
        self.n_iter = n_iterations
        self.tol = tol
        self.weights = None
        self.bias = None

    def sigmoid(self, z):
        return 1 / (1 + np.exp(-z))

    def fit(self, X, y):
        n_samples, n_features = X.shape
        self.weights = np.zeros(n_features)
        self.bias = 0
        X = np.hstack([np.ones((X.shape[0], 1)), X])
        self.weights = np.zeros(X.shape[1])  # bias is now included in weights
        for _ in range(self.n_iter):
            linear_model = np.dot(X, self.weights) + self.bias
            y_pred = self.sigmoid(linear_model)

            # calculate the diagonal elements of matrix R
            r = y_pred * (1 - y_pred)

            # it is impractical to make the R diagonal matrix due to space constraints (it will require 151 Gb of RAM!)
            # that is why we just compute R * X (which is just a scaling of diagonal elements of X by the entries in r vector)
            RX = X * r[:, np.newaxis]  # compute RX

            gradient = np.dot(X.T, (y_pred - y))
            hessian = X.T @ RX  # X.T * R * X

            # the update equation is : parameter_list -= (hessian ^ (-1)) * gradient
            # therefore: update_value = (hessian ^ (-1)) * gradient
            # also can be written as : hessian * update_value = gradient
            # this can be efficiently solved for using row reduction (np.linalg.solve)

            delta = np.linalg.solve(hessian, gradient)

            self.weights -= delta

            # If the change is very small, stop early (convergence)
            if np.linalg.norm(delta) < self.tol:
                print(f"Converged after {_+1} iterations")
                break

    def predict(self, X):
        X = np.hstack([np.ones((X.shape[0], 1)), X])
        linear_model = np.dot(X, self.weights)
        y_pred = self.sigmoid(linear_model)
        y_pred = np.clip(y_pred, 1e-8, 1 - 1e-8)
        return (y_pred >= 0.5).astype(int)


def accuracy_score(y_true, y_pred):
    correct = np.sum(y_true == y_pred)
    return correct / len(y_true)


def precision_score(y_true, y_pred):
    true_positives = np.sum((y_pred == 1) & (y_true == 1))
    predicted_positives = np.sum(y_pred == 1)
    if predicted_positives == 0:
        return 0.0
    return true_positives / predicted_positives


def standardiseData():
    global X_train, X_test
    means = np.mean(X_train, axis=0)
    stds = np.std(X_train, axis=0)
    stds[stds == 0] = 1
    X_train = (X_train - means) / stds
    X_test = (X_test - means) / stds


def recall_performance(pred_values, target_values):
    if (len(pred_values) != len(target_values)):
        return -1
    target_positives = 0
    pred_positives = 0
    for i in range(len(target_values)):
        if (target_values[i]):
            target_positives += 1
            if (pred_values[i]):
                pred_positives += 1
    return pred_positives/target_positives


training_data = pd.read_csv("training.csv")
X_train = training_data.iloc[:, :-1].values  # Feature Matrix
y_train = training_data.iloc[:, -1].values  # Target values for labels
testing_data = pd.read_csv("testing.csv")
X_test = testing_data.iloc[:, :-1].values  # Feature matrix
y_test = testing_data.iloc[:, -1].values  # True values of labels
smote = SMOTE(random_state=42)
X_train, y_train = smote.fit_resample(X_train, y_train)
standardiseData()

custom_model_irls = LogisticRegressionIRLS(n_iterations=1000)
custom_model_irls.fit(X_train, y_train)
custom_preds_irls = custom_model_irls.predict(X_test)
custom_acc_irls = accuracy_score(y_test, custom_preds_irls)
custom_prec_irls = precision_score(y_test, custom_preds_irls)
print(f"Custom Logistic Regression (IRLS) Accuracy: {custom_acc_irls:.5f}")
print(f"Custom Logistic Regression (IRLS) Precision: {custom_prec_irls:.5f}")
print(f"Custom Logistic Regression (IRLS) Recall performance: {
      recall_performance(custom_preds_irls, y_test)}")

sklearn_model = SklearnLogisticRegression()
sklearn_model.fit(X_train, y_train)
sklearn_preds = sklearn_model.predict(X_test)
sklearn_acc = accuracy_score(y_test, sklearn_preds)
sklearn_prec = precision_score(y_test, sklearn_preds)
print(f"Sklearn Logistic Regression Accuracy: {sklearn_acc:.5f}")
print(f"Sklearn Logistic Regression Precision: {sklearn_prec:.5f}")
print(f"Sklearn Logistic Regression Recall performance: {
      recall_performance(sklearn_preds, y_test)}")
