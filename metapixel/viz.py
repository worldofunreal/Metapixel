import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

def create_palette_image(colors, width=500, height=100):
    """
    Creates a horizontal strip of the given colors.
    colors: List of (rgb_tuple, category, name)
    """
    if not colors:
        return None
        
    swatch_width = width // len(colors)
    palette = Image.new('RGB', (width, height))
    draw = ImageDraw.Draw(palette)
    
    for i, (rgb, category, name) in enumerate(colors):
        x0 = i * swatch_width
        x1 = (i + 1) * swatch_width
        draw.rectangle([x0, 0, x1, height], fill=rgb)
        
    return palette

def create_comparison(image_path, colors, output_path):
    """
    Creates a comparison image with the original image and the palette below it.
    """
    # Load original image using PIL
    original = Image.open(image_path)
    
    # Create palette with same width as original
    palette_height = int(original.height * 0.2) # 20% of original height
    palette = create_palette_image(colors, width=original.width, height=palette_height)
    
    # Combine
    total_height = original.height + palette.height
    combined = Image.new('RGB', (original.width, total_height))
    combined.paste(original, (0, 0))
    combined.paste(palette, (0, original.height))
    
    combined.save(output_path)
    print(f"Visualization saved to {output_path}")
