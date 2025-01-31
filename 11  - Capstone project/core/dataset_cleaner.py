
class DatasetCleaner:
    """Handles cleaning and standardizing of datasets."""

    def __init__(self, column_mapping, drop_columns):
        self.column_mapping = column_mapping
        self.drop_columns = drop_columns

    def clean_and_standardize(self, df):
        df = df.rename(columns=self.column_mapping)
        df = df.drop(columns=[col for col in self.drop_columns if col in df.columns], errors="ignore")
        return df