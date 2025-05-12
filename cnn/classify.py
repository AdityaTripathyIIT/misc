import torch
from torch.utils.data import Dataset, DataLoader
from sklearn.model_selection import train_test_split
import pandas as pd
import os
from PIL import Image
from torchvision import transforms, models
import torch.nn as nn
import torch.optim as optim
from sklearn.metrics import accuracy_score, confusion_matrix, ConfusionMatrixDisplay
import matplotlib.pyplot as plt
from tqdm import tqdm
import numpy as np

# Load CSV
labeled_data = pd.read_csv("train.csv")

# Split into training and validation sets
training_df, validation_df = train_test_split(
    labeled_data, test_size=0.25, stratify=labeled_data["Class"], random_state=123
)


class CoinDataset(Dataset):
    def __init__(self, data, image_dir, transform):
        self.data = data.reset_index(drop=True)
        self.image_dir = image_dir
        self.transform = transform
        self.coin_classes = sorted(self.data["Class"].unique())
        self.assigned_class_index = {
            coin_class: i for i, coin_class in enumerate(self.coin_classes)
        }
        self.index_to_label = {
            i: coin_class for coin_class, i in self.assigned_class_index.items()
        }

    def __len__(self):
        return len(self.data)

    def __getitem__(self, index):
        image_id = self.data.loc[index, "Id"]
        image_path = f"train/{image_id}.jpg"
        image = Image.open(image_path).convert("RGB")
        label = self.assigned_class_index[self.data.loc[index, "Class"]]
        return self.transform(image), label


# Transforms with augmentation
transform = transforms.Compose(
    [
        transforms.Resize((224, 224)),
        transforms.RandomHorizontalFlip(),
        transforms.RandomVerticalFlip(),
        transforms.RandomAffine(degrees=0, translate=(0.1, 0.1)),
        transforms.ColorJitter(brightness=0.2, contrast=0.2),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
    ]
)

# Dataset and Dataloader setup
training_data = CoinDataset(training_df, "train", transform)
validation_data = CoinDataset(validation_df, "train", transform)

train_loader = DataLoader(training_data, batch_size=50, shuffle=True)
validation_loader = DataLoader(validation_data, batch_size=50, shuffle=False)

device = torch.device("cpu")  # or torch.device("cuda") if GPU is available

# Load pretrained ResNet18 and adjust final layer
model = models.resnet18(pretrained=True)
model.fc = nn.Linear(model.fc.in_features, len(training_data.coin_classes))
model = model.to(device)

# Loss and optimizer
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=1e-4)


# Evaluation function
def evaluate(model, val_loader):
    correct_pred = {classname: 0 for classname in val_loader.dataset.coin_classes}
    total_pred = {classname: 0 for classname in val_loader.dataset.coin_classes}

    model.eval()
    y_true, y_pred = [], []
    running_loss = 0.0
    total = 0

    with torch.no_grad():
        for images, labels in val_loader:
            images, labels = images.to(device), labels.to(device)
            outputs = model(images)
            _, preds = outputs.max(1)
            loss = criterion(outputs, labels)

            y_true.extend(labels.cpu().numpy())
            y_pred.extend(preds.cpu().numpy())

            running_loss += loss.item() * images.size(0)
            total += labels.size(0)

            for label, prediction in zip(labels, preds):
                classname = val_loader.dataset.coin_classes[label]
                if label == prediction:
                    correct_pred[classname] += 1
                total_pred[classname] += 1

    accuracy_per_class = {
        classname: (
            correct_pred[classname] / total_pred[classname]
            if total_pred[classname] > 0
            else 0
        )
        for classname in val_loader.dataset.coin_classes
    }

    overall_accuracy = accuracy_score(y_true, y_pred)

    print("Accuracy per class:")
    for classname, accuracy in accuracy_per_class.items():
        print(f"{classname}: {accuracy:.4f}")
    print(f"Overall Accuracy: {overall_accuracy:.4f}")

    val_loss = running_loss / total
    val_acc = sum([yt == yp for yt, yp in zip(y_true, y_pred)]) / total

    return val_loss, val_acc


# Training function
def train_model(model, train_loader, val_loader, epochs=10):
    training_accuracies = np.zeros(epochs)
    validation_accuracies = np.zeros(epochs)
    training_losses = np.zeros(epochs)
    validation_losses = np.zeros(epochs)

    for epoch in range(epochs):
        model.train()
        running_loss = 0
        correct = 0
        total = 0

        for images, labels in tqdm(train_loader, desc=f"Epoch {epoch+1}/{epochs}"):
            images, labels = images.to(device), labels.to(device)
            optimizer.zero_grad()
            outputs = model(images)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()

            running_loss += loss.item() * images.size(0)
            _, preds = outputs.max(1)
            correct += (preds == labels).sum().item()
            total += labels.size(0)

        train_loss = running_loss / total
        train_acc = correct / total
        val_loss, val_acc = evaluate(model, val_loader)

        training_accuracies[epoch] = train_acc
        validation_accuracies[epoch] = val_acc
        training_losses[epoch] = train_loss
        validation_losses[epoch] = val_loss

        print(
            f"Epoch {epoch+1}: Train Acc={train_acc:.4f}, Train Loss={train_loss:.4f}, Val Acc={val_acc:.4f}, Val Loss={val_loss:.4f}"
        )

    return (
        training_accuracies,
        training_losses,
        validation_accuracies,
        validation_losses,
    )


# Train
epochs = 10
training_accuracies, training_losses, validation_accuracies, validation_losses = (
    train_model(model, train_loader, validation_loader, epochs)
)

# Plot metrics
x_range = np.arange(1, epochs + 1)

fig, axs = plt.subplots(2, 2, figsize=(10, 8))
axs[0, 0].plot(x_range, training_accuracies)
axs[0, 0].set_title("Training Accuracy vs. Epoch")

axs[0, 1].plot(x_range, training_losses)
axs[0, 1].set_title("Training Loss vs. Epoch")

axs[1, 0].plot(x_range, validation_accuracies)
axs[1, 0].set_title("Validation Accuracy vs. Epoch")

axs[1, 1].plot(x_range, validation_losses)
axs[1, 1].set_title("Validation Loss vs. Epoch")

plt.tight_layout()
plt.show()

# Confusion Matrix (overall)
model.eval()
y_true, y_pred = [], []
with torch.no_grad():
    for images, labels in validation_loader:
        images, labels = images.to(device), labels.to(device)
        outputs = model(images)
        preds = outputs.argmax(1)
        y_true.extend(labels.cpu().numpy())
        y_pred.extend(preds.cpu().numpy())

cm = confusion_matrix(y_true, y_pred)
disp = ConfusionMatrixDisplay(confusion_matrix=cm)
disp.plot(cmap=plt.cm.Blues)
plt.title("Overall Confusion Matrix")
plt.show()

# TP, FP, FN, TN (overall)
TP = np.diag(cm).sum()
FP = cm.sum(axis=0) - np.diag(cm)
FN = cm.sum(axis=1) - np.diag(cm)
TN = cm.sum() - (FP + FN + np.diag(cm))

print(f"TP: {TP}, FP: {FP.sum()}, FN: {FN.sum()}, TN: {TN.sum()}")

# Test prediction
test_transform = transforms.Compose(
    [
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
    ]
)

model.eval()
test_preds = []
test_filenames = sorted(os.listdir("test"))

for filename in test_filenames:
    img_path = os.path.join("test", filename)
    image = Image.open(img_path).convert("RGB")
    image = test_transform(image).unsqueeze(0).to(device)

    with torch.no_grad():
        output = model(image)
        pred = output.argmax(1).item()
        label = training_data.index_to_label[pred]
        test_preds.append((filename[:-4], label))

submission = pd.DataFrame(test_preds, columns=["id", "label"])
submission.to_csv("submission.csv", index=False)

torch.save(model.state_dict(), "model_weights.pth")
