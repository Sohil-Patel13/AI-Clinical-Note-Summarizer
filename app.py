import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
import os

# Load API key
load_dotenv()

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Page configuration
st.set_page_config(
    page_title="AI Clinical Note Summarizer",
    page_icon="🩺",
    layout="centered"
)

# App title
st.title("🩺 AI Clinical Note Summarizer")

# Description
st.markdown("""
This tool uses AI to summarize clinical notes and identify:

- Key conditions
- Risk factors
- Suggested follow-up actions
""")

# Text area
clinical_note = st.text_area(
    "Paste Clinical Note Below",
    height=250,
    placeholder="Example: 65-year-old male with hypertension..."
)

# Button
if st.button("Generate Summary"):

    if clinical_note.strip() == "":
        st.warning("Please enter a clinical note.")
    else:

        with st.spinner("Analyzing clinical note..."):

            prompt = f"""
            You are a healthcare assistant.

            Analyze the following clinical note.

            Return your response in this format:

            ## Key Conditions
            ## Risk Factors
            ## Suggested Follow-Up

            Clinical Note:
            {clinical_note}
            """

            response = client.chat.completions.create(
                model="gpt-4.1-mini",
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )

            summary = response.choices[0].message.content

        st.success("Analysis Complete")

        st.markdown(summary)