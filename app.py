# app.py
# app.py
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import re
from pathlib import Path
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import textstat

# Local imports
from email_parser import parse_email
from tone_scorer import analyze_tone
from sentence_analyzer import analyze_sentences
from rewrite_engine import rewrite_full_email, get_rewrite_suggestions
from report_builder import build_full_report

# Download NLTK data if needed (local)
nltk.download('vader_lexicon', quiet=True)
nltk.download('punkt', quiet=True)

st.set_page_config(
    page_title="ToneCoach - Email Power Analyzer",
    page_icon="📧",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for dark theme
st.markdown("""
<style>
    .main {background-color: #030309; color: #ffffff;}
    .stButton>button {background-color: #FF6B6B; color: white; border: none;}
    .stTextArea textarea {font-family: 'JetBrains Mono', monospace;}
    .metric-card {background-color: #1a1a2e; padding: 20px; border-radius: 10px; border-left: 5px solid #FF6B6B;}
    h1, h2, h3 {font-family: 'JetBrains Mono', monospace;}
</style>
""", unsafe_allow_html=True)

st.title("📧 ToneCoach - Email Power Analyzer")
st.markdown("**Professional email tone optimization • 100% local • Zero API calls**")

# Sidebar
with st.sidebar:
    st.markdown("### ⚙️ Settings")
    st.markdown("**🟢 OFFLINE MODE**")
    
    target_register = st.selectbox(
        "Preferred Communication Register",
        ["Direct", "Diplomatic", "Warm"],
        index=1
    )
    
    email_type = st.selectbox(
        "Email Context",
        ["Internal Team", "External Stakeholder", "Client", "Recruiter/Hiring"]
    )
    
    st.markdown("---")
    st.info("All analysis runs locally using spaCy, VADER, and local Transformers models.")

# Main input
raw_email = st.text_area(
    "Paste your email here:",
    height=300,
    placeholder="Subject: Follow up on Q3 deliverables...\n\nHi Team,\n\n...",
    help="Include the full email with subject if available"
)

if st.button("🔍 Analyze Email", type="primary", use_container_width=True):
    if not raw_email.strip():
        st.error("Please enter an email to analyze.")
    else:
        with st.spinner("Analyzing tone, structure, and impact..."):
            # Parse
            email_data = parse_email(raw_email)
            
            # Tone analysis
            tone_results = analyze_tone(email_data)
            
            # Sentence analysis
            sentences_analysis = analyze_sentences(email_data["body"])
            
            # Store in session
            st.session_state.email_data = email_data
            st.session_state.tone_results = tone_results
            st.session_state.sentences = sentences_analysis
            st.session_state.target_register = target_register
            st.session_state.raw_email = raw_email

# Display results if analyzed
if "tone_results" in st.session_state:
    email_data = st.session_state.email_data
    tone_results = st.session_state.tone_results
    sentences = st.session_state.sentences
    target_register = st.session_state.target_register
    
    tabs = st.tabs(["📊 Tone Scorecard", "🔦 Sentence Spotlight", "✍️ Rewrites", "📋 Full Report"])
    
    with tabs[0]:
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.subheader("Overall Tone Profile")
            overall_score = tone_results.get("overall_score", 75)
            st.metric("Tone Effectiveness", f"{overall_score}/100", delta="Strong" if overall_score > 70 else "Needs Work")
            
            # Radar chart
            dimensions = list(tone_results["dimensions"].keys())
            scores = [tone_results["dimensions"][d]["score"] for d in dimensions]
            
            fig = go.Figure(data=go.Scatterpolar(
                r=scores,
                theta=dimensions,
                fill='toself',
                line_color='#FF6B6B'
            ))
            fig.update_layout(
                polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
                showlegend=False,
                template="plotly_dark",
                height=500
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.subheader("Priority Fixes")
            for issue in tone_results.get("top_issues", [])[:3]:
                st.markdown(f"""
                <div class="metric-card">
                    <strong>{issue['type'].upper()}</strong><br>
                    {issue['description']}<br>
                    <small>Impact: {issue['severity']}</small>
                </div>
                """, unsafe_allow_html=True)
    
    with tabs[1]:
        st.subheader("Sentence-by-Sentence Analysis")
        for i, sent in enumerate(sentences):
            with st.expander(f"Sentence {i+1}: {sent['text'][:80]}..."):
                cols = st.columns(4)
                for j, flag in enumerate(sent.get("flags", [])):
                    cols[j % 4].markdown(f"**{flag}**")
    
    with tabs[2]:
        st.subheader("Suggested Rewrites")
        rewritten = rewrite_full_email(st.session_state.raw_email, tone_results.get("issues", []), target_register)
        
        col_orig, col_new = st.columns(2)
        with col_orig:
            st.markdown("**Original**")
            st.text_area("", value=st.session_state.raw_email, height=400, disabled=True)
        with col_new:
            st.markdown("**Rewritten**")
            st.text_area("", value=rewritten, height=400)
        
        st.download_button(
            "📥 Download Rewritten Email",
            rewritten,
            file_name="rewritten_email.txt",
            mime="text/plain"
        )
    
    with tabs[3]:
        report = build_full_report(email_data, tone_results, sentences, target_register)
        st.markdown(report)
        
        st.download_button(
            "📄 Download Full PDF Report (simulated)",
            report,
            file_name="tonecoach_report.txt"
        )

# LinkedIn sharing text
st.markdown("---")
st.subheader("🔗 Ready for LinkedIn?")
linkedin_text = """
Just built ToneCoach - a 100% local AI email tone analyzer and rewriter using Streamlit, spaCy, and local Transformers. 

No APIs, no data leaving your machine. Perfect for professionals who want confident, polished communication.

Features:
• Multi-dimensional tone scoring (assertiveness, hedging, passive aggression, etc.)
• Sentence-level spotlight with flags
• Context-aware rewrites (Direct/Diplomatic/Warm)
• Radar visualizations + full reports

Running entirely offline. Great for recruiters, sales, and engineering leaders.

#Productivity #Communication #AI #LocalAI #Python #Streamlit
"""
st.code(linkedin_text, language="markdown")
st.button("Copy LinkedIn Post", on_click=lambda: st.success("Copied to clipboard! (simulated)"))