
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
import pandas as pd
import joblib
import os

MODEL_PATH = os.path.join(os.path.dirname(__file__), "models", "category_model.joblib")

def train_model():
    # Train a simple TF-IDF + Logistic Regression classifier from sample CSV.
    data_path = os.path.join(os.path.dirname(__file__), "data", "sample_training_data.csv")
    data = pd.read_csv(data_path)
    X, y = data["merchant"], data["category"]
    model = make_pipeline(TfidfVectorizer(ngram_range=(1,2)), LogisticRegression(max_iter=1000))
    model.fit(X, y)
    joblib.dump(model, MODEL_PATH)
    return MODEL_PATH

def load_model():
    return joblib.load(MODEL_PATH)
