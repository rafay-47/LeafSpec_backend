from PIL import Image
import numpy as np
from app import mb

class PredictionService:
    SPECIES = [
        'Aloe Vera', 'Alstonia Scholaris', 'Apple', 'Arjun', 'Blueberry',
        'Buxus sempervirens L(200)', 'Cherry', 'Corn', 'Cotinus coggygria Scop(200)',
        'Crataegus monogyna Jacq(200)', 'Fraxinus angustifolia Vahl(200)', 'Grape',
        'Guava', 'Hedera helix L(200)', 'Jamun', 'Jatropha', 'Kale',
        'Laurus nobilis L(200)', 'Lemon', 'Mango', 'Orange', 'Paddy Rice',
        'Peach', 'Pepper Bell', 'Phillyrea angustifolia L(200)',
        'Pistacia lentiscus L(200)', 'Pittosporum tobira Thunb WTAiton(200)',
        'Pomegranate', 'Pongamia Pinnata', 'Populus alba L(200)',
        'Populus nigra L(200)', 'Potato', 'Quercus ilex L(200)', 'Raspberry',
        'Soybean', 'Spinach', 'Strawberry', 'Tobacco', 'Tomato'
    ]

    @staticmethod
    def preprocess_image(image):
        image = image.resize((224, 224))
        image = np.array(image)
        image = image / 255.0
        image = np.expand_dims(image, axis=0)
        return image

    @staticmethod
    def predict(image):
        preprocessed_image = PredictionService.preprocess_image(image)
        prediction_data = mb.get_inference(
            region="us-east-1.aws",
            workspace="nu-edu",
            deployment="predict_species",
            data={"image": preprocessed_image.tolist()}
        )
        
        prediction = prediction_data.get('data', {}).get('prediction', [])
        predicted_species = PredictionService.SPECIES[np.argmax(prediction)]
        confidence = prediction[0][np.argmax(prediction)]
        
        return predicted_species, str(confidence)
