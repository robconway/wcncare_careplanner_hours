import streamlit as st
import fitz  # PyMuPDF
import csv
import re
import io

st.title("Shift Extractor from Timesheets PDF")

uploaded_file = st.file_uploader("Upload a timesheet PDF", type="pdf")

if uploaded_file:
    doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
    pages_text = [page.get_text() for page in doc]

    records = []
    carer_name = ""

    carer_pattern = re.compile(r"Mr\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)")
    shift_pattern = re.compile(
        r"(?P<date>\d{2}/\d{2}/\d{4})\s+"
        r"(?P<start>\d{2}:\d{2})\s+"
        r"(?P<end>\d{2}:\d{2})\s+"
        r"(?P<duration>\d{2}:\d{2})\s+"
        r"(?P<rate>[A-Za-z]+(?:\s+[A-Za-z]+)?)\s+"
        r"(?P<description>Dom|Home)\s+"
        r"£[\d,.]+\s+£[\d,.]+\s+(.*?)"
    )

    for page_text in pages_text:
        carer_match = carer_pattern.search(page_text)
        if carer_match:
            carer_name = carer_match.group(1)

        normalized_text = re.sub(r'\s+', ' ', page_text)

        for match in shift_pattern.finditer(normalized_text):
            date = match.group("date")
            duration = match.group("duration")
            rate_description = f"{match.group('rate')} {match.group('description')}"
            records.append([carer_name, date, duration, rate_description])

    if records:
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(["carer_name", "date", "duration", "rate_description"])
        writer.writerows(records)

        st.success(f"Extracted {len(records)} shift records.")
        st.download_button(
            label="Download CSV",
            data=output.getvalue(),
            file_name="shifts_without_clients.csv",
            mime="text/csv"
        )
    else:
        st.warning("No shift records found in the uploaded PDF.")
