import streamlit as st
import pandas as pd
import re
from io import BytesIO

st.title("Enhanced CSV Combiner with Name Extraction")

st.write("Upload multiple CSV timesheet files. The app will extract the name from each filename and add it as the first column in the combined CSV.")

uploaded_files = st.file_uploader("Choose CSV files", type="csv", accept_multiple_files=True)

def extract_name(filename):
    match = re.search(r"Timesheet_for_(.*?)_\d{4}-\d{2}-\d{2}", filename)
    return match.group(1) if match else "Unknown"

if uploaded_files:
    combined_data = []

    for file in uploaded_files:
        name = extract_name(file.name)
        df = pd.read_csv(file)
        df.insert(0, "Name", name)
        combined_data.append(df)

    combined_df = pd.concat(combined_data, ignore_index=True)

    st.write("Preview of Combined Data:")
    st.dataframe(combined_df.head())

    def convert_df(df):
        return df.to_csv(index=False).encode('utf-8')

    csv_data = convert_df(combined_df)

    st.download_button(
        label="Download Combined CSV",
        data=csv_data,
        file_name="combined_timesheets.csv",
        mime="text/csv"
    )
