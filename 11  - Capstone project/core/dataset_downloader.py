import kagglehub

class DatasetDownloader:
    """Handles downloading of datasets from Kaggle."""

    @staticmethod
    def download_dataset(dataset_identifier):
        return kagglehub.dataset_download(dataset_identifier)