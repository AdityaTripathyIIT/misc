'''
import pandas as pd
import numpy as np

learning_rate = 1e-3
max_iters = int(1e4)
tolerance = 1e-6

training_data = pd.read_csv("training.csv")
X = training_data.iloc[:, :-1].values
y = training_data.iloc[:, -1].values
X = np.hstack([np.ones((X.shape[0], 1)), X])  # Add bias term
parameter_list = np.zeros(X.shape[1])  # Initialize weights

test_data = pd.read_csv("testing.csv")
X_t = test_data.iloc[:, :-1].values
y_t = test_data.iloc[:, -1].values
X_t = np.hstack([np.ones((X_t.shape[0], 1)), X_t])  # Add bias term


def sigmoid(x):
    return 1 / (1 + np.exp(-x))


def gradient():
    y_pred = sigmoid(np.dot(X, parameter_list))
    return np.dot(X.T, (y_pred - y)) / X.shape[0]


def get_learned_parameters():
    global parameter_list
    for i in range(max_iters):
        grad = gradient()
        step = grad * learning_rate
        if np.linalg.norm(step) <= tolerance:
            print(f"Converged at iteration {i}")
            break
        parameter_list -= step
        print(parameter_list.T)
    return parameter_list


def predict():
    y_pred = (sigmoid(np.dot(X_t, parameter_list)) >= 0.5).astype(int)
    true_pos = np.sum((y_t == 1) & (y_pred == 1))
    actual_pos = np.sum(y_t == 1)

    recall = true_pos / actual_pos if actual_pos > 0 else 0
    print(f"Number of predicted 1s : {np.sum(y_pred)}")
    print(f"Recall Accuracy : {recall}")


if __name__ == "__main__":
    params = get_learned_parameters()
    print("Learned parameters:\n", params)
    predict()

'''

import numpy as np
import pandas as pd

# Hyperparameters
learning_rate = 0.001
max_iters = 10000
tolerance = 1e-6

# Load data
train = pd.read_csv("training.csv")
test = pd.read_csv("testing.csv")

# Extract features and labels
X_train = train.iloc[:, :-1].to_numpy()
t_train = train.iloc[:, -1].to_numpy()
X_test = test.iloc[:, :-1].to_numpy()
t_test = test.iloc[:, -1].to_numpy()

# Add bias term (prepend column of 1s)


def add_bias(X):
    return np.hstack([np.ones((X.shape[0], 1)), X])


X_train = add_bias(X_train)
X_test = add_bias(X_test)

# Initialize weights
w = np.zeros(X_train.shape[1])

# Sigmoid function


def sigmoid(a):
    return 1 / (1 + np.exp(-a))

# Compute gradient based on Bishop Eq. 4.91


def compute_gradient(X, t, w):
    y = sigmoid(np.dot(X, w))
    grad = np.dot(X.T, (y - t)) / X.shape[0]
    return grad

# Gradient descent training


def train_model():
    global w
    for _ in range(max_iters):
        grad = compute_gradient(X_train, t_train, w)
        update = learning_rate * grad

        if np.linalg.norm(update) < tolerance:
            break

        w -= update
    return w

# Predict class labels


def predict(X, w):
    probs = sigmoid(np.dot(X, w))
    return (probs > 0.5).astype(int)

# Evaluation (Recall)


def evaluate():
    y_pred = predict(X_test, w)
    true_positives = np.sum((y_pred == 1) & (t_test == 1))
    actual_positives = np.sum(t_test == 1)
    recall = true_positives / actual_positives if actual_positives > 0 else 0.0
    print("Recall Accuracy:", recall)


# Run training and evaluation
if __name__ == "__main__":
    final_weights = train_model()
    print("Learned parameters:", final_weights)
    evaluate()
