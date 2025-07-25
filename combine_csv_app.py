import pandas as pd
import re

# Load the uploaded CSV file
file_path = "Timesheet_for_Norma Zhonga_2025-06-25_2025-07-24.csv"
df = pd.read_csv(file_path)

# Extract name from filename
match = re.search(r"Timesheet_for_(.*?)_\d{4}-\d{2}-\d{2}", file_path)
name = match.group(1) if match else "Unknown"

# Add name column
df.insert(0, "Name", name)

# Identify rows containing 'Time off'
timeoff_df = df[df.apply(lambda row: row.astype(str).str.contains("Time off", case=False).any(), axis=1)]

# Identify rows containing 'TOTAL'
totals_df = df[df.apply(lambda row: row.astype(str).str.contains("TOTAL", case=False).any(), axis=1)]

# Remove 'Time off' and 'TOTAL' rows from main dataframe
combined_df = df[~df.apply(lambda row: row.astype(str).str.contains("TOTAL|Time off", case=False).any(), axis=1)]

# Save the dataframes to separate CSV files
combined_df.to_csv("combined_timesheets.csv", index=False)
timeoff_df.to_csv("timeoff.csv", index=False)
totals_df.to_csv("totals.csv", index=False)

print("Files created: combined_timesheets.csv, timeoff.csv, totals.csv")
