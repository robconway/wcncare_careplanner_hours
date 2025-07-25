import streamlit as st
import pandas as pd
from io import BytesIO

st.title("CSV Combiner")

st.write("Upload multiple CSV files to combine them into one.")

uploaded_files = st.file_uploader("Choose CSV files", type="csv", accept_multiple_files=True)

if uploaded_files:
    combined_df = pd.concat([pd.read_csv(file) for file in uploaded_files], ignore_index=True)
    
    st.write("Preview of Combined Data:")
    st.dataframe(combined_df.head())

    # Convert to CSV for download
    def convert_df(df):
        return df.to_csv(index=False).encode('utf-8')

    csv_data = convert_df(combined_df)

    st.download_button(
        label="Download Combined CSV",
        data=csv_data,
        file_name="combined.csv",
        mime="text/csv"
    )
