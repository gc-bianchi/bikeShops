import csv
import glob

# List of CSV files to be combined
csv_files = glob.glob("done/email_batch*.csv")

combined_emails = []

# Read emails from each CSV file
for file in csv_files:
    with open(file, "r") as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # Skip header row
        for row in reader:
            combined_emails.append(row[0])

# Write combined emails to a new CSV file
combined_filename = "combined_emails.csv"
with open(combined_filename, "w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["email"])
    writer.writerows([[email] for email in combined_emails])

print("Combined CSV file saved successfully.")
