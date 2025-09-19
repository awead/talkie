import openwakeword
from openwakeword.model import Model
import openwakeword.utils
import numpy as np

class WakeWordDetector:
    def __init__(self, wake_words=["alexa", "hey_jarvis"]):
        '''
        Initializes the class with the default model that include the pre-trained wake words.
        '''
        # Initialize the default model with pre-trained data
        self.model = Model()
        self.confidence_threshold = 0.5
        
    def detect(self, audio_chunk):
        """
        Process 80ms of 16kHz audio (1280 samples)
        Returns wake word name if detected, None otherwise
        """
        prediction = self.model.predict(audio_chunk)
        
        for wake_word in prediction:
            confidence = prediction[wake_word]
            if confidence > self.confidence_threshold:
                print(f"Wake word '{wake_word}' detected with confidence {confidence:.2f}")
                return wake_word
        return None

