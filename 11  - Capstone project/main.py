import os

from core.dataset_manager import DatasetManager
from core.db_manager import SQLiteDBManager
from app import App

if __name__ == "__main__":
    manager = DatasetManager()
    db_manager = SQLiteDBManager()
    db_manager.run_migration()

    file = 'data/final_prepared_car_dataset.csv'
    # If file not exist run manager
    if not os.path.isfile(file):
        file_path = manager.run()
        db_manager.save_csv_to_db(file_path)

    app = App()
    app.run()