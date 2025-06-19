# # ml_pipeline/predict.py
# import pandas as pd
# import joblib
# from .utils import get_logger, save_csv

# logger = get_logger(__name__)

# def predict_and_save(input_path: str, model_full_path: str, model_top5_path: str, output_path: str):
#     df = pd.read_csv(input_path)
#     y = df['species_label_encoded']
#     X = df.drop(columns=[
#         'species', 'species_label_encoded',
#         'species_setosa', 'species_versicolor', 'species_virginica'
#     ], errors='ignore')

#     clf_full = joblib.load(model_full_path)
#     clf_top5 = joblib.load(model_top5_path)
#     top5 = clf_top5.feature_names_in_

#     df_preds = pd.DataFrame({
#         "y_true": y,
#         "y_pred_full": clf_full.predict(X),
#         "y_pred_top5": clf_top5.predict(X[top5])
#     })

#     save_csv(df_preds, output_path)
#     logger.info(f"✅ Предсказания сохранены в {output_path}")

# if __name__ == "__main__":
#     predict_and_save(
#         input_path="data/db/features_iris.csv",
#         model_full_path="models/model_full.pkl",
#         model_top5_path="models/model_top5.pkl",
#         output_path="data/db/iris_predictions.csv"
#     )

# ml_pipeline/predict.py
import pandas as pd
import os
import joblib
from .utils import get_logger, save_csv

logger = get_logger(__name__)

def predict_and_save(execution_date: str, data_root: str, model_root: str):
    # Пути
    date_dir = os.path.join(data_root, execution_date)
    input_path = os.path.join(date_dir, "features.csv")
    model_full_path = os.path.join(model_root, execution_date, "model_full.pkl")
    model_top5_path = os.path.join(model_root, execution_date, "model_top5.pkl")
    output_path = os.path.join(date_dir, "predictions.csv")

    # Загрузка данных
    df = pd.read_csv(input_path)
    y = df['species_label_encoded']
    X = df.drop(columns=[
        'species', 'species_label_encoded',
        'species_setosa', 'species_versicolor', 'species_virginica'
    ], errors='ignore')

    # Загрузка моделей
    clf_full = joblib.load(model_full_path)
    clf_top5 = joblib.load(model_top5_path)
    top5 = clf_top5.feature_names_in_

    # Предсказания
    df_preds = pd.DataFrame({
        "y_true": y,
        "y_pred_full": clf_full.predict(X),
        "y_pred_top5": clf_top5.predict(X[top5])
    })

    # Сохранение
    save_csv(df_preds, output_path)
    logger.info(f"✅ Предсказания сохранены в {output_path}")
    return output_path

if __name__ == "__main__":
    import sys
    from datetime import datetime

    execution_date = sys.argv[1] if len(sys.argv) > 1 else datetime.today().date().isoformat()
    predict_and_save(
        execution_date=execution_date,
        data_root="data/db",
        model_root="models"
    )
