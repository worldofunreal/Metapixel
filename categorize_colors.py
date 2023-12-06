import csv

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
        return 'Balanced'  # For colors that don't fit clearly into one category




def safe_int(value):
    try:
        return int(value)
    except ValueError:
        return None

input_file = 'Cleaned_Colors.csv'  # Replace with your actual file name
output_file = 'CategorizedColors.csv'

with open(input_file, mode='r', encoding='utf-8') as infile, \
     open(output_file, mode='w', encoding='utf-8', newline='') as outfile:

    reader = csv.DictReader(infile)
    writer = csv.DictWriter(outfile, fieldnames=reader.fieldnames + ['Category'])
    writer.writeheader()

    for row in reader:
        r = safe_int(row['Red'])
        g = safe_int(row['Green'])
        b = safe_int(row['Blue'])

        if r is not None and g is not None and b is not None:
            category = categorize_color(r, g, b)
            row['Category'] = category
            writer.writerow(row)

print("Categorization complete!")
