# process_iris_ml_only.py

import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

def process_iris_data():
    # Загрузка данных
    df = pd.read_csv("data/iris_data.csv")
    print(f"Loaded {df.shape[0]} rows with {df.shape[1]} columns.")

    # Кодируем целевую переменную
    df["species_label_encoded"] = df["species"].astype("category").cat.codes

    # Делим данные на X и y
    X = df.drop(columns=["species", "species_label_encoded"])
    y = df["species_label_encoded"]

    # Масштабируем признаки
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # Разделение на обучающую и тестовую выборки
    X_train, X_test, y_train, y_test = train_test_split(
        X_scaled, y, test_size=0.3, random_state=42
    )

    # Обучаем модель
    clf = RandomForestClassifier(n_estimators=100, random_state=42)
    clf.fit(X_train, y_train)

    # Оцениваем качество
    train_score = clf.score(X_train, y_train)
    test_score = clf.score(X_test, y_test)
    print(f"Train accuracy: {train_score:.4f}")
    print(f"Test accuracy:  {test_score:.4f}")

    # Важность признаков
    feature_importances = clf.feature_importances_
    feature_names = df.drop(columns=["species", "species_label_encoded"]).columns

    print("\nFeature Importances:")
    for name, importance in zip(feature_names, feature_importances):
        print(f"{name}: {importance:.4f}")

if __name__ == "__main__":
    process_iris_data()
