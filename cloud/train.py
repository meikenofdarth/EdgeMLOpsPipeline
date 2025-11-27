# # cloud/train.py

# import pandas as pd
# import numpy as np
# import lightgbm as lgb
# from sklearn.model_selection import train_test_split
# from sklearn.linear_model import LinearRegression
# from sklearn.metrics import mean_squared_error
# import joblib
# import mlflow
# import mlflow.sklearn
# import os
# from datetime import datetime

# # --- Configuration ---
# RAW_DATA_PATH = "data/raw.csv"
# MODEL_DIR = "models"
# MODEL_NAME = "voc_predictor"
# N_LAGS = 5 # Number of past values to use as features

# # --- MLflow Setup ---
# # Set a descriptive experiment name
# mlflow.set_experiment("IoT VOC Prediction")
# mlflow.set_tracking_uri("http://mlflow:5001")

# # --- Feature Engineering ---
# def create_lag_features(df, target_col, n_lags):
#     """Creates columns for previous values of the target variable."""
#     df_lags = df.copy()
#     for i in range(1, n_lags + 1):
#         df_lags[f'{target_col}_lag_{i}'] = df_lags[target_col].shift(i)
#     # Drop rows with NaN values created by shifting
#     df_lags = df_lags.dropna()
#     return df_lags

# # --- Main Training Logic ---
# if __name__ == "__main__":
#     print("Starting model training process...")

#     # 1. Read data
#     try:
#         df = pd.read_csv(RAW_DATA_PATH)
#         # Ensure we have enough data to create features and split
#         if len(df) < N_LAGS + 10:
#             print(f"Not enough data to train. Need at least {N_LAGS + 10} rows, but found {len(df)}.")
#             exit()
#     except FileNotFoundError:
#         print(f"Error: Data file not found at {RAW_DATA_PATH}. Run the publisher first.")
#         exit()

#     # Start an MLflow run to log everything
#     with mlflow.start_run() as run:
#         run_id = run.info.run_id
#         print(f"MLflow Run ID: {run_id}")

#         # 2. Build lag features
#         df_featured = create_lag_features(df, 'voc_ppb', N_LAGS)
#         print(f"Data shape after feature engineering: {df_featured.shape}")

#         # Define features (X) and target (y)
#         features = [f'voc_ppb_lag_{i}' for i in range(1, N_LAGS + 1)]
#         target = 'voc_ppb'
#         X = df_featured[features]
#         y = df_featured[target]

#         # 3. Train simple model using a time-series split
#         # We train on the first 80% and test on the most recent 20%
#         split_index = int(len(X) * 0.8)
#         X_train, X_test = X[:split_index], X[split_index:]
#         y_train, y_test = y[:split_index], y[split_index:]
#         print(f"Train set size: {len(X_train)}, Test set size: {len(X_test)}")

#         # Log parameters
#         mlflow.log_param("n_lags", N_LAGS)
#         mlflow.log_param("train_test_split_ratio", 0.8)

#         # model = LinearRegression()
#         # model.fit(X_train, y_train)
#         # A more powerful, non-linear model
#         model = lgb.LGBMRegressor(random_state=42)
#         model.fit(X_train, y_train)

#         # 4. Evaluate via time-series split, compute RMSE
#         predictions = model.predict(X_test)
#         rmse = np.sqrt(mean_squared_error(y_test, predictions))
#         print(f"Model RMSE on test set: {rmse:.4f}")

#         # Log metrics
#         mlflow.log_metric("rmse", rmse)
#         mlflow.log_param("model_type", model.__class__.__name__)

#         # 5. Save model to models/
#         os.makedirs(MODEL_DIR, exist_ok=True)
#         timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
#         model_filename = f"{MODEL_NAME}-v{timestamp}.joblib"
#         model_path = os.path.join(MODEL_DIR, model_filename)
#         joblib.dump(model, model_path)
#         print(f"Model saved to: {model_path}")

#         # Log the model itself to MLflow for easy retrieval
#         mlflow.sklearn.log_model(model, "model", registered_model_name=MODEL_NAME)

#     print("Training process finished successfully.")



# # cloud/train.py

# import pandas as pd
# import numpy as np
# from sklearn.model_selection import train_test_split
# from sklearn.metrics import mean_squared_error
# import joblib
# import mlflow
# import mlflow.sklearn
# import os
# from datetime import datetime
# import lightgbm as lgb # Make sure lightgbm is imported
# import time

# # --- Configuration ---
# RAW_DATA_PATH = "data/raw.csv"
# MODEL_DIR = "models"
# MODEL_NAME = "voc_predictor"
# N_LAGS = 5

# # --- MLflow Setup ---
# # --- NEW: Add connection retry logic for MLflow ---
# MLFLOW_TRACKING_URI = "http://mlflow:5001"
# mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)
# connected_to_mlflow = False
# while not connected_to_mlflow:
#     try:
#         # A lightweight way to check for connection is to list experiments
#         mlflow.search_experiments()
#         print("Trainer: Connected to MLflow Tracking Server.")
#         connected_to_mlflow = True
#     except Exception as e:
#         print(f"Trainer: MLflow server not ready ({e}). Retrying in 5 seconds...")
#         time.sleep(5)

# mlflow.set_experiment("IoT VOC Prediction")

# # ... (create_lag_features function remains the same) ...
# def create_lag_features(df, target_col, n_lags):
#     df_lags = df.copy()
#     for i in range(1, n_lags + 1):
#         df_lags[f'{target_col}_lag_{i}'] = df_lags[target_col].shift(i)
#     df_lags = df_lags.dropna()
#     return df_lags

# # --- Main Training Logic ---
# if __name__ == "__main__":
#     # ... (The rest of the main function remains the same) ...
#     print("Starting model training process...")
#     try:
#         df = pd.read_csv(RAW_DATA_PATH)
#         if len(df) < N_LAGS + 10:
#             print(f"Not enough data to train. Need at least {N_LAGS + 10} rows, but found {len(df)}.")
#             exit()
#     except FileNotFoundError:
#         print(f"Error: Data file not found at {RAW_DATA_PATH}. Run the publisher first.")
#         exit()

#     with mlflow.start_run() as run:
#         run_id = run.info.run_id
#         print(f"MLflow Run ID: {run_id}")

#         df_featured = create_lag_features(df, 'voc_ppb', N_LAGS)
#         features = [f'voc_ppb_lag_{i}' for i in range(1, N_LAGS + 1)]
#         target = 'voc_ppb'
#         X = df_featured[features]
#         y = df_featured[target]

#         split_index = int(len(X) * 0.8)
#         X_train, X_test = X[:split_index], X[split_index:]
#         y_train, y_test = y[:split_index], y[split_index:]

#         mlflow.log_param("n_lags", N_LAGS)
#         mlflow.log_param("train_test_split_ratio", 0.8)

#         model = lgb.LGBMRegressor(random_state=42)
#         model.fit(X_train, y_train)

#         predictions = model.predict(X_test)
#         rmse = np.sqrt(mean_squared_error(y_test, predictions))
#         print(f"Model RMSE on test set: {rmse:.4f}")

#         mlflow.log_metric("rmse", rmse)
#         mlflow.log_param("model_type", model.__class__.__name__)

#         os.makedirs(MODEL_DIR, exist_ok=True)
#         timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
#         model_filename = f"{MODEL_NAME}-v{timestamp}.joblib"
#         model_path = os.path.join(MODEL_DIR, model_filename)
#         joblib.dump(model, model_path)
#         print(f"Model saved to: {model_path}")

#         mlflow.sklearn.log_model(model, "model", registered_model_name=MODEL_NAME)
#     print("Training process finished successfully.")


# cloud/train.py

import pandas as pd
import numpy as np
from sklearn.metrics import mean_squared_error
import joblib
import mlflow
import mlflow.sklearn
import os
from datetime import datetime
import lightgbm as lgb
import time

# --- Configuration ---
RAW_DATA_PATH = "data/raw.csv"
MODEL_DIR = "models"
MODEL_NAME = "voc_predictor"
N_LAGS = 5

# --- MLflow Setup ---
MLFLOW_TRACKING_URI = "http://mlflow:5001"
mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)
connected_to_mlflow = False
while not connected_to_mlflow:
    try:
        mlflow.search_experiments()
        print("Trainer: Connected to MLflow Tracking Server.")
        connected_to_mlflow = True
    except Exception as e:
        print(f"Trainer: MLflow server not ready ({e}). Retrying in 5 seconds...")
        time.sleep(5)

mlflow.set_experiment("IoT VOC Prediction")

def create_lag_features(df, target_col, n_lags):
    df_lags = df.copy()
    for i in range(1, n_lags + 1):
        df_lags[f'{target_col}_lag_{i}'] = df_lags[target_col].shift(i)
    df_lags = df_lags.dropna()
    return df_lags

# --- Main Training Logic ---
if __name__ == "__main__":
    print("Starting model training process...")
    try:
        df = pd.read_csv(RAW_DATA_PATH)
        if len(df) < N_LAGS + 10:
            print(f"Not enough data to train. Need at least {N_LAGS + 10} rows, but found {len(df)}.")
            exit()
    except FileNotFoundError:
        print(f"Error: Data file not found at {RAW_DATA_PATH}. Run the publisher first.")
        exit()

    with mlflow.start_run() as run:
        run_id = run.info.run_id
        print(f"MLflow Run ID: {run_id}")

        df_featured = create_lag_features(df, 'voc_ppb', N_LAGS)
        features = [f'voc_ppb_lag_{i}' for i in range(1, N_LAGS + 1)]
        target = 'voc_ppb'
        X = df_featured[features]
        y = df_featured[target]

        split_index = int(len(X) * 0.8)
        X_train, X_test = X[:split_index], X[split_index:]
        y_train, y_test = y[:split_index], y[split_index:]

        mlflow.log_param("n_lags", N_LAGS)
        mlflow.log_param("train_test_split_ratio", 0.8)

        model = lgb.LGBMRegressor(random_state=42)
        model.fit(X_train, y_train)

        predictions = model.predict(X_test)
        rmse = np.sqrt(mean_squared_error(y_test, predictions))
        print(f"Model RMSE on test set: {rmse:.4f}")

        mlflow.log_metric("rmse", rmse)
        mlflow.log_param("model_type", model.__class__.__name__)

        os.makedirs(MODEL_DIR, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        model_filename = f"{MODEL_NAME}-v{timestamp}.joblib"
        model_path = os.path.join(MODEL_DIR, model_filename)
        joblib.dump(model, model_path)
        print(f"Model saved to: {model_path}")

        mlflow.sklearn.log_model(model, "model", registered_model_name=MODEL_NAME)
    print("Training process finished successfully.")