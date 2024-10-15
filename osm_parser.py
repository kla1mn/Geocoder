import sqlite3
import logging
from parsed_object import ParsedObject

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s')


def find_address_by_city_street_house(city: str, street: str, house_number: str, db_name: str, table_name: str) \
        -> tuple[str, str, str, str, float, float, str] | None:
    """Finds an address by city, street and house number."""
    try:
        with sqlite3.connect(db_name) as conn:
            cursor = conn.cursor()
            cursor.execute(f'''
                SELECT city, street, housenumber, postcode, lon, lat, country
                FROM {table_name}
                WHERE city = ? AND street = ? AND housenumber = ?
            ''', (city, street, house_number))

            result = cursor.fetchone()

        if result:
            logging.info(f"Found address for {city}, {street}, {house_number}.")
        else:
            logging.warning(f"No address found for {city}, {street}, {house_number}.")

        return result
    except Exception as e:
        logging.error(f"Error finding address by city, street, and house: {e}")
        return None


def find_address_by_coordinates(lon: float, lat: float, db_name: str, table_name: str) \
        -> tuple[str, str, str, str, float, float, str] | None:
    """Finds an address by coordinates."""
    try:
        with sqlite3.connect(db_name) as conn:
            cursor = conn.cursor()
            cursor.execute(f'''
                SELECT city, street, housenumber, postcode, lon, lat, country
                FROM {table_name}
                WHERE lon = ? AND lat = ?
            ''', (lon, lat))

            result = cursor.fetchone()

        if result:
            logging.info(f"Found address for coordinates: {lon}, {lat}.")
        else:
            logging.warning(f"No address found for coordinates: {lon}, {lat}.")

        return result
    except Exception as e:
        logging.error(f"Error finding address by coordinates: {e}")
        return None


def insert_data(parsed_obj: ParsedObject, db_name: str, table_name: str) -> None:
    """Inserts address data into the database."""
    if _address_exists(parsed_obj, db_name, table_name):
        logging.info(
            f"Address already exists: {parsed_obj.city}, {parsed_obj.street}, {parsed_obj.house_number}. Skipping.")
        return None

    try:
        with sqlite3.connect(db_name) as conn:
            cursor = conn.cursor()
            cursor.execute(f'''
                INSERT INTO {table_name} (city, street, housenumber, postcode, lon, lat, country)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (parsed_obj.city, parsed_obj.street, parsed_obj.house_number,
                  parsed_obj.postcode, parsed_obj.lon, parsed_obj.lat, "Russia"))

        logging.info(f"Inserted address: {parsed_obj.city}, {parsed_obj.street}, {parsed_obj.house_number}.")
    except Exception as e:
        logging.error(f"Error inserting data: {e}")


def _address_exists(parsed_obj: ParsedObject, db_name: str, table_name: str) -> bool:
    """Checks if an address exists in the database."""
    try:
        with sqlite3.connect(db_name) as conn:
            cursor = conn.cursor()
            cursor.execute(f'''
                SELECT 1 FROM {table_name}
                WHERE city = ? AND street = ? AND housenumber = ?
            ''', (parsed_obj.city, parsed_obj.street, parsed_obj.house_number))

            result = cursor.fetchone()
        return result is not None
    except Exception as e:
        logging.error(f"Error checking if address exists: {e}")
        return False


def create_table(db_name: str, table_name: str) -> None:
    """Creates the database and necessary indexes."""
    try:
        with sqlite3.connect(db_name) as conn:
            cursor = conn.cursor()
            cursor.execute(f'''
                CREATE TABLE IF NOT EXISTS {table_name} (
                    city TEXT,
                    street TEXT,
                    housenumber TEXT,
                    postcode TEXT,
                    lon REAL,
                    lat REAL,
                    country TEXT,
                    UNIQUE(city, street, housenumber) 
                )
            ''')
            cursor.execute(
                f'CREATE INDEX IF NOT EXISTS idx_city_street_house ON {table_name} (city, street, housenumber)')
            cursor.execute(f'CREATE INDEX IF NOT EXISTS idx_lon_lat ON {table_name} (lon, lat)')

        logging.info("Database and indexes created successfully.")
    except Exception as e:
        logging.error(f"Error creating database: {e}")
