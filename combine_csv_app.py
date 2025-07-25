import streamlit as st
import pandas as pd
import re

st.title("Timesheet Processor")

st.write("""
Upload multiple CSV timesheet files. This app will:
- Extract the name from each filename and add it as a column.
- Remove rows containing 'Time off' and 'TOTAL' from the main sheet.
- Export 'Time off' and 'TOTAL' rows to separate files.
""")

uploaded_files = st.file_uploader("Upload CSV files", type="csv", accept_multiple_files=True)

def extract_name(filename):
    match = re.search(r"Timesheet_for_(.*?)_\d{4}-\d{2}-\d{2}", filename)
    return match.group(1) if match else "Unknown"

if uploaded_files:
    combined_data = []
    timeoff_data = []
    totals_data = []

    for file in uploaded_files:
        name = extract_name(file.name)
        df = pd.read_csv(file)
        df.insert(0, "Name", name)

        # Extract and store 'Time off' rows
        timeoff_rows = df[df.apply(lambda row: row.astype(str).str.contains("Time off", case=False).any(), axis=1)]
        if not timeoff_rows.empty:
            timeoff_data.append(timeoff_rows)

        # Extract and store 'TOTAL' rows
        total_rows = df[df.apply(lambda row: row.astype(str).str.contains("TOTAL", case=False).any(), axis=1)]
        if not total_rows.empty:
            totals_data.append(total_rows)

        # Remove 'Time off' and 'TOTAL' rows from main data
        df = df[~df.apply(lambda row: row.astype(str).str.contains("TOTAL|Time off", case=False).any(), axis=1)]
        combined_data.append(df)

    # Combine and export
    def convert_df(df):
        return df.to_csv(index=False).encode('utf-8')

    if combined_data:
        combined_df = pd.concat(combined_data, ignore_index=True)
        st.write("Combined Timesheets (excluding 'Time off' and 'TOTAL'):")
        st.dataframe(combined_df.head())
        st.download_button("Download Combined CSV", convert_df(combined_df), "combined_timesheets.csv", "text/csv")

    if timeoff_data:
        timeoff_df = pd.concat(timeoff_data, ignore_index=True)
        st.write("Time Off Entries:")
        st.dataframe(timeoff_df.head())
        st.download_button("Download Time Off CSV", convert_df(timeoff_df), "timeoff.csv", "text/csv")

    if totals_data:
        totals_df = pd.concat(totals_data, ignore_index=True)
        st.write("Total Rows:")
        st.dataframe(totals_df.head())
        st.download_button("Download Totals CSV", convert_df(totals_df), "totals.csv", "text/csv")
