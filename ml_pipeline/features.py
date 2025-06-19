# # ml_pipeline/features.py
# import pandas as pd
# import numpy as np
# from itertools import combinations
# from sklearn.preprocessing import (
#     KBinsDiscretizer, RobustScaler, MaxAbsScaler, MinMaxScaler,
#     StandardScaler, LabelEncoder, OneHotEncoder, FunctionTransformer
# )
# from .utils import get_logger, save_csv

# logger = get_logger(__name__)

# def generate_features(input_path: str, output_path: str):
#     df = pd.read_csv(input_path)
#     logger.info(f"Загружено {df.shape[0]} строк, {df.shape[1]} столбцов.")

#     numeric_cols = ['sepal_length', 'sepal_width', 'petal_length', 'petal_width']
#     result = df[numeric_cols].copy()

#     for strategy in ['quantile', 'uniform']:
#         kbins = KBinsDiscretizer(n_bins=5, encode='ordinal', strategy=strategy)
#         result[[f"{col}_{strategy}_bin" for col in numeric_cols]] = kbins.fit_transform(df[numeric_cols])

#     result[[f"{col}_robust_scaled" for col in numeric_cols]] = RobustScaler().fit_transform(df[numeric_cols])
#     result[[f"{col}_max_absolute_scaled" for col in numeric_cols]] = MaxAbsScaler().fit_transform(df[numeric_cols])
#     result[[f"{col}_max_min_max_scaled" for col in numeric_cols]] = MinMaxScaler((0, 1)).fit_transform(df[numeric_cols])
#     result[[f"{col}_logged" for col in numeric_cols]] = FunctionTransformer(np.log1p).fit_transform(df[numeric_cols])
#     result[[f"{col}_standardized" for col in numeric_cols]] = StandardScaler().fit_transform(df[numeric_cols])

#     for col in numeric_cols:
#         result[f"{col}_binarized"] = (df[col] > df[col].median()).astype(int)

#     for col1, col2 in combinations(numeric_cols, 2):
#         result[f"{col1}_x_{col2}_interaction"] = df[col1] * df[col2]
#         result[f"{col1}_plus_{col2}_interaction"] = df[col1] + df[col2]

#     result['species'] = df['species']
#     result['species_label_encoded'] = LabelEncoder().fit_transform(df['species'])
#     ohe = OneHotEncoder(sparse_output=False)
#     ohe_result = ohe.fit_transform(df[['species']])
#     result[ohe.get_feature_names_out(['species'])] = ohe_result

#     save_csv(result, output_path)
#     logger.info(f"✅ Features saved to {output_path}")

# if __name__ == "__main__":
#     generate_features(
#         input_path="data/iris/iris_data.csv",
#         output_path="data/db/features_iris.csv"
#     )


# ml_pipeline/features.py

import pandas as pd
import numpy as np
import os
from itertools import combinations
from sklearn.preprocessing import (
    KBinsDiscretizer, RobustScaler, MaxAbsScaler, MinMaxScaler,
    StandardScaler, LabelEncoder, OneHotEncoder, FunctionTransformer
)
from .utils import get_logger, save_csv

logger = get_logger(__name__)

def generate_features(input_path: str, execution_date: str, output_folder: str):
    # Преобразуем дату
    exec_date = pd.to_datetime(execution_date).date()

    # Читаем симулированный файл
    df = pd.read_csv(input_path, parse_dates=["date"])
    df["date"] = df["date"].dt.date
    df = df[df["date"] == exec_date].copy()

    if df.empty:
        raise ValueError(f"❌ Нет строк для даты {execution_date}")

    logger.info(f"Загружено {df.shape[0]} строк, {df.shape[1]} столбцов для даты {execution_date}")

    numeric_cols = ['sepal_length', 'sepal_width', 'petal_length', 'petal_width']
    result = df[numeric_cols].copy()

    for strategy in ['quantile', 'uniform']:
        kbins = KBinsDiscretizer(n_bins=5, encode='ordinal', strategy=strategy)
        result[[f"{col}_{strategy}_bin" for col in numeric_cols]] = kbins.fit_transform(df[numeric_cols])

    result[[f"{col}_robust_scaled" for col in numeric_cols]] = RobustScaler().fit_transform(df[numeric_cols])
    result[[f"{col}_max_absolute_scaled" for col in numeric_cols]] = MaxAbsScaler().fit_transform(df[numeric_cols])
    result[[f"{col}_max_min_max_scaled" for col in numeric_cols]] = MinMaxScaler((0, 1)).fit_transform(df[numeric_cols])
    result[[f"{col}_logged" for col in numeric_cols]] = FunctionTransformer(np.log1p).fit_transform(df[numeric_cols])
    result[[f"{col}_standardized" for col in numeric_cols]] = StandardScaler().fit_transform(df[numeric_cols])

    for col in numeric_cols:
        result[f"{col}_binarized"] = (df[col] > df[col].median()).astype(int)

    for col1, col2 in combinations(numeric_cols, 2):
        result[f"{col1}_x_{col2}_interaction"] = df[col1] * df[col2]
        result[f"{col1}_plus_{col2}_interaction"] = df[col1] + df[col2]

    result['species'] = df['species']
    result['species_label_encoded'] = LabelEncoder().fit_transform(df['species'])

    ohe = OneHotEncoder(sparse_output=False)
    ohe_result = ohe.fit_transform(df[['species']])
    result[ohe.get_feature_names_out(['species'])] = ohe_result

    # Путь для конкретной даты
    dated_output_dir = os.path.join(output_folder, str(exec_date))
    os.makedirs(dated_output_dir, exist_ok=True)
    output_path = os.path.join(dated_output_dir, "features.csv")

    save_csv(result, output_path)
    logger.info(f"✅ Фичи сохранены в {output_path}")


if __name__ == "__main__":
    import sys
    from datetime import datetime

    execution_date = sys.argv[1] if len(sys.argv) > 1 else datetime.today().date().isoformat()

    # output_folder больше НЕ содержит execution_date — она добавляется внутри функции
    output_folder = "data/db"

    generate_features(
        input_path="data/simulated/iris_simulated.csv",
        output_folder=output_folder,
        execution_date=execution_date
    )


