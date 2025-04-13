import sqlite3
import math
from geopy.distance import geodesic


class CityDistanceCalculator:
    R = 6371  # Earth radius in kilometers

    def __init__(self, db_name="cities.db"):
        """Initialize the database connection and ensure the table exists"""
        self.db_name = db_name
        self.conn = sqlite3.connect(self.db_name)
        self.create_database()

    def create_database(self):
        """Create the database table if it doesn't exist"""
        cursor = self.conn.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS city_coordinates (
            city_name TEXT PRIMARY KEY,
            latitude REAL,
            longitude REAL
        )
        """)
        self.conn.commit()

    def get_city_coordinates(self, city_name):
        """Get the coordinates of a city from the database"""
        cursor = self.conn.cursor()
        cursor.execute("SELECT latitude, longitude FROM city_coordinates WHERE city_name = ?", (city_name,))
        result = cursor.fetchone()
        return result

    def insert_city_coordinates(self, city_name, latitude, longitude):
        """Insert the coordinates of a city into the database"""
        cursor = self.conn.cursor()
        cursor.execute("INSERT INTO city_coordinates (city_name, latitude, longitude) VALUES (?, ?, ?)",
                       (city_name, latitude, longitude))
        self.conn.commit()

    def haversine(self, lat1, lon1, lat2, lon2):
        """Calculate the straight-line distance between two points on Earth using the Haversine formula"""
        lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])

        # Haversine formula
        delt_lat = lat2 - lat1
        delt_lon = lon2 - lon1
        a = math.sin(delt_lat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(delt_lon / 2) ** 2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

        # Distance in kilometers
        distance = self.R * c
        return distance

    @staticmethod
    def vincenty(lat1, lon1, lat2, lon2):
        """Calculate the straight-line distance between two points on Earth using the geopy (Vincenty formula)"""
        city1 = (lat1, lon1)
        city2 = (lat2, lon2)

        return geodesic(city1, city2).km

    def get_coordinates(self, city_name):
        """Helper function to get coordinates for a city"""
        city_coordinates = self.get_city_coordinates(city_name)
        lat, lon = None, None
        if city_coordinates is None:
            print(f"Coordinates for {city_name} not found.")
            while True:
                try:
                    lat = float(input(f"Enter the latitude in format XX.XXXX for {city_name}: ").replace(',', '.'))
                    if not -90 <= lat <= 90:
                        print("Invalid latitude. Must be between -90 and 90.")
                        continue
                    break
                except ValueError:
                    print("Invalid input. Please enter a numeric value for latitude.")
                    continue

            while True:
                try:
                    lon = float(input(f"Enter the longitude in format XX.XXXX for {city_name}: ").replace(',', '.'))
                    if not -180 <= lon <= 180:
                        print("Invalid longitude. Must be between -180 and 180.")
                        continue
                    break
                except ValueError:
                    print("Invalid input. Please enter a numeric value for longitude.")
                    continue

            # Insert the city coordinates into the database
            self.insert_city_coordinates(city_name, lat, lon)
        else:
            lat, lon = city_coordinates

        return lat, lon

    def calculate_distance(self):
        """Main method to interact with the user and calculate the distance between two cities"""
        city1 = input("Enter the first city name: ")
        city2 = input("Enter the second city name: ")

        # Get coordinates for both cities using the helper function
        lat1, lon1 = self.get_coordinates(city1)
        lat2, lon2 = self.get_coordinates(city2)

        # Calculate and display the distance
        distance_haversine = self.haversine(lat1, lon1, lat2, lon2)
        distance_vincenty = self.vincenty(lat1, lon1, lat2, lon2)
        print(f"The distance between {city1} and {city2} by Haversine is {distance_haversine:.2f} kilometers.")
        print(f"The distance between {city1} and {city2} by Vincenty is {distance_vincenty:.2f} kilometers.")


# Main execution
if __name__ == "__main__":
    calculator = CityDistanceCalculator()
    calculator.calculate_distance()
