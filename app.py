import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import time
from agent import get_ranked_candidates
from utils import configure_gemini, parse_jd_agentic, generate_outreach

# --- Page Setup & Glassmorphism CSS ---
st.set_page_config(
    page_title="AI Talent Scout", 
    layout="wide", 
    page_icon="🔮",
    initial_sidebar_state="expanded"
)

st.markdown("""
    <style>
    /* Dark Gradient Background for the whole app */
    .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #1e1e3f 100%);
        color: #e2e8f0;
    }
    
    /* Fixed Glassmorphism Sidebar */
    [data-testid="collapsedControl"] { display: none !important; }
    section[data-testid="stSidebar"] { 
        width: 350px !important; min-width: 350px !important; 
        background: rgba(15, 23, 42, 0.4) !important;
        backdrop-filter: blur(16px) !important;
        -webkit-backdrop-filter: blur(16px) !important;
        border-right: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    /* Glassmorphism Metric Cards */
    div[data-testid="stMetric"] { 
        background: rgba(255, 255, 255, 0.03); 
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        padding: 15px 20px; 
        border-radius: 16px; 
        border: 1px solid rgba(255, 255, 255, 0.1);
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3);
    }
    div[data-testid="stMetricValue"] { color: #38bdf8; font-weight: 800; }
    div[data-testid="stMetricLabel"] { color: #94a3b8; }
    
    /* Glassmorphism Tabs */
    .stTabs [data-baseweb="tab-list"] { background: transparent; }
    .stTabs [data-baseweb="tab"] { 
        background: rgba(255, 255, 255, 0.02); 
        border-radius: 12px 12px 0 0; 
        padding: 12px 24px; 
        color: #94a3b8;
        border: 1px solid transparent;
    }
    .stTabs [aria-selected="true"] { 
        background: rgba(255, 255, 255, 0.08); 
        border-bottom: 2px solid #38bdf8 !important; 
        color: #38bdf8 !important; 
        font-weight: bold;
        border-top: 1px solid rgba(255, 255, 255, 0.1);
        border-left: 1px solid rgba(255, 255, 255, 0.1);
        border-right: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    /* Bulletproof Text Area & Input Styling Fix */
    .stTextArea textarea, .stTextInput input {
        color: #ffffff !important;
        -webkit-text-fill-color: #ffffff !important;
        caret-color: #ffffff !important; 
        background-color: transparent !important; /* Forces the white box to be transparent */
    }
    div[data-baseweb="base-input"], div[data-baseweb="textarea"] {
        background-color: rgba(255, 255, 255, 0.05) !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        border-radius: 8px !important;
    }
    
    /* Awesome Button Styling (Deploy Agent Analysis & Webhook) */
    div.stButton > button {
        background: linear-gradient(90deg, #38bdf8 0%, #3b82f6 100%) !important;
        color: #ffffff !important;
        font-weight: 800 !important;
        border: none !important;
        border-radius: 8px !important;
        box-shadow: 0 4px 15px rgba(56, 189, 248, 0.3) !important;
        transition: all 0.3s ease !important;
    }
    div.stButton > button:hover {
        box-shadow: 0 6px 20px rgba(56, 189, 248, 0.6) !important;
        color: #ffffff !important;
        border-color: transparent !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- Fixed Sidebar ---
with st.sidebar:
    st.title("🔮 System Control")
    
    # API Key is fully visible, and the background is now transparent dark!
    api_key = st.text_input("Gemini API Key")
    
    model = configure_gemini(api_key)
    
    if model: st.success("🟢 API Connected")
    else: st.warning("🔴 API Offline (Mock Mode)")
    
    st.divider()
    st.markdown("### Catalyst AI Hackathon")
    st.info("👨‍💻 **Developer:** Mani Bhushan\n\n🎯 **Track:** Agentic AI")

# --- Main App ---
st.title("🌌 Agentic Talent Intelligence")
st.caption("AI-Powered Candidate Scouting & Outreach Workflows")

jd_input = st.text_area("📄 Paste Job Description:", height=100, placeholder="e.g. Looking for a Python Developer with SQL experience...")

if st.button("🚀 Deploy Agent Analysis"):
    if jd_input:
        my_bar = st.progress(0, text="Parsing JD Intent...")
        jd_params = parse_jd_agentic(model, jd_input)
        time.sleep(0.5)
        
        my_bar.progress(50, text="Scoring Candidates...")
        results = get_ranked_candidates(jd_params)
        df = pd.DataFrame(results)
        time.sleep(0.5)
        
        my_bar.progress(100, text="Finalizing 3D Environment...")
        time.sleep(0.5)
        my_bar.empty()
        
        # --- Interactive Tabs ---
        t1, t2, t3 = st.tabs(["🌌 3D Pipeline", "🧬 Deep Profile", "⚡ Automated Actions"])

        with t1:
            st.subheader("Interactive Candidate Ecosystem")
            st.caption("Rotate and zoom to explore candidates. Names are visible above the data points.")
            
            # 3D Scatter Plot with Visible Names
            fig_3d = px.scatter_3d(
                df, x='match_score', y='interest_score', z='experience',
                color='decision', size='final_score', hover_name='name',
                text='name', # Forces names to render
                color_discrete_map={'🔥 Hot Match': '#38bdf8', '⭐ Potential': '#a855f7', '❌ Pass': '#475569'}
            )
            
            # Positions the text above the dot and styles it white
            fig_3d.update_traces(textposition='top center', textfont=dict(size=12, color='#ffffff'))
            
            fig_3d.update_layout(
                scene=dict(
                    xaxis_title='Tech Match', yaxis_title='Engagement', zaxis_title='Experience (Yrs)',
                    xaxis=dict(gridcolor='rgba(255,255,255,0.1)', backgroundcolor='rgba(0,0,0,0)'),
                    yaxis=dict(gridcolor='rgba(255,255,255,0.1)', backgroundcolor='rgba(0,0,0,0)'),
                    zaxis=dict(gridcolor='rgba(255,255,255,0.1)', backgroundcolor='rgba(0,0,0,0)')
                ),
                margin=dict(l=0, r=0, b=0, t=0),
                paper_bgcolor="rgba(0,0,0,0)",
                font_color="#e2e8f0",
                legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01)
            )
            st.plotly_chart(fig_3d, use_container_width=True, height=600)
            
            st.dataframe(df[["name", "final_score", "match_score", "decision"]].style.background_gradient(cmap='PuBu_r'), use_container_width=True)

        with t2:
            selected = st.selectbox("Select candidate to inspect:", df["name"])
            c = df[df["name"] == selected].iloc[0]
            
            m1, m2, m3 = st.columns(3)
            m1.metric("Overall Score", f"{c['final_score']}/100")
            m2.metric("Tech Match", f"{c['match_score']}/100")
            m3.metric("Engagement", f"{c['interest_score']}/100")
            
            st.divider()
            
            # Interactive Radar Chart
            st.subheader(f"Skill Radar: {c['name']}")
            radar_fig = go.Figure()
            radar_fig.add_trace(go.Scatterpolar(
                r=[c['match_score'], c['interest_score'], c['experience']*10, 100 - len(c['missing_critical'])*20],
                theta=['Tech Match', 'Engagement', 'Experience Gap', 'Critical Skills'],
                fill='toself', name=c['name'], line_color='#38bdf8', fillcolor='rgba(56, 189, 248, 0.3)'
            ))
            radar_fig.update_layout(
                polar=dict(
                    radialaxis=dict(visible=True, range=[0, 100], gridcolor='rgba(255,255,255,0.1)'),
                    angularaxis=dict(gridcolor='rgba(255,255,255,0.1)'),
                    bgcolor="rgba(0,0,0,0)"
                ), 
                paper_bgcolor="rgba(0,0,0,0)", 
                font_color="#e2e8f0", 
                showlegend=False, height=350
            )
            st.plotly_chart(radar_fig, use_container_width=True)
            
            c1, c2 = st.columns(2)
            c1.success(f"**Matched:** {', '.join(c['crit_matches']) if c['crit_matches'] else 'None'}")
            c2.error(f"**Missing:** {', '.join(c['missing_critical']) if c['missing_critical'] else 'None'}")

        with t3:
            st.subheader("Agentic Outreach Hub")
            msg = generate_outreach(model, c, jd_params['role'])
            st.text_area("Review AI Draft:", value=msg, height=150)
            
            if st.button(f"✉️ Trigger Webhook for {c['name']}"):
                with st.spinner("Dispatching..."):
                    time.sleep(1.5)
                    st.toast(f"Success! Webhook fired for {c['name']}.", icon="✅")
                    st.balloons()
    else:
        st.error("Please paste a Job Description.")