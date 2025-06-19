# # ml_pipeline/train.py
# import pandas as pd
# import numpy as np
# import joblib
# from sklearn.ensemble import RandomForestClassifier
# from sklearn.model_selection import train_test_split
# from .utils import get_logger, save_csv

# logger = get_logger(__name__)

# def train_and_save_models(input_path: str, model_full_path: str, model_top5_path: str, importance_path: str):
#     df = pd.read_csv(input_path)
#     y = df['species_label_encoded']
#     X = df.drop(columns=[
#         'species', 'species_label_encoded',
#         'species_setosa', 'species_versicolor', 'species_virginica'
#     ], errors='ignore')

#     X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

#     clf_full = RandomForestClassifier(n_estimators=100, random_state=42)
#     clf_full.fit(X_train, y_train)

#     importances = clf_full.feature_importances_
#     importance_df = pd.DataFrame({"feature": X_train.columns, "importance": importances})

#     top5 = importance_df.sort_values(by='importance', ascending=False).head(5)['feature'].tolist()

#     clf_top5 = RandomForestClassifier(n_estimators=100, random_state=42)
#     clf_top5.fit(X_train[top5], y_train)

#     joblib.dump(clf_full, model_full_path)
#     joblib.dump(clf_top5, model_top5_path)
#     save_csv(importance_df, importance_path)

#     logger.info("✅ Модели и важности сохранены.")

# if __name__ == "__main__":
#     train_and_save_models(
#         input_path="data/db/features_iris.csv",
#         model_full_path="models/model_full.pkl",
#         model_top5_path="models/model_top5.pkl",
#         importance_path="data/db/iris_feature_importance.csv"
#     )

# # ml_pipeline/train.py
# import pandas as pd
# import numpy as np
# import os
# import joblib
# from sklearn.ensemble import RandomForestClassifier
# from sklearn.model_selection import train_test_split
# from .utils import get_logger

# logger = get_logger(__name__)

# def train_and_save_models(input_path: str, execution_date: str, model_root: str):
#     df = pd.read_csv(input_path)
#     y = df['species_label_encoded']
#     X = df.drop(columns=[
#         'species', 'species_label_encoded',
#         'species_setosa', 'species_versicolor', 'species_virginica'
#     ], errors='ignore')

#     X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

#     clf_full = RandomForestClassifier(n_estimators=100, random_state=42)
#     clf_full.fit(X_train, y_train)

#     importances = clf_full.feature_importances_
#     importance_df = pd.DataFrame({"feature": X_train.columns, "importance": importances})

#     top5 = importance_df.sort_values(by='importance', ascending=False).head(5)['feature'].tolist()

#     clf_top5 = RandomForestClassifier(n_estimators=100, random_state=42)
#     clf_top5.fit(X_train[top5], y_train)

#     # Папка по дате
#     dated_model_dir = os.path.join(model_root, execution_date)
#     os.makedirs(dated_model_dir, exist_ok=True)

#     joblib.dump(clf_full, os.path.join(dated_model_dir, "model_full.pkl"))
#     joblib.dump(clf_top5, os.path.join(dated_model_dir, "model_top5.pkl"))
#     importance_df.to_csv(os.path.join(dated_model_dir, "feature_importance.csv"), index=False)

#     logger.info(f"✅ Модели и важности сохранены в {dated_model_dir}")
#     return dated_model_dir

# if __name__ == "__main__":
#     import sys
#     from datetime import datetime

#     execution_date = sys.argv[1] if len(sys.argv) > 1 else datetime.today().date().isoformat()
#     input_path = f"data/db/{execution_date}/features.csv"
#     model_root = "models"

#     train_and_save_models(
#         input_path=input_path,
#         execution_date=execution_date,
#         model_root=model_root
#     )



# ml_pipeline/train.py
import pandas as pd
import numpy as np
import os
import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from .utils import get_logger

logger = get_logger(__name__)

def train_and_save_models(input_path: str, execution_date: str, model_root: str, data_root: str):
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

    # Создаём папки
    model_dir = os.path.join(model_root, execution_date)
    data_dir = os.path.join(data_root, execution_date)
    os.makedirs(model_dir, exist_ok=True)
    os.makedirs(data_dir, exist_ok=True)

    # Сохраняем модели
    joblib.dump(clf_full, os.path.join(model_dir, "model_full.pkl"))
    joblib.dump(clf_top5, os.path.join(model_dir, "model_top5.pkl"))

    # Сохраняем важности
    importance_path = os.path.join(data_dir, "feature_importance.csv")
    importance_df.to_csv(importance_path, index=False)

    logger.info(f"✅ Модели сохранены в {model_dir}")
    logger.info(f"✅ Важности признаков сохранены в {importance_path}")
    return model_dir, importance_path

if __name__ == "__main__":
    import sys
    from datetime import datetime

    execution_date = sys.argv[1] if len(sys.argv) > 1 else datetime.today().date().isoformat()
    input_path = f"data/db/{execution_date}/features.csv"
    model_root = "models"
    data_root = "data/db"

    train_and_save_models(
        input_path=input_path,
        execution_date=execution_date,
        model_root=model_root,
        data_root=data_root
    )


