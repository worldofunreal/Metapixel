import cv2
import numpy as np
import csv
import sys

# Function to load the color database from a CSV file
def load_color_database(csv_path):
    color_database = {}
    with open(csv_path, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            red, green, blue = int(row['Red']), int(row['Green']), int(row['Blue'])
            color_database[(red, green, blue)] = row['Name']
    return color_database

# Color categorization function
def categorize_color(r, g, b):
    max_color = max(r, g, b)
    min_color = min(r, g, b)
    
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

# Function to find the closest color name from the database
def find_closest_color_name(rgb, color_database):
    r, g, b = rgb
    min_distance = float('inf')
    closest_color_name = None

    for db_rgb, name in color_database.items():
        distance = sum((c1 - c2) ** 2 for c1, c2 in zip(rgb, db_rgb))
        if distance < min_distance:
            min_distance = distance
            closest_color_name = name

    return closest_color_name

# Function to find dominant colors in an image
def find_dominant_colors(image_path, k=3):
    image = cv2.imread(image_path)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    pixel_values = image.reshape((-1, 3))
    pixel_values = np.float32(pixel_values)

    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 0.2)
    _, labels, centers = cv2.kmeans(pixel_values, k, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)
    centers = np.uint8(centers)

    return centers

if __name__ == "__main__":
    color_db = load_color_database("CategorizedColors.csv")
    image_path = sys.argv[1] if len(sys.argv) > 1 else "totem1.png"
    dominant_colors = find_dominant_colors(image_path, k=3)

    print("Dominant colors are:")
    for color in dominant_colors:
        r, g, b = color
        category = categorize_color(r, g, b)
        color_name = find_closest_color_name((r, g, b), color_db)
        print(f"RGB: {color}, Category: {category}, Closest Color Name: {color_name}")