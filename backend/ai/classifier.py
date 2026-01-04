# import os
# import numpy as np
# from tensorflow.keras.models import load_model
# from tensorflow.keras.preprocessing import image


# BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# BASE_DIR = os.path.dirname(os.path.dirname(BASE_DIR))
# MODEL_PATH = os.path.join(BASE_DIR, 'model', 'model.h5')

# IMG_HEIGHT = 224
# IMG_WIDTH = 224
# CLASS_NAMES = ['Classe 0', 'Classe 1', 'Classe 2'] 

# print(f"🔄 Chargement du modèle IA depuis : {MODEL_PATH}")
# try:
#     model = load_model(MODEL_PATH)
#     print("✅ Modèle chargé avec succès !")
# except Exception as e:
#     print(f"❌ ERREUR CRITIQUE : Impossible de charger le modèle.\n{e}")
#     model = None

# def predict_image(image_path):
   
    
#     # Sécurité : Si le modèle a planté au chargement
#     if model is None:
#         return "Erreur Modèle", 0.0

#     try:
#         # A. Chargement et Redimensionnement de l'image
#         img = image.load_img(image_path, target_size=(IMG_HEIGHT, IMG_WIDTH))

#         # B. Transformation en tableau de nombres (Array)
#         img_array = image.img_to_array(img)

#         # C. Ajout d'une dimension pour le batch (Le modèle attend [1, 224, 224, 3])
#         img_array = np.expand_dims(img_array, axis=0)

#         # D. Normalisation (CRUCIAL : Diviser par 255 si vous l'avez fait à l'entraînement)
#         img_array = img_array / 255.0

#         # E. Prédiction
#         predictions = model.predict(img_array)
        
#         # --- LOGIQUE DE DÉCODAGE (CHOISISSEZ VOTRE CAS) ---
        
#         # CAS 1 : Classification Multi-classes (Softmax - Plusieurs neurones de sortie)
#         # On prend l'index qui a la plus grande probabilité
       
#         class_index = np.argmax(predictions[0])
#         confidence = float(np.max(predictions[0])) * 100
#         result_class = CLASS_NAMES[class_index]

        

#         print(f"🔍 Résultat IA : {result_class} ({confidence:.2f}%)")
#         return result_class, round(confidence, 2)

#     except Exception as e:
#         print(f"⚠️ Erreur pendant la prédiction : {str(e)}")
#         return "Erreur Inconnue", 0.0