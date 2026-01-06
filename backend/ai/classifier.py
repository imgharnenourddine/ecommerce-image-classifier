import os
import torch
import torch.nn as nn
from torchvision import models, transforms
from PIL import Image

# --- CONFIGURATION DES CHEMINS ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__)) 
BACKEND_DIR = os.path.dirname(BASE_DIR)              
ROOT_DIR = os.path.dirname(BACKEND_DIR)               

# Chemin vers le nouveau modèle entraîné avec 4 catégories
MODEL_PATH = os.path.join(ROOT_DIR, 'model', 'ecommerce_resnet50.pth')

# --- CONFIGURATION IA ---
# Ordre alphabétique strict correspondant aux dossiers de ecommerce_dataset/train
CLASS_NAMES = ['Handbags', 'Jeans', 'Shirts', 'Watches']
num_classes = len(CLASS_NAMES)
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# --- CHARGEMENT DU MODÈLE ---
def load_resnet_model():
    print(f"🔄 Chargement du modèle PyTorch depuis : {MODEL_PATH}")
    try:
        # Initialisation architecture ResNet50
        model = models.resnet50(weights=None)
        num_ftrs = model.fc.in_features
        # On définit 4 neurones de sortie
        model.fc = nn.Linear(num_ftrs, num_classes)
        
        # Chargement des poids entraînés
        model.load_state_dict(torch.load(MODEL_PATH, map_location=device))
        model.to(device)
        model.eval() 
        print("✅ Modèle ResNet50 (4 classes) chargé avec succès !")
        return model
    except Exception as e:
        print(f"❌ ERREUR CHARGEMENT : {e}")
        return None

model = load_resnet_model()

# --- FONCTION DE PRÉDICTION ---
def predict_image(image_path):
    if model is None:
        return "Model Error", 0.0

    try:
        # Prétraitement standard pour ResNet
        transform = transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
        ])

        # Ouverture de l'image
        img = Image.open(image_path).convert('RGB')
        img_tensor = transform(img).unsqueeze(0).to(device)

        with torch.no_grad():
            outputs = model(img_tensor)
            
            # Conversion des scores bruts en probabilités (Somme = 1.0)
            probabilities = torch.nn.functional.softmax(outputs, dim=1)
            
            # Extraction de la classe avec la plus haute probabilité
            confidence, class_index = torch.max(probabilities, 1)
            
            # On récupère la valeur entre 0.0 et 1.0
            conf_score = confidence.item() 
            result_class = CLASS_NAMES[class_index.item()]

        print(f"🔍 Résultat IA : {result_class} ({conf_score*100:.2f}%)")
        
        # On retourne le label et le score (ex: 0.8542)
        return result_class, round(conf_score, 4)

    except Exception as e:
        print(f"⚠️ Erreur prédiction : {str(e)}")
        return "Image Error", 0.0