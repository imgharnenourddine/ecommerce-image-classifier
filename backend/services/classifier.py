import tensorflow as tf
from tensorflow.keras.applications.mobilenet_v2 import MobileNetV2, preprocess_input, decode_predictions
from tensorflow.keras.preprocessing import image
import numpy as np
from PIL import Image
import io

class Classifier:
    def __init__(self):
        # Load the pre-trained MobileNetV2 model
        self.model = MobileNetV2(weights='imagenet')

    def predict(self, image_bytes):
        # Load image from bytes
        img = Image.open(io.BytesIO(image_bytes))
        
        # Resize image to 224x224 as required by MobileNetV2
        img = img.resize((224, 224))
        
        # Convert to array and preprocess
        x = image.img_to_array(img)
        x = np.expand_dims(x, axis=0)
        x = preprocess_input(x)
        
        # Predict
        preds = self.model.predict(x)
        
        # Decode predictions (returns list of tuples (class_id, class_name, probability))
        # Top 3 predictions
        results = decode_predictions(preds, top=3)[0]
        
        formatted_results = []
        for _, class_name, prob in results:
            formatted_results.append({
                "class": class_name,
                "confidence": float(prob)
            })
            
        return formatted_results

# Global instance
classifier = Classifier()
