# ml_pipeline/metrics.py
import pandas as pd
from sklearn.metrics import accuracy_score
from .utils import get_logger, save_csv, get_timestamp

logger = get_logger(__name__)

def compute_metrics_from_predictions(pred_path: str, metrics_path: str):
    df = pd.read_csv(pred_path)
    acc_full = accuracy_score(df["y_true"], df["y_pred_full"])
    acc_top5 = accuracy_score(df["y_true"], df["y_pred_top5"])

    results = pd.DataFrame({
        "model_type": ["full_model", "top5_model"],
        "accuracy": [acc_full, acc_top5],
        "run_timestamp": [get_timestamp()] * 2
    })

    save_csv(results, metrics_path)
    logger.info(f"✅ Метрики сохранены в {metrics_path}")

if __name__ == "__main__":
    compute_metrics_from_predictions(
        pred_path="data/db/iris_predictions.csv",
        metrics_path="data/db/iris_model_metrics.csv"
    )
