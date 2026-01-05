import os
import torch
import torch.nn as nn
from torchvision import models, transforms
from PIL import Image

# --- CONFIGURATION DES CHEMINS ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__)) # dossier 'ai'
BACKEND_DIR = os.path.dirname(BASE_DIR)              # dossier 'backend'
ROOT_DIR = os.path.dirname(BACKEND_DIR)               # Racine du projet

# Le chemin pointe maintenant vers : Racine/model/ecommerce_resnet50.pth
MODEL_PATH = os.path.join(ROOT_DIR, 'model', 'ecommerce_resnet50.pth')

# --- CONFIGURATION IA ---
# Remplace par tes vraies catégories dans l'ordre alphabétique
CLASS_NAMES = ['Handbags', 'Jeans', 'Shirts', 'Shoes', 'Watches']
num_classes = len(CLASS_NAMES)
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# --- CHARGEMENT DU MODÈLE ---
def load_resnet_model():
    print(f"🔄 Chargement du modèle PyTorch depuis : {MODEL_PATH}")
    try:
        # 1. Recréer l'architecture ResNet50
        model = models.resnet50(weights=None)
        num_ftrs = model.fc.in_features
        model.fc = nn.Linear(num_ftrs, num_classes)
        
        # 2. Charger les poids (.pth)
        model.load_state_dict(torch.load(MODEL_PATH, map_location=device))
        model.to(device)
        model.eval() # Mode évaluation
        print("✅ Modèle ResNet50 chargé avec succès !")
        return model
    except Exception as e:
        print(f"❌ ERREUR : Impossible de charger le modèle.\n{e}")
        return None

model = load_resnet_model()

# --- FONCTION DE PRÉDICTION ---
def predict_image(image_path):
    if model is None:
        return "Erreur Modèle", 0.0

    try:
        # 1. Préparation de l'image (Exactement comme à l'entraînement)
        transform = transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
        ])

        # 2. Ouvrir l'image
        img = Image.open(image_path).convert('RGB')
        img_tensor = transform(img).unsqueeze(0).to(device)

        # 3. Prédiction
        with torch.no_grad():
            outputs = model(img_tensor)
            # Softmax pour obtenir des probabilités (0 à 1)
            probabilities = torch.nn.functional.softmax(outputs[0], dim=0)
            
            # Récupérer le meilleur score
            confidence, class_index = torch.max(probabilities, 0)
            
        result_class = CLASS_NAMES[class_index.item()]
        conf_score = confidence.item() * 100

        print(f"🔍 Résultat IA : {result_class} ({conf_score:.2f}%)")
        return result_class, round(conf_score, 2)

    except Exception as e:
        print(f"⚠️ Erreur pendant la prédiction : {str(e)}")
        return "Erreur Image", 0.0