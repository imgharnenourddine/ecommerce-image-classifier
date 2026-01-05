import pandas as pd
import os
import shutil
from sklearn.model_selection import train_test_split

# 1. Configuration des chemins
csv_path = "styles.csv"  # Nom de votre fichier
images_dir = "images"    # Dossier contenant vos images .jpg
output_dir = "ecommerce_dataset"

# 2. Charger le CSV
df = pd.read_csv(csv_path, on_bad_lines='skip')

# 3. Sélectionner les catégories que vous voulez (Exemple: Shirts, Jeans, Watches, Shoes)
# Vous pouvez en ajouter d'autres présentes dans la colonne articleType
categories_to_keep = ['Shirts', 'Jeans', 'Watches', 'Shoes', 'Handbags']
df = df[df['articleType'].isin(categories_to_keep)]

# 4. Limiter le nombre d'images par catégorie (ex: 500 pour commencer léger)
df = df.groupby('articleType').head(500)

train_df, val_df = train_test_split(df, test_size=0.2, stratify=df['articleType'])

def prepare_folders(data_df, subset_name):
    for _, row in data_df.iterrows():
        category = row['articleType']
        img_name = f"{int(row['id'])}.jpg"
        src_path = os.path.join(images_dir, img_name)
        
        # Créer le dossier de destination : ecommerce_dataset/train/Shirts/
        dest_dir = os.path.join(output_dir, subset_name, category)
        os.makedirs(dest_dir, exist_ok=True)
        
        # Copier l'image si elle existe
        if os.path.exists(src_path):
            shutil.copy(src_path, os.path.join(dest_dir, img_name))

# Lancer la copie
print("Début de l'organisation des images...")
prepare_folders(train_df, 'train')
prepare_folders(val_df, 'val')
print(f"Terminé ! Votre dataset est prêt dans le dossier : {output_dir}")