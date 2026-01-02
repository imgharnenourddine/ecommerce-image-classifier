# Ecommerce Image Classifier

## Description

Ce projet est une **application web de reconnaissance et classification d’images de produits pour e-commerce**.  
Elle permet de :

- Télécharger des images de produits via l’interface web.
- Reconnaître automatiquement la catégorie du produit (ex : chaussures, t-shirts, sacs) grâce à un **modèle Keras pré-entraîné et fine-tuning**.
- Visualiser les résultats et les statistiques sur un **dashboard Streamlit**.
- Exporter les résultats dans une base de données pour intégration dans un système e-commerce.

---

## Architecture du projet

Le projet utilise **Flask pour le backend**, **HTML/CSS/JS pour le frontend**, et **Streamlit pour le dashboard**.  
L’architecture des dossiers est la suivante :

package/
│
├── routes/ # Définition des routes Flask pour l'upload et l'affichage
├── templates/ # Pages HTML
├── static/ # CSS, JS, images
├── models/ # Modèles pour la base de données
├── ai/ # Chargement et prédiction du modèle Keras
└── uploads/ # Images uploadées par l’utilisateur

## Fonctionnalités principales

1. **Upload d’images** : L’utilisateur peut uploader des images de produits depuis son ordinateur.  
2. **Classification IA** : Le modèle Keras prédit la catégorie du produit et retourne la probabilité.  
3. **Visualisation** : Les résultats sont affichés dans le frontend Flask et envoyés au dashboard Streamlit.  
4. **Base de données** : Les informations sur les produits uploadés et leurs catégories sont stockées pour analyse.  
5. **Dashboard Streamlit** : Affichage des statistiques par catégorie, nombre d’images uploadées, et performances du modèle.


## Technologies utilisées

- **Python**  
- **Flask** (backend)  
- **HTML / CSS / JS** (frontend)  
- **Keras / TensorFlow** (modèle IA)  
- **Streamlit** (dashboard interactif)  
- **SQLite / PostgreSQL** (base de données)