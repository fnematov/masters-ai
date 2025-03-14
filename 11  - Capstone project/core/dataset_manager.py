from .dataset_downloader import DatasetDownloader
from .dataset_loader import DatasetLoader
from .dataset_cleaner import DatasetCleaner
from .dataset_processor import DatasetProcessor
import pandas as pd
import os

class DatasetManager:
    """Manages the entire process of downloading, loading, cleaning, and processing datasets."""

    def __init__(self):
        self.column_mapping = {
            "Brand": "make", "Make": "make", "model": "model", "Model": "model", "Year": "year",
            "FuelType": "fuel_type", "Fuel_Type": "fuel_type", "Engine Fuel Type": "fuel_type",
            "Transmission": "transmission_type", "Transmission Type": "transmission_type",
            "Transmission_Type": "transmission_type", "Owner": "owner_type", "Owner_Count": "owner_type",
            "Driven_Wheels": "driven_wheels", "Number of Doors": "number_of_doors", "Doors": "number_of_doors",
            "Market Category": "market_category", "Vehicle Size": "vehicle_size", "Vehicle Style": "vehicle_style",
            "Popularity": "popularity_rate", "Engine HP": "engine_hp", "Engine Cylinders": "engine_cylinders",
            "Engine_Size": "engine_size", "MSRP": "msrp", "Price": "price", "kmDriven": "mileage",
            "Mileage": "mileage", "AdditionInfo": "additional_info",
        }
        self.drop_columns = ["Age", "PostedDate", "AskPrice", "highway MPG", "city mpg"]
        self.columns = [
            "make", "model", "year", "mileage", "transmission_type", "owner_type", "fuel_type", "additional_info",
            "engine_hp", "engine_cylinders", "driven_wheels", "number_of_doors", "market_category", "vehicle_size",
            "vehicle_style", "popularity_rate", "msrp", "engine_size", "price"
        ]

    def run(self):
        # Download datasets
        used_cars_path = DatasetDownloader.download_dataset("mohitkumar282/used-car-dataset")
        car_features_path = DatasetDownloader.download_dataset("CooperUnion/cardataset")
        car_price_path = DatasetDownloader.download_dataset("asinow/car-price-dataset")

        # Load datasets
        used_cars_df = DatasetLoader.load_dataset(used_cars_path, "used_cars_dataset_v2.csv")
        car_features_df = DatasetLoader.load_dataset(car_features_path, "data.csv")
        car_price_df = DatasetLoader.load_dataset(car_price_path, "car_price_dataset.csv")

        # Clean and standardize datasets
        cleaner = DatasetCleaner(self.column_mapping, self.drop_columns)
        used_cars_df = cleaner.clean_and_standardize(used_cars_df)
        car_features_df = cleaner.clean_and_standardize(car_features_df)
        car_price_df = cleaner.clean_and_standardize(car_price_df)

        # Process datasets
        processor = DatasetProcessor(self.columns)
        final_data = []
        processor.process_rows(used_cars_df, car_price_df, car_features_df, final_data)
        processor.process_rows(car_features_df, used_cars_df, car_price_df, final_data)
        processor.process_rows(car_price_df, car_features_df, used_cars_df, final_data)

        # Save the final prepared data
        prepared_dataset = pd.DataFrame(final_data)

        current_dir = os.path.dirname(os.path.abspath(__file__))
        dataset_folder = f"{current_dir}/../data"

        if not os.path.exists(dataset_folder):
            os.makedirs(dataset_folder)

        dataset_file_path = f"{dataset_folder}/final_prepared_car_dataset.csv"

        prepared_dataset.to_csv(dataset_file_path, index=False)

        return dataset_file_path