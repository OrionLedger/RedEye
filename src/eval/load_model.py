import os
import joblib
from dotenv import load_dotenv

if os.getenv("red_eye_state", "development") == "development":
    from dotenv import load_dotenv
    load_dotenv()

def load_kmeans_model(model_filename="kmeans_model.joblib"):
    models_path = os.environ.get("MODELS")
    if models_path is None:
        raise EnvironmentError("Please set the MODELS environment variable to load the model.")
    
    model_file = os.path.join(models_path, model_filename)
    if not os.path.exists(model_file):
        raise FileNotFoundError(f"Model file not found at {model_file}")
    
    model = joblib.load(model_file)
    return model
