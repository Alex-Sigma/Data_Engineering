# ml_pipeline/train.py
import pandas as pd
import numpy as np
import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from .utils import get_logger, save_csv

logger = get_logger(__name__)

def train_and_save_models(input_path: str, model_full_path: str, model_top5_path: str, importance_path: str):
    df = pd.read_csv(input_path)
    y = df['species_label_encoded']
    X = df.drop(columns=[
        'species', 'species_label_encoded',
        'species_setosa', 'species_versicolor', 'species_virginica'
    ], errors='ignore')

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

    clf_full = RandomForestClassifier(n_estimators=100, random_state=42)
    clf_full.fit(X_train, y_train)

    importances = clf_full.feature_importances_
    importance_df = pd.DataFrame({"feature": X_train.columns, "importance": importances})

    top5 = importance_df.sort_values(by='importance', ascending=False).head(5)['feature'].tolist()

    clf_top5 = RandomForestClassifier(n_estimators=100, random_state=42)
    clf_top5.fit(X_train[top5], y_train)

    joblib.dump(clf_full, model_full_path)
    joblib.dump(clf_top5, model_top5_path)
    save_csv(importance_df, importance_path)

    logger.info("✅ Модели и важности сохранены.")

if __name__ == "__main__":
    train_and_save_models(
        input_path="data/db/features_iris.csv",
        model_full_path="models/model_full.pkl",
        model_top5_path="models/model_top5.pkl",
        importance_path="data/db/iris_feature_importance.csv"
    )