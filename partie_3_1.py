from google.colab import drive
drive.mount('/content/drive')

import pandas as pd
import torch
from torch.utils.data import Dataset, DataLoader
import torch.nn as nn
import torch.optim as optim

# Charger le dataset avec avertissements Dtype
labelled_dataset = pd.read_csv('/content/drive/MyDrive/TPDataScience/database_with_activities.csv')

# Supprimer les lignes où il n'y a rien dans la colonne 'Activity'
labelled_dataset = labelled_dataset.dropna(subset=['Activity'])

# Définir la classe du dataset personnalisé
class CustomDataset(Dataset):
    def __init__(self, csv_file):
        self.data = pd.read_csv(csv_file, low_memory=False)  # Lire le fichier CSV dans un DataFrame
        self.data = self.data.apply(pd.to_numeric, errors='coerce')  # Convertir les données en numériques
        self.data.fillna(0, inplace=True)  # Remplacer les valeurs manquantes par 0

        # Supprimer les lignes où il n'y a rien dans la colonne 'Activity'
        self.data = self.data.dropna(subset=['Activity'])

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        features = torch.tensor(self.data.iloc[idx, :-1].values, dtype=torch.float32)  # Exclure la dernière colonne (label)

        # Recherche dynamique de la colonne contenant les étiquettes
        label_column = self.data.columns[-1]  # Récupérer le nom de la dernière colonne
        label_value = self.data.loc[idx, label_column]  # Récupérer la valeur de l'étiquette

        # Vérifier si la valeur de l'étiquette est trop grande ou contient des décimales
        if label_value > 2147483647 or label_value != int(label_value):
            raise ValueError(f"Label value {label_value} at index {idx} cannot be converted to int64 without overflow or contains decimals.")

        label = torch.tensor(int(label_value), dtype=torch.long)  # Convertir la valeur de l'étiquette en entier

        return features, label

# Charger l'ensemble de données
dataset = CustomDataset('/content/drive/MyDrive/TPDataScience/database_with_activities.csv')
data_loader = DataLoader(dataset, batch_size=32, shuffle=True)

# Définir le modèle
class SimpleNN(nn.Module):
    def __init__(self, input_size, output_size):
        super(SimpleNN, self).__init__()
        self.fc1 = nn.Linear(input_size, 64)
        self.fc2 = nn.Linear(64, 32)
        self.fc3 = nn.Linear(32, output_size)

    def forward(self, x):
        x = torch.relu(self.fc1(x))
        x = torch.relu(self.fc2(x))
        x = self.fc3(x)
        return x

# Initialiser le modèle
input_size = len(labelled_dataset.columns) - 1  # Exclure la colonne label
output_size = 10  # Nombre de classes d'activité
model = SimpleNN(input_size, output_size)

# Définir la fonction de perte et l'optimiseur
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)

# Entraîner le modèle
for epoch in range(10):  # 10 époques
    running_loss = 0.0
    for inputs, labels in data_loader:
        optimizer.zero_grad()
        outputs = model(inputs)
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()
        running_loss += loss.item()
    print(f"Epoch {epoch+1}, Loss: {running_loss / len(data_loader)}")

correct = 0
total = 0
with torch.no_grad():
    for inputs, labels in data_loader:
        outputs = model(inputs)
        _, predicted = torch.max(outputs.data, 1)
        total += labels.size(0)
        correct += (predicted == labels).sum().item()

print(f"Accuracy: {100 * correct / total}%")
