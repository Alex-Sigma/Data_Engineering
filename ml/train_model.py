import pandas as pd
import os
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

def train_model_from_features():
    df = pd.read_csv("data/db/features_iris.csv")

    # Целевая переменная
    y = df['species_label_encoded']
    X = df.drop(columns=[
        'species', 'species_label_encoded',
        'species_setosa', 'species_versicolor', 'species_virginica'
    ], errors='ignore')

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

    # Полная модель
    clf_full = RandomForestClassifier(n_estimators=100, random_state=42)
    clf_full.fit(X_train, y_train)
    train_score_full = clf_full.score(X_train, y_train)
    test_score_full = clf_full.score(X_test, y_test)

    # Важность признаков
    importances = clf_full.feature_importances_
    importance_df = pd.DataFrame({
        'feature': X_train.columns,
        'importance': importances
    }).sort_values(by='importance', ascending=False)

    top_features = importance_df.head(5)['feature'].tolist()

    # Модель на топ-5
    clf_top5 = RandomForestClassifier(n_estimators=100, random_state=42)
    clf_top5.fit(X_train[top_features], y_train)
    train_score_top5 = clf_top5.score(X_train[top_features], y_train)
    test_score_top5 = clf_top5.score(X_test[top_features], y_test)

    # Сохраняем результаты
    os.makedirs("data/db", exist_ok=True)

    pd.DataFrame({
        'model_type': ['full_model', 'top5_model'],
        'train_accuracy': [train_score_full, train_score_top5],
        'test_accuracy': [test_score_full, test_score_top5],
        'features_count': [X.shape[1], len(top_features)],
        'run_timestamp': [pd.Timestamp.now(), pd.Timestamp.now()]
    }).to_csv("data/db/model_metrics.csv", index=False)

    importance_df['run_timestamp'] = pd.Timestamp.now()
    importance_df.to_csv("data/db/feature_importance.csv", index=False)

    print("✅ Model trained. Metrics saved in data/db/")

if __name__ == "__main__":
    train_model_from_features()
