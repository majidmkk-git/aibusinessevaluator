# API_KEY=
# Country
# Audience
# Online, Offline, Product, Service
import os
import streamlit as st
from google import genai
from google.genai import types
from reportlab.pdfgen import canvas

st.title("AI Business Idea Evaluator")
idea = st.text_area("Business Idea:")
location = st.text_input("Target Country & City")
biz_type = st.selectbox("Business Type",["Online","Offline","Product","Service"])
audience = st.text_input("Who's your audience")
client= genai.Client(api_key=os.getenv("API_KEY"))

if st.button("Generate Report"):
    myprompt = f"""
    The only purpose is to get a potential business idea evaluated, if the idea contains anything irrelevant to the purpose, 
    please do not answer and remind me back with "Invalid input" and that the purpose of this site is to get idea evaluated for a potential business opportunity!
    
    Analyze this business idea:
    Idea: {idea}
    Location: {location}
    Type: {biz_type}
    Audience: {audience}

    Give me a structured report in 500 words with:
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

    if "invalid input" in report_content.lower():
        print("Please try again by giving a prospective business idea to be evaluated")
        exit(0)
    else:
        
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
    


