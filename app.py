import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Configure page
st.set_page_config(
    page_title="AI Clinical Note Summarizer",
    page_icon="🩺",
    layout="centered"
)

# App title
st.title("🩺 AI Clinical Note Summarizer")

# Description
st.markdown("""
This AI-powered healthcare tool summarizes clinical notes and identifies:

- Key conditions
- Risk factors
- Suggested follow-up actions
- Severity level
""")

# Text input
clinical_note = st.text_area(
    "Paste Clinical Note Below",
    height=250,
    placeholder="Example: 72-year-old patient with hypertension and diabetes..."
)

# Generate button
if st.button("Generate Summary"):

    # Empty input protection
    if clinical_note.strip() == "":
        st.warning("Please enter a clinical note.")

    else:

        # Loading spinner
        with st.spinner("Analyzing clinical note..."):

            prompt = f"""
            You are an AI healthcare assistant helping summarize clinical notes.

            Analyze the clinical note below.

            Return your response using EXACTLY this format:

            ## Key Conditions
            - Bullet points only

            ## Risk Factors
            - Bullet points only

            ## Suggested Follow-Up
            - Bullet points only

            ## Severity Level
            Choose ONE:
            - Low
            - Moderate
            - High

            Keep the response concise and professional.

            Clinical Note:
            {clinical_note}
            """

            # OpenAI API request
            response = client.chat.completions.create(
                model="gpt-4.1-mini",
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )

            # Extract AI response
            summary = response.choices[0].message.content

        # Success message
        st.success("Analysis Complete")

        # Display summary
        st.markdown(summary)

        # Severity indicators
        if "High" in summary:
            st.error("Severity Level: HIGH")

        elif "Moderate" in summary:
            st.warning("Severity Level: MODERATE")

        elif "Low" in summary:
            st.success("Severity Level: LOW")