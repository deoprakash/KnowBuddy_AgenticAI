import os
import re
import time
from datetime import datetime
from dotenv import load_dotenv
import streamlit as st
from langchain_groq import ChatGroq
from langchain_community.tools import DuckDuckGoSearchRun
from fpdf import FPDF
from random import shuffle

# ---------- LOAD ENV ----------
load_dotenv()

# ---------- STREAMLIT PAGE CONFIG ----------
st.set_page_config(page_title="KnowBuddy - Student Research Assistant", layout="centered", page_icon="🧠")

# ---------- STYLING ----------
st.markdown("""
    <style>
    .title-text { text-align: center; font-size: 2.8rem; font-weight: 700; color: #4B8BBE; margin-bottom: 1rem; }
    .subtitle-text { text-align: center; font-size: 1.2rem; color: #6c757d; margin-bottom: 2rem; }
    .stButton>button { width: 100%; font-size: 1rem; padding: 0.75rem; }
    </style>
""", unsafe_allow_html=True)

# ---------- FORMATTER ----------
def format_ai_summary(content: str):
    match = re.search(r"1\.\s", content)
    if match:
        content = content[match.start():]
    lines = re.split(r'\n\d+\.\s', content)
    return [line.strip() for line in lines if line.strip()]


# ---------- LLM SETUP ----------
llm = ChatGroq(
    model_name="llama3-70b-8192",
    temperature=0,
    api_key=os.getenv("GROQ_API_KEY")
)
search_tool = DuckDuckGoSearchRun()

# ---------- HEADER ----------
st.markdown("<div class='title-text'>🧠 KnowBuddy</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle-text'>Student-Focused AI Research Assistant</div>", unsafe_allow_html=True)

# ---------- TABS ----------
tab1, tab2, tab3, tab4 = st.tabs(["🔍 Research", "✍️ Essay Builder", "📅 Time Table", "📉 Citation"])

# ========== RESEARCH TOOL ==========
with tab1:
    st.subheader("🔍 Research Summarizer")
    topic = st.text_input("📌 Enter your research topic", placeholder="e.g., Future of Space Travel")

    if st.button("🔍 Search & Summarize", use_container_width=True) and topic.strip():
        st.info(f"🔍 Searching for: **{topic}**")
        with st.spinner("Gathering articles..."):
            results = search_tool.run(topic)
            time.sleep(1)

        st.markdown("### 📜 Raw Results")
        with st.expander("Show Raw Output"):
            st.code(results, language="text")

        prompt = f"Summarize the key points about: {topic}. Provide at least 10 detailed bullet points with explanation."

        with st.spinner("Summarizing..."):
            response = llm.invoke(prompt)
            raw_summary = response.content
            summary_list = format_ai_summary(raw_summary)

        st.success("✅ Summary Ready:")
        for idx, item in enumerate(summary_list, 1):
            st.markdown(f"**{idx}.** {item}\n")

# ========== ESSAY BUILDER ==========
with tab2:
    st.subheader("✍️ AI Essay Builder")
    essay_topic = st.text_input("Enter Essay Topic", key="essay_topic")
    if essay_topic:
        if st.button("Generate Essay"):
            essay = llm.invoke(f"Write a detailed essay on the topic: {essay_topic}").content
            st.markdown(essay)

# ========== TIME TABLE GENERATOR ==========
with tab3:
    st.subheader("📅 Time Table Generator")
    subjects = st.text_input("Subjects (comma separated)", key="tt_subjects")
    hours = st.slider("Hours per day", 1, 8, 3)
    if subjects and st.button("Generate Timetable"):
        days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]
        s_list = [s.strip() for s in subjects.split(",")]
        shuffle(s_list)
        timetable = {day: s_list[i % len(s_list)] for i, day in enumerate(days)}
        st.json(timetable)

# ========== CITATION GENERATOR ==========
with tab4:
    st.subheader("📉 Citation Generator")
    title = st.text_input("Title")
    author = st.text_input("Author")
    year = st.text_input("Year")
    source = st.text_input("Source URL")
    style = st.radio("Style", ["APA", "MLA"])
    if title and author and year and source:
        if st.button("Generate Citation"):
            if style == 'APA':
                citation = f"{author} ({year}). *{title}*. Retrieved from {source}"
            else:
                citation = f"{author}. \"{title}.\" {source}, {year}."
            st.code(citation, language='markdown')
