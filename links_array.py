import csv

csv_file = 'output.csv'

links = []

with open(csv_file, 'r') as file:
    csv_reader = csv.reader(file)
    for row in csv_reader:
        links.extend(row)