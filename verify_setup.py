import sys
import os
import io
import unittest
import numpy as np
from PIL import Image

# Add project root to path
sys.path.append(os.getcwd())

from backend.app import create_app
from backend.services.classifier import classifier

class TestECommerceApp(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()
        self.app.testing = True

    def test_classifier_loading(self):
        print("\nTesting Model Loading...")
        self.assertIsNotNone(classifier.model)
        print("Model loaded successfully.")

    def test_prediction_endpoint(self):
        print("\nTesting Prediction Endpoint...")
        # Create a dummy image (100x100 white image)
        img = Image.new('RGB', (100, 100), color = 'white')
        img_byte_arr = io.BytesIO()
        img.save(img_byte_arr, format='JPEG')
        img_byte_arr.seek(0)

        response = self.client.post('/api/predict', data={
            'file': (img_byte_arr, 'test.jpg')
        })
        
        self.assertEqual(response.status_code, 200)
        json_data = response.get_json()
        self.assertIn('predictions', json_data)
        print("Predictions received:", json_data['predictions'])

if __name__ == '__main__':
    unittest.main()
