import csv

input_file = 'Color.csv'  # Replace with your actual file name
output_file = 'Cleaned_Colors.csv'

with open(input_file, mode='r', encoding='utf-8') as infile, \
     open(output_file, mode='w', encoding='utf-8', newline='') as outfile:

    reader = csv.DictReader(infile)
    writer = csv.writer(outfile)

    # Write header for the new CSV
    writer.writerow(['Name', 'Red', 'Green', 'Blue'])

    for row in reader:
        name = row['name']
        red = row['redDecimal']
        green = row['greenDecimal']
        blue = row['blueDecimal']

        writer.writerow([name, red, green, blue])

print("File cleaned and saved as:", output_file)
