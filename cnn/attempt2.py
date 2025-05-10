import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader
from torchvision import transforms, models
from PIL import Image
import pandas as pd
import os
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from tqdm import tqdm

# === Load CSV and split ===
labeled_data = pd.read_csv("train.csv")
training_df, validation_df = train_test_split(
    labeled_data, test_size=0.25, stratify=labeled_data['Class'], random_state=123
)

# === Dataset ===
class CoinDataset(Dataset):
    def __init__(self, data, image_dir, transform):
        self.data = data.reset_index(drop=True)
        self.image_dir = image_dir
        self.transform = transform
        self.coin_classes = sorted(self.data['Class'].unique())
        self.assigned_class_index = {
            coin_class: i for i, coin_class in enumerate(self.coin_classes)}
        self.index_to_label = {i: coin_class for coin_class,
                               i in self.assigned_class_index.items()}

    def __len__(self):
        return len(self.data)

    def __getitem__(self, index):
        image_id = self.data.loc[index, 'Id']
        image_path = os.path.join(self.image_dir, f"{image_id}.jpg")
        image = Image.open(image_path).convert('RGB')
        label = self.assigned_class_index[self.data.loc[index, 'Class']]
        return self.transform(image), label

# === Transforms ===
transform = transforms.Compose([
    transforms.Resize((256, 256)),
    transforms.RandomResizedCrop(224, scale=(0.8, 1.0)),
    transforms.RandomHorizontalFlip(),
    transforms.RandomRotation(15),
    transforms.ColorJitter(brightness=0.3, contrast=0.3, saturation=0.3),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406],
                         std=[0.229, 0.224, 0.225])
])

# === Loaders ===
training_data = CoinDataset(training_df, 'train', transform)
validation_data = CoinDataset(validation_df, 'train', transform)
train_loader = DataLoader(training_data, batch_size=50, shuffle=True)
validation_loader = DataLoader(validation_data, batch_size=50, shuffle=False)

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# === Model Definition ===
class ResNetWithCustomHead(nn.Module):
    def __init__(self, num_classes, hidden_layers=[512, 256], dropout=0.4):
        super().__init__()
        self.base_model = models.resnet18(pretrained=True)
        for param in self.base_model.parameters():
            param.requires_grad = False

        in_features = self.base_model.fc.in_features
        layers = []
        prev = in_features
        for h in hidden_layers:
            layers.append(nn.Linear(prev, h))
            layers.append(nn.ReLU())
            layers.append(nn.Dropout(dropout))
            prev = h
        layers.append(nn.Linear(prev, num_classes))
        self.base_model.fc = nn.Sequential(*layers)

    def forward(self, x):
        return self.base_model(x)

def unfreeze_backbone(model, trainable_layers=2):
    ct = 0
    for child in reversed(list(model.base_model.children())):
        for param in child.parameters():
            param.requires_grad = True
        ct += 1
        if ct >= trainable_layers:
            break

# === Hyperparameters ===
dropout_rate = 0.4
hidden_layers = [512, 256]
learning_rate = 1e-4
weight_decay = 1e-4  # L2 Regularization

model = ResNetWithCustomHead(
    num_classes=len(training_data.coin_classes),
    hidden_layers=hidden_layers,
    dropout=dropout_rate
).to(device)

criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=learning_rate, weight_decay=weight_decay)
scheduler = optim.lr_scheduler.StepLR(optimizer, step_size=3, gamma=0.5)

# === Training Function ===
def train_model(model, train_loader, val_loader, epochs=10):
    for epoch in range(epochs):
        if epoch == 3:
            print("\n🔓 Unfreezing backbone...")
            unfreeze_backbone(model)

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

            _, preds = outputs.max(1)
            correct += (preds == labels).sum().item()
            total += labels.size(0)

        scheduler.step()

        train_acc = correct / total
        print(f"Training Accuracy: {train_acc:.4f}")
        evaluate(model, val_loader)

# === Evaluation Function ===
def evaluate(model, val_loader):
    model.eval()
    y_true, y_pred = [], []
    with torch.no_grad():
        for images, labels in val_loader:
            images, labels = images.to(device), labels.to(device)
            outputs = model(images)
            _, preds = outputs.max(1)
            y_true.extend(labels.cpu().numpy())
            y_pred.extend(preds.cpu().numpy())

    acc = sum([yt == yp for yt, yp in zip(y_true, y_pred)]) / len(y_true)
    print(f"Validation Accuracy: {acc:.4f}")
    print(classification_report(y_true, y_pred, target_names=validation_data.coin_classes))

# === Train or Load Model ===
train_model(model, train_loader, validation_loader, epochs=10)
torch.save(model.state_dict(), "model_weights_att.pth")

# === Test Prediction ===
test_transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406],
                         std=[0.229, 0.224, 0.225])
])

model.eval()
test_preds = []
test_filenames = sorted(os.listdir('test'))

for filename in test_filenames:
    img_path = os.path.join('test', filename)
    image = Image.open(img_path).convert("RGB")
    image = test_transform(image).unsqueeze(0).to(device)

    with torch.no_grad():
        output = model(image)
        pred = output.argmax(1).item()
        label = training_data.index_to_label[pred]
        test_preds.append((filename[:-4], label))

# === Save Predictions ===
submission = pd.DataFrame(test_preds, columns=['id', 'label'])
submission.to_csv("submission_att.csv", index=False)

