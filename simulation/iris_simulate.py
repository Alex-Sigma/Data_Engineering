import pandas as pd
import numpy as np

def simulate_iris_with_bootstrap(input_path: str, output_path: str, dates: list[str], samples_per_date: int = 100):
    df = pd.read_csv(input_path)
    df_shuffled = df.sample(frac=1, random_state=42).reset_index(drop=True)

    result_frames = []
    for date in dates:
        # Бутстрэппинг с сохранением статистики
        part = df_shuffled.sample(n=samples_per_date, replace=True, random_state=hash(date) % 2**32).copy()
        part["date"] = date
        result_frames.append(part)

    result_df = pd.concat(result_frames).reset_index(drop=True)
    result_df.to_csv(output_path, index=False)
    print(f"✅ Bootstrapped iris data saved to {output_path} with {samples_per_date} samples per date.")

# Пример использования
if __name__ == "__main__":
    simulate_iris_with_bootstrap(
        input_path="data/iris/iris_data.csv",
        output_path="data/simulated/iris_simulated.csv",
        dates=["2025-06-14", "2025-06-15", "2025-06-16"],
        samples_per_date=150  # теперь для каждой даты будет 150 строк
    )

