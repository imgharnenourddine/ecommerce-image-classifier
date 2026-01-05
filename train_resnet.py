import torch
import torch.nn as nn
import torch.optim as optim
from torchvision import datasets, models, transforms
from torch.utils.data import DataLoader
import os

# 1. Configuration
data_dir = 'ecommerce_dataset' # Le dossier créé à l'étape précédente
num_classes = 5                # Le nombre de catégories que vous avez choisies
batch_size = 32                # Nombre d'images traitées en même temps
epochs = 10                    # Nombre de fois que l'IA va voir tout le dataset
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# 2. Transformations d'images (Redimensionner pour ResNet50)
data_transforms = {
    'train': transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.RandomHorizontalFlip(),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
    ]),
    'val': transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
    ]),
}

# 3. Chargement des images depuis les dossiers
image_datasets = {x: datasets.ImageFolder(os.path.join(data_dir, x), data_transforms[x])
                  for x in ['train', 'val']}

dataloaders = {x: DataLoader(image_datasets[x], batch_size=batch_size, shuffle=True)
               for x in ['train', 'val']}

# 4. Préparation du modèle ResNet50 (Fine-Tuning)
model = models.resnet50(weights=models.ResNet50_Weights.DEFAULT)

# Geler les couches anciennes
for param in model.parameters():
    param.requires_grad = False

# Remplacer la dernière couche par une adaptée à vos catégories
num_ftrs = model.fc.in_features
model.fc = nn.Linear(num_ftrs, num_classes)

model = model.to(device)

# 5. Fonction de perte et Optimiseur
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.fc.parameters(), lr=0.001)

# 6. Boucle d'entraînement
print(f"Entraînement démarré sur : {device}")
for epoch in range(epochs):
    model.train()
    running_loss = 0.0
    
    for inputs, labels in dataloaders['train']:
        inputs, labels = inputs.to(device), labels.to(device)
        
        optimizer.zero_grad()
        outputs = model(inputs)
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()
        
        running_loss += loss.item() * inputs.size(0)
    
    epoch_loss = running_loss / len(image_datasets['train'])
    print(f"Epoch {epoch+1}/{epochs} - Loss: {epoch_loss:.4f}")

# 7. Sauvegarder le modèle final
torch.save(model.state_dict(), "ecommerce_resnet50.pth")
print("Modèle sauvegardé sous le nom : ecommerce_resnet50.pth")