import streamlit as st
import pandas as pd
from datetime import datetime
from reportlab.platypus import SimpleDocTemplate, Table

# Page Configuration
st.set_page_config(
    page_title="Study Planner Generator",
    page_icon="📚"
)

# Title
st.title("📚 Study Planner Generator")

# Description
st.info(
    "This application helps students create a study plan based on exam dates and available study hours."
)

# Current Date
st.write("📅 Today's Date:", datetime.today().date())

st.write("Enter your subjects, exam dates, and daily study hours.")

# Number of Subjects
num_subjects = st.number_input(
    "Number of Subjects",
    min_value=1,
    max_value=10,
    value=3
)

subjects = []
exam_dates = []

st.subheader("Enter Subject Details")

# Subject Inputs
for i in range(num_subjects):

    subject = st.text_input(
        f"Subject {i+1}",
        key=f"subject_{i}"
    )

    exam_date = st.date_input(
        f"Exam Date for Subject {i+1}",
        key=f"date_{i}"
    )

    subjects.append(subject)
    exam_dates.append(exam_date)

# Study Hours
study_hours = st.number_input(
    "Study Hours Per Day",
    min_value=1,
    max_value=24,
    value=4
)

# Generate Button
if st.button("Generate Study Plan"):

    today = datetime.today().date()

    data = []

    for sub, exam in zip(subjects, exam_dates):

        if sub.strip() != "":

            days_left = (exam - today).days

            if days_left <= 0:
                days_left = 1

            priority = 1 / days_left

            data.append(
                [
                    sub,
                    exam,
                    days_left,
                    priority
                ]
            )

    if len(data) == 0:

        st.error(
            "Please enter at least one subject."
        )

    else:

        df = pd.DataFrame(
            data,
            columns=[
                "Subject",
                "Exam Date",
                "Days Left",
                "Priority"
            ]
        )

        total_priority = df["Priority"].sum()

        df["Study Hours"] = (
            df["Priority"] /
            total_priority
        ) * study_hours

        df["Study Hours"] = df["Study Hours"].round(1)

        df = df.sort_values("Days Left")

        st.subheader("📅 Today's Study Plan")

        display_df = df[
            [
                "Subject",
                "Exam Date",
                "Days Left",
                "Study Hours"
            ]
        ]

        st.dataframe(display_df)

        # PDF Generation
        pdf_file = "study_plan.pdf"

        pdf = SimpleDocTemplate(pdf_file)

        table_data = [display_df.columns.tolist()]

        for row in display_df.values.tolist():
            table_data.append(row)

        table = Table(table_data)

        pdf.build([table])

        with open(pdf_file, "rb") as file:

            st.download_button(
                label="📄 Download Study Plan PDF",
                data=file,
                file_name="study_plan.pdf",
                mime="application/pdf"
            )

        st.success(
            "Study Plan Generated Successfully!"
        )