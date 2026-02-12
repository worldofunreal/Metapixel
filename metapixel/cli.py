import argparse
import sys
import json
import csv
from .core import Metapixel
from .viz import create_palette_image, create_comparison

def main():
    parser = argparse.ArgumentParser(description="Metapixel: Extract dominant colors from images.")
    parser.add_argument("image", help="Path to the input image.")
    parser.add_argument("-k", "--colors", type=int, default=5, help="Number of dominant colors to extract.")
    parser.add_argument("-o", "--output", choices=["json", "csv", "text"], default="text", help="Output format.")
    parser.add_argument("-v", "--visualize", action="store_true", help="Generate a visualization image.")
    
    args = parser.parse_args()

    try:
        mp = Metapixel()
        colors = mp.extract(args.image, k=args.colors)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

    if args.output == "json":
        output = [
            {"rgb": rgb, "category": cat, "name": name}
            for rgb, cat, name in colors
        ]
        print(json.dumps(output, indent=2))
    elif args.output == "csv":
        writer = csv.writer(sys.stdout)
        writer.writerow(["Red", "Green", "Blue", "Category", "Name"])
        for (r, g, b), cat, name in colors:
            writer.writerow([r, g, b, cat, name])
    else:
        print(f"Dominant colors for {args.image}:")
        for (r, g, b), cat, name in colors:
            print(f"RGB: ({r}, {g}, {b}) | Category: {cat} | Closest Name: {name}")

    if args.visualize:
        output_viz = "metapixel_viz.png"
        create_comparison(args.image, colors, output_viz)
        
if __name__ == "__main__":
    main()
