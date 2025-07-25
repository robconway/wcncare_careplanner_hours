import streamlit as st
import pandas as pd
import re

st.title("Enhanced CSV Combiner with Name Extraction and Filtering")

st.write("""
Upload multiple CSV timesheet files. The app will:
- Extract the name from each filename and add it as the first column.
- Remove rows containing the word 'TOTAL'.
- Move rows containing 'Time off' to a separate CSV file.
""")

uploaded_files = st.file_uploader("Choose CSV files", type="csv", accept_multiple_files=True)

def extract_name(filename):
    match = re.search(r"Timesheet_for_(.*?)_\d{4}-\d{2}-\d{2}", filename)
    return match.group(1) if match else "Unknown"

if uploaded_files:
    combined_data = []
    timeoff_data = []

    for file in uploaded_files:
        name = extract_name(file.name)
        df = pd.read_csv(file)

        # Add name column
        df.insert(0, "Name", name)

        # Extract time off rows
        timeoff_rows = df[df.apply(lambda row: row.astype(str).str.contains("Time off", case=False).any(), axis=1)]
        if not timeoff_rows.empty:
            timeoff_data.append(timeoff_rows)

        # Remove rows containing 'TOTAL' or 'Time off'
        df = df[~df.apply(lambda row: row.astype(str).str.contains("TOTAL|Time off", case=False).any(), axis=1)]

        combined_data.append(df)

    combined_df = pd.concat(combined_data, ignore_index=True)

    st.write("Preview of Combined Data (excluding 'TOTAL' and 'Time off' rows):")
    st.dataframe(combined_df.head())

    def convert_df(df):
        return df.to_csv(index=False).encode('utf-8')

    csv_combined = convert_df(combined_df)

    st.download_button(
        label="Download Combined CSV",
        data=csv_combined,
        file_name="combined_timesheets.csv",
        mime="text/csv"
    )

    if timeoff_data:
        timeoff_df = pd.concat(timeoff_data, ignore_index=True)
        csv_timeoff = convert_df(timeoff_df)

        st.download_button(
            label="Download Time Off CSV",
            data=csv_timeoff,
            file_name="timeoff.csv",
            mime="text/csv"
        )
