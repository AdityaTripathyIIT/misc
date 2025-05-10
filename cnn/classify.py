import torch
from torch.utils.data import Dataset, DataLoader
from sklearn.model_selection import train_test_split
import pandas as pd
import os
from PIL import Image
from torchvision import transforms, models
import torch.nn as nn
import torch.optim as optim
from sklearn.metrics import accuracy_score, precision_recall_fscore_support
import matplotlib.pyplot as plt
import seaborn as sns
from tqdm import tqdm

# Load CSV
labeled_data = pd.read_csv("train.csv")

# Split into training and validation sets
training_df, validation_df = train_test_split(
    labeled_data, test_size=0.25,
    stratify=labeled_data['Class'], random_state=123
)

'''
Since we are using a custom dataset to train our resnet model, we need to create a Dataset class as prescribed
in the pytorch documentation : https://docs.pytorch.org/tutorials/beginner/basics/data_tutorial.html#creating-a-custom-dataset-for-your-files
'''
class CoinDataset(Dataset):                                     # The CoinDataset is inheriting from the Dataset class in pytorch library
    def __init__(self, data, image_dir, transform):
        self.data = data.reset_index(drop=True)
        self.image_dir = image_dir
        self.transform = transform
        self.coin_classes = sorted(self.data['Class'].unique())
        '''
        Working with numbers is easier than with strings. 
        So we will assign a numerical index to each (unique) coin class.
        '''
        self.assigned_class_index = {
            coin_class: i for i, coin_class in enumerate(self.coin_classes)}
        self.index_to_label = {i: coin_class for coin_class,
                               i in self.assigned_class_index.items()}

    def __len__(self):
        return len(self.data)

    def __getitem__(self, index):
        image_id = self.data.loc[index, 'Id']
        image_path = f"train/{image_id}.jpg"
        image = Image.open(image_path).convert('RGB')
        label = self.assigned_class_index[self.data.loc[index, 'Class']]
        return self.transform(image), label

'''
We will apply data augmentation (transforms) to tackle overfitting and non-idealites
of real-world images of coin.
'''

transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.RandomHorizontalFlip(),
    transforms.RandomVerticalFlip(),
    transforms.RandomAffine(degrees=0, translate=(0.1, 0.1)),
    transforms.ColorJitter(brightness=0.2, contrast=0.2),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406],
                     std=[0.229, 0.224, 0.225])
])

# Datasets and DataLoaders
training_data = CoinDataset(training_df, 'train', transform)
validation_data = CoinDataset(validation_df, 'train', transform)

train_loader = DataLoader(training_data, batch_size=50, shuffle=True)
validation_loader = DataLoader(validation_data, batch_size=50, shuffle=False)

device = torch.device("cpu")                            # I don't have a dedicated GPU

# Model
model = models.resnet18(pretrained=True)
model.fc = nn.Linear(model.fc.in_features, len(training_data.coin_classes))
model = model.to(device)

# Loss and optimizer
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=1e-4)

# Training function
def train_model(model, train_loader, val_loader, epochs=10):
    for epoch in range(epochs):
        model.train()
        running_loss = 0
        correct = 0
        total = 0
        running_loss = 0.0

        for images, labels in tqdm(train_loader, desc=f"Epoch {epoch+1}/{epochs}"):
            images, labels = images.to(device), labels.to(device)

            optimizer.zero_grad()                       # Clear the gradients from previous pass through the network
            outputs = model(images)                     # Forward Pass through the neural network
            loss = criterion(outputs, labels)           # Compute the cross entropy loss
            loss.backward()                             # Backpropagation
            optimizer.step()                            # not clear what this does

            running_loss += loss.item() * images.size(0)

            _, preds = outputs.max(1)
            correct += (preds == labels).sum().item()
            total += labels.size(0)

        train_loss = running_loss / total
        train_acc = correct / total

        val_loss, val_acc = evaluate(model, val_loader)

        print(f"Epoch{epoch+1}: Training Accuracy = {train_acc:.6f} Training Loss = {train_loss:.6f} Validation Accuracy = {val_acc:.6f} Validation Loss = {val_loss:.6f}")

# Evaluation function
def evaluate(model, val_loader):
    
    correct_pred = {classname: 0 for classname in val_loader.dataset.coin_classes}
    total_pred = {classname: 0 for classname in val_loader.dataset.coin_classes}

    model.eval()

    y_true, y_pred = [], []

    running_loss = 0.0 
    
    total = 0
    all_labels = []
    
    '''
    The no_grad() means that we are not doing this pass for learning purpose but rather for 
    prediction purpose. 
    '''
    with torch.no_grad():
        for images, labels in val_loader:
            images, labels = images.to(device), labels.to(device)
            outputs = model(images)
            _, preds = outputs.max(1)
            
            loss = criterion(outputs, labels)

            y_true.extend(labels.cpu().numpy())
            y_pred.extend(preds.cpu().numpy())

            running_loss +=  loss.item() * images.size(0)
            total += labels.size(0)

            for label, prediction in zip(labels, preds):
                classname = val_loader.dataset.coin_classes[label]
                if label == prediction :
                    correct_pred[classname] += 1
                total_pred[classname] += 1


    accuracy_per_class = {classname: correct_pred[classname] / total_pred[classname] if total_pred[classname] > 0 else 0
                          for classname in val_loader.dataset.coin_classes}

    # Calculate overall accuracy
    overall_accuracy = accuracy_score(y_true, y_pred)


    # Print the evaluation results
    print("Accuracy per class:")
    for classname, accuracy in accuracy_per_class.items():
        print(f"{classname}: {accuracy:.4f}")

    print()
    print(f"Overall Accuracy: {overall_accuracy:.4f}")

    val_loss = running_loss / total
    val_acc = sum([yt == yp for yt, yp in zip(y_true, y_pred)]) / total
    
    return val_loss, val_acc
    '''
    classification_report will compute the precision, recall, f1-score (prec * recall / prec + recall) and support
    '''    

#    print(classification_report(y_true, y_pred, target_names=validation_data.coin_classes))

# Train
train_model(model, train_loader, validation_loader, epochs=10)

# Test prediction
test_transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
])

model.eval()
test_preds = []
test_filenames = sorted(os.listdir('test'))         # Fetch all test image filenames         

for filename in test_filenames:
    img_path = os.path.join('test', filename)
    image = Image.open(img_path).convert("RGB")
    image = test_transform(image).unsqueeze(0).to(device)

    with torch.no_grad():
        output = model(image)
        pred = output.argmax(1).item()
        label = training_data.index_to_label[pred]
        test_preds.append((filename[:-4], label))

# Save predictions
submission = pd.DataFrame(test_preds, columns=['id', 'label'])
submission.to_csv('submission-test.csv', index=False)

# Save the weights for future use
torch.save(model.state_dict(), 'model_weights.pth')

