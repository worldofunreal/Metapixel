import cv2
import numpy as np
import csv
import os
from pathlib import Path

class Metapixel:
    def __init__(self, color_db_path=None):
        if color_db_path is None:
            # Default to bundled colors.csv
            color_db_path = Path(__file__).parent / "colors.csv"
        
        self.color_database = self._load_color_database(color_db_path)

    def _load_color_database(self, csv_path):
        color_database = {}
        try:
            with open(csv_path, mode='r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    red, green, blue = int(row['Red']), int(row['Green']), int(row['Blue'])
                    color_database[(red, green, blue)] = row['Name']
        except FileNotFoundError:
            print(f"Warning: Color database not found at {csv_path}")
        return color_database

    def extract(self, image_path, k=5):
        """
        Extracts dominant colors from an image using K-Means clustering.
        Returns a list of tuples: (rgb_tuple, category, color_name)
        """
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Image not found: {image_path}")

        image = cv2.imread(image_path)
        if image is None:
            raise ValueError(f"Failed to load image: {image_path}")
            
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        pixel_values = image.reshape((-1, 3))
        pixel_values = np.float32(pixel_values)

        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 0.2)
        _, labels, centers = cv2.kmeans(pixel_values, k, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)
        centers = np.uint8(centers)

        results = []
        for color in centers:
            r, g, b = int(color[0]), int(color[1]), int(color[2])
            category = self.categorize_color(r, g, b)
            color_name = self.find_closest_color_name((r, g, b))
            results.append(((r, g, b), category, color_name))
            
        return results

    def categorize_color(self, r, g, b):
        max_color = max(r, g, b)
        
        if r == max_color and g < r and b < r:
            return 'Red' if g >= b else 'Pink'
        elif g == max_color and r < g and b < g:
            return 'Green' if r >= b else 'Aquamarine'
        elif b == max_color and r < b and g < b:
            return 'Blue' if r >= g else 'Azure'
        elif r == max_color and g == max_color:
            return 'Yellow' if b < r else 'Lime'
        elif g == max_color and b == max_color:
            return 'Cyan' if r < g else 'Aquamarine'
        elif r == max_color and b == max_color:
            return 'Magenta' if g < r else 'Purple'
        elif r > g and g > b:
            return 'Orange'
        elif g > r and r > b:
            return 'Lime'
        elif g > b and b > r:
            return 'Aquamarine'
        elif b > g and g > r:
            return 'Azure'
        elif b > r and r > g:
            return 'Purple'
        elif r > b and b > g:
            return 'Pink'
        else:
            return 'Balanced'

    def find_closest_color_name(self, rgb):
        r, g, b = rgb
        min_distance = float('inf')
        closest_color_name = "Unknown"

        for db_rgb, name in self.color_database.items():
            distance = sum((c1 - c2) ** 2 for c1, c2 in zip(rgb, db_rgb))
            if distance < min_distance:
                min_distance = distance
                closest_color_name = name

        return closest_color_name
