import os
import shutil
from PIL import Image

# Define the source directory containing the images
source_directory = '/home/bizkit/Downloads/MJ/'

# Define the destination directories for each aspect ratio
aspect_ratio_directories = {
    '16:9': '/home/bizkit/Downloads/MJ/16_9',
    '1:1': '/home/bizkit/Downloads/MJ/1_1',
    '9:16': '/home/bizkit/Downloads/MJ/9_16',
    '16:6': '/home/bizkit/Downloads/MJ/16_6',
    '4:3': '/home/bizkit/Downloads/MJ/4_3',
    # Add more aspect ratios and destination directories as needed
}

# Create the destination directories if they don't exist
for directory in aspect_ratio_directories.values():
    os.makedirs(directory, exist_ok=True)

# Function to determine the aspect ratio of an image
def get_aspect_ratio(image_path):
    with Image.open(image_path) as img:
        exif_data = img._getexif()
        if exif_data:
            for tag, value in exif_data.items():
                if tag == 274:  # Exif tag for orientation
                    if value == 6 or value == 8:  # Landscape orientations
                        return '16:9'
                    elif value == 3 or value == 1:  # Portrait orientations
                        return '9:16'
        return '1:1'  # Default to 1:1 if no orientation data is found

# Loop through the images in the source directory
for filename in os.listdir(source_directory):
    if filename.endswith(('.jpg', '.jpeg', '.png', '.gif', '.bmp')):
        image_path = os.path.join(source_directory, filename)
        aspect_ratio = get_aspect_ratio(image_path)
        
        # Categorize the image based on aspect ratio
        destination = aspect_ratio_directories.get(aspect_ratio)
        if destination:
            # Move the image to the appropriate destination directory
            shutil.move(image_path, os.path.join(destination, filename))
        else:
            print(f"Image '{filename}' was not categorized.")

print("Images categorized successfully.")
