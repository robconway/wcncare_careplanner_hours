import streamlit as st
import pandas as pd
import re

st.title("CSV Combiner with Name Extraction and Row Filtering")

st.write("""
Upload multiple CSV timesheet files. The app will:
- Extract the name from each filename and add it as the first column.
- Remove rows containing the word 'TOTAL' or 'Time off' from the main CSV.
- Move 'Time off' rows to a separate CSV file.
- Move 'TOTAL' rows to another separate CSV file.
""")

uploaded_files = st.file_uploader("Choose CSV files", type="csv", accept_multiple_files=True)

def extract_name(filename):
    match = re.search(r"Timesheet_for_(.*?)_\d{4}-\d{2}-\d{2}", filename)
    return match.group(1) if match else "Unknown"

if uploaded_files:
    combined_data = []
    timeoff_data = []
    total_data = []

    for file in uploaded_files:
        name = extract_name(file.name)
        df = pd.read_csv(file)

        # Add name column
        df.insert(0, "Name", name)

        # Extract 'Time off' rows
        timeoff_rows = df[df.apply(lambda row: row.astype(str).str.contains("Time off", case=False).any(), axis=1)]
        if not timeoff_rows.empty:
            timeoff_data.append(timeoff_rows)

        # Extract 'TOTAL' rows
        total_rows = df[df.apply(lambda row: row.astype(str).str.contains("TOTAL", case=False).any(), axis=1)]
        if not total_rows.empty:
            total_data.append(total_rows)

        # Remove 'Time off' and 'TOTAL' rows from main data
        df = df[~df.apply(lambda row: row.astype(str).str.contains("TOTAL|Time off", case=False).any(), axis=1)]

       
