import pandas as pd

class DatasetLoader:
    """Handles loading of datasets into pandas DataFrames."""

    @staticmethod
    def load_dataset(path, file_name):
        return pd.read_csv(f"{path}/{file_name}")