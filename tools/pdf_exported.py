from fpdf import FPDF
import os

def save_to_pdf(topic, summaries, filename):
    os.makedirs("output", exist_ok=True)
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, f"Topic: {topic}\n\nSummaries:\n")
    for i, (summary, url) in enumerate(summaries, 1):
        pdf.multi_cell(0, 10, f"{i}. {summary}\n[Source] {url}\n")
        pdf.ln()
    pdf.output(filename)
