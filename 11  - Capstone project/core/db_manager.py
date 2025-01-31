import pandas as pd
import sqlite3
import streamlit as st

class SQLiteDBManager:
    def __init__(self):
        self.db_path = "car_data.db"

    def save_csv_to_db(self, csv_path: str):
        """Reads CSV and saves it into the SQLite database"""
        try:
            df = pd.read_csv(csv_path)

            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            # ✅ Get column names from database (excluding 'id')
            cursor.execute("PRAGMA table_info(available_cars);")
            db_columns = [row[1] for row in cursor.fetchall() if row[1] != "id"]

            # ✅ Ensure only matching columns are inserted
            df = df[db_columns]  # Keep only columns that exist in the database

            # ✅ Dynamically construct the INSERT query (excluding 'id')
            columns = ", ".join(db_columns)
            placeholders = ", ".join(["?" for _ in db_columns])
            insert_query = f"INSERT INTO available_cars ({columns}) VALUES ({placeholders})"

            # ✅ Convert DataFrame to list of tuples for bulk insertion
            data = [tuple(row) for row in df.itertuples(index=False, name=None)]

            # ✅ Insert records while allowing SQLite to auto-generate IDs
            cursor.executemany(insert_query, data)

            conn.commit()
            conn.close()
        except Exception as e:
            st.error(f"Error saving CSV to DB: {e}")

    def fetch_top_rated_cars(self, limit=10):
        """Fetches the top-rated cars from the database"""
        try:
            conn = sqlite3.connect(self.db_path)
            query = f"""
            SELECT id, make, model, year, (make || ' ' || model || ' ' || year) AS car_name, MAX(popularity_rate) AS rating
            FROM available_cars
            GROUP BY make
            ORDER BY rating DESC
            LIMIT {limit}
            """
            df = pd.read_sql(query, conn)
            conn.close()
            return df
        except Exception as e:
            print(f"Database Error: {e}")
            return None

    def get_top_ordered_cars(self):
        """Fetches the top-rated cars from the database"""
        try:
            conn = sqlite3.connect(self.db_path)
            query = """
            select (make || ' ' || model || ' ' || year) as car_name, count(car_id) as total_orders
            from orders
            join available_cars on orders.car_id = available_cars.id
            group by car_id
            order by total_orders desc
            limit 5
            """
            df = pd.read_sql(query, conn)
            conn.close()
            return df
        except Exception as e:
            print(f"Database Error: {e}")
            return None

    def create_order(self, car_id: int, first_name: str, last_name: str, phone_number: str, email: str):
        """Fetches the top-rated cars from the database"""
        try:
            conn = sqlite3.connect(self.db_path)
            query = f"""
            INSERT INTO orders (car_id, first_name, last_name, phone_number, email)
            VALUES (?, ?, ?, ?, ?)
            """
            cursor = conn.cursor()
            cursor.execute(query, (car_id, first_name, last_name, phone_number, email))
            conn.commit()
            conn.close()
        except Exception as e:
            print(f"Database Error: {e}")
            return None

    def fetch_cars(self, make: str = None, model: str = None, year_from: int = None, year_to: int = None, mileage_from: int = None, mileage_to: int = None, transmission_type: str = None, fuel_type: str = None, msrp_from: int = None, msrp_to: int = None):
        """Fetch cars from the database based on filters."""

        query = f"SELECT make, model, year, mileage, transmission_type, fuel_type, msrp FROM available_cars WHERE 1=1"
        query_params = []

        if make:
            query += " AND LOWER(make) LIKE LOWER(?)"
            query_params.append(f"%{make}%")

        if model:
            query += " AND LOWER(model) LIKE LOWER(?)"
            query_params.append(f"%{model}%")

        if year_from and year_to:
            query += " AND year BETWEEN ? AND ?"
            query_params.extend([year_from, year_to])

        if mileage_from and mileage_to:
            query += " AND mileage BETWEEN ? AND ?"
            query_params.extend([mileage_from, mileage_to])

        if transmission_type:
            query += " AND LOWER(transmission_type) LIKE LOWER(?)"
            query_params.append(f"%{transmission_type}%")

        if fuel_type:
            query += " AND LOWER(fuel_type) LIKE LOWER(?)"
            query_params.append(f"%{fuel_type}%")

        if msrp_from and msrp_to:
            query += " AND msrp BETWEEN ? AND ?"
            query_params.extend([msrp_from, msrp_to])

        query += " LIMIT ?"
        query_params.append(5)

        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute(query, tuple(query_params))
                rows = cursor.fetchall()

            return [dict(zip(["id", "make", "model", "year", "mileage", "transmission_type", "fuel_type", "msrp"], row)) for
                    row in rows]

        except sqlite3.Error as e:
            print(f"🚨 Database error: {e}")
            return []


    def load_data(self):
        """Loads data from SQLite database"""
        try:
            conn = sqlite3.connect(self.db_path)
            df = pd.read_sql(f"SELECT * FROM available_cars", conn)
            conn.close()
            return df
        except Exception as e:
            st.error(f"Error loading data from DB: {e}")
            return None

    def run_migration(self):
        """Runs the database migration to create the necessary tables"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("""
            create table if not exists available_cars
                (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    make              TEXT,
                    model             TEXT,
                    year              INTEGER,
                    mileage           TEXT,
                    transmission_type TEXT,
                    owner_type        TEXT,
                    fuel_type         TEXT,
                    additional_info   TEXT,
                    engine_size       REAL,
                    number_of_doors   REAL,
                    price             REAL,
                    engine_hp         REAL,
                    engine_cylinders  REAL,
                    driven_wheels     TEXT,
                    market_category   TEXT,
                    vehicle_size      TEXT,
                    vehicle_style     TEXT,
                    popularity_rate   REAL,
                    msrp              REAL
                );
            """)
            cursor.execute("""
                    CREATE TABLE IF NOT EXISTS orders (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        car_id INTEGER,
                        first_name TEXT,
                        last_name TEXT,
                        phone_number TEXT,
                        email TEXT
                    )
            """)
            conn.commit()
            conn.close()
        except Exception as e:
            st.error(f"Error running migration: {e}")