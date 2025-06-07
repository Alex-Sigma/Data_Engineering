# ml_pipeline/train.py
from .utils import get_logger
from .metrics import save_metrics, save_feature_importance
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

logger = get_logger(__name__)

def train_model(input_path: str, metrics_path: str, importance_path: str):
    logger.info(f"📆 Чтение {input_path}")
    df = pd.read_csv(input_path)
    y = df['species_label_encoded']
    X = df.drop(columns=[
        'species', 'species_label_encoded',
        'species_setosa', 'species_versicolor', 'species_virginica'
    ], errors='ignore')

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

    clf = RandomForestClassifier(n_estimators=100, random_state=42)
    clf.fit(X_train, y_train)
    train_score = clf.score(X_train, y_train)
    test_score = clf.score(X_test, y_test)

    importances = clf.feature_importances_
    importance_df = pd.DataFrame({
        'feature': X_train.columns,
        'importance': importances
    }).sort_values(by='importance', ascending=False)

    top5 = importance_df.head(5)['feature'].tolist()
    clf_top5 = RandomForestClassifier(n_estimators=100, random_state=42)
    clf_top5.fit(X_train[top5], y_train)
    train_top5 = clf_top5.score(X_train[top5], y_train)
    test_top5 = clf_top5.score(X_test[top5], y_test)

    save_metrics({
        'train_full': train_score,
        'test_full': test_score,
        'train_top5': train_top5,
        'test_top5': test_top5,
        'n_full': X.shape[1],
        'n_top5': len(top5),
    }, metrics_path)

    save_feature_importance(importance_df, importance_path)
    logger.info("✅ Модель обучена, метрики сохранены")

if __name__ == "__main__":
    train_model(
        input_path="data/db/features_iris.csv",
        metrics_path= "data/db/iris_model_metrics.csv", 
        importance_path= "data/db/iris_feature_importance.csv"
        
    )