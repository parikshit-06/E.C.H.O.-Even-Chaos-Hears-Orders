import numpy as np
from openwakeword.model import Model

# Test model loading
print("Loading 'hey jarvis' model...")
m = Model(wakeword_models=['hey jarvis'])
print("Models loaded:", list(m.models.keys()))

# Test prediction with silence (should return low scores)
silent_audio = np.zeros(1280, dtype=np.int16)
preds = m.predict(silent_audio)
print("Prediction on silence:", preds)

# Check the class_mapping
print("Class mapping:", m.class_mapping)
