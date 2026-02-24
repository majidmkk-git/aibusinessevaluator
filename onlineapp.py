# API_KEY=
# Country
# Audience
# Online, Offline, Product, Service

import streamlit as st
from google import genai
from google.genai import types
import os
from reportlab.pdfgen import canvas

st.title("AI Business Idea validator")

idea = st.text_area("Business Idea:")

location = st.text_input("Target Country & City")

biz_type = st.selectbox("Business Type",["Online","Offline","Product","Service"])

audience = st.text_input("Who's your audience")

client= genai.Client(api_key="AIzaSyBJqzUI6KcnKuvtk4K7su41vNaywY7GnYU")

if st.button("Generate Report"):
    myprompt = f"""
    Analyze this business idea:
    Idea: {idea}
    Location: {location}
    Type: {biz_type}
    Audience: {audience}

    Give me a structured report with:
    1. Overview
    2. Market Analysis
    3. Revenue possibility
    4. Funding options
    5. Competitor Analysis
"""
    answer = client.models.generate_content(
                contents = myprompt,
                model = "gemini-3-flash-preview"
                )
    st.subheader("AI Analysis")
    st.write(answer.text)
    report_content = answer.text

    pdffile="output.pdf"

    c = canvas.Canvas(pdffile)

    c.setFont("Helvetica",12)

    y = 800

    for line in report_content.split("\n"):
        c.drawString(30,y,line)
        y = y -15
        if y < 50:
            c.showPage()
            y = 800

    c.save()

    with open(pdffile,"rb") as file:
        st.download_button(label="Download Report",
             data = file,
             file_name="Business Analysis Report.pdf")
    


