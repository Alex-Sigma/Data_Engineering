import logging
import pandas as pd
import os
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

# Настройка логгера
logging.basicConfig(level=logging.INFO, format='🧠 [%(levelname)s] %(message)s')
logger = logging.getLogger(__name__)

def train_model_from_features():
    logger.info("📦 Загружаем признаки из features_iris.csv ...")
    df = pd.read_csv("data/db/features_iris.csv")
    logger.info(f"🔢 Загружено {df.shape[0]} строк и {df.shape[1]} столбцов.")

    # Целевая переменная
    y = df['species_label_encoded']
    X = df.drop(columns=[
        'species', 'species_label_encoded',
        'species_setosa', 'species_versicolor', 'species_virginica'
    ], errors='ignore')

    logger.info("✂️ Делим выборку на train/test ...")
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.3, random_state=42
    )

    # Полная модель
    logger.info("🧠 Обучаем полную модель RandomForestClassifier ...")
    clf_full = RandomForestClassifier(n_estimators=100, random_state=42)
    clf_full.fit(X_train, y_train)
    train_score_full = clf_full.score(X_train, y_train)
    test_score_full = clf_full.score(X_test, y_test)
    logger.info(f"✅ Полная модель: train={train_score_full:.4f}, test={test_score_full:.4f}")

    # Важность признаков
    importances = clf_full.feature_importances_
    importance_df = pd.DataFrame({
        'feature': X_train.columns,
        'importance': importances
    }).sort_values(by='importance', ascending=False)

    top_features = importance_df.head(5)['feature'].tolist()
    logger.info(f"🏆 Топ-5 признаков: {top_features}")

    # Модель на топ-5
    logger.info("🧠 Обучаем модель только на топ-5 признаках ...")
    clf_top5 = RandomForestClassifier(n_estimators=100, random_state=42)
    clf_top5.fit(X_train[top_features], y_train)
    train_score_top5 = clf_top5.score(X_train[top_features], y_train)
    test_score_top5 = clf_top5.score(X_test[top_features], y_test)
    logger.info(f"✅ Модель на топ-5: train={train_score_top5:.4f}, test={test_score_top5:.4f}")

    # Сохраняем результаты
    logger.info("💾 Сохраняем метрики и важность признаков ...")
    os.makedirs("data/db", exist_ok=True)

    pd.DataFrame({
        'model_type': ['full_model', 'top5_model'],
        'train_accuracy': [train_score_full, train_score_top5],
        'test_accuracy': [test_score_full, test_score_top5],
        'features_count': [X.shape[1], len(top_features)],
        'run_timestamp': [pd.Timestamp.now(), pd.Timestamp.now()]
    }).to_csv("data/db/iris_model_metrics.csv", index=False)

    importance_df['run_timestamp'] = pd.Timestamp.now()
    importance_df.to_csv("data/db/iris_feature_importance.csv", index=False)

    logger.info("📁 Всё готово. Метрики и важности сохранены в data/db/")

if __name__ == "__main__":
    train_model_from_features()
