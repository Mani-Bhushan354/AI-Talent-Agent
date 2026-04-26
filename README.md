🤖 Agentic Talent Intelligence & 3D Visualization
Catalyst AI Hackathon Submission by Mani Bhushan

🚀 Overview
Recruiters today spend hours manually screening resumes against vague and unstructured job descriptions. This project introduces an **Agentic AI Recruitment Co-pilot** that automates the entire workflow—from understanding hiring intent to ranking candidates and visualizing talent insights in an interactive 3D ecosystem.

The system transforms raw recruiter input into **actionable hiring intelligence**, enabling faster, data-driven decision-making.

🏗️ Architecture & Implementation

Frontend:
Built using Streamlit with a custom **Glassmorphism UI**, delivering a modern, enterprise-grade dark interface.

Agentic Brain:
Powered by Gemini 1.5 Flash, responsible for:

* Parsing unstructured Job Descriptions
* Extracting must-have skills and experience
* Generating recruiter-style outreach messages

Core Pipeline:

1. Agentic Parsing (utils.py)
   Converts raw JD text into structured hiring requirements using LLM reasoning.

2. Intelligent Ranking Engine (agent.py)
   Computes a weighted `final_score` based on skill match, experience, and engagement signals.

3. 3D Talent Ecosystem (app.py)
   Uses Plotly to map candidates across:

   * Tech Match
   * Experience
   * Engagement

   This creates an **interactive hiring map**, enabling recruiters to instantly identify top talent clusters.

4. Persona-Driven Outreach
   Generates personalized LinkedIn-style messages using a **Senior Recruiter persona**, improving response rates.

⚖️ Trade-offs & Engineering Decisions

* Set Matching vs Semantic Search
  Implemented fast set-based matching for the hackathon. Future versions will use vector embeddings (FAISS/ChromaDB) for deeper semantic understanding.

* Smart Mock Mode
  Ensures uninterrupted demo experience by switching to rule-based logic if API limits are reached.

* Local JSON Storage
  Chosen for speed and simplicity. Scalable architecture would integrate MongoDB/PostgreSQL.

📊 Impact

* Reduces resume screening time from hours → seconds
* Provides **visual decision support** instead of static lists
* Enables **AI-driven recruiter outreach**

▶️ How to Run

1. Install Dependencies
   pip install -r requirements.txt

2. Launch App
   streamlit run app.py

3. Add Gemini API Key
   Enter in sidebar for full agentic functionality

🎥 Demo Video
(https://drive.google.com/drive/u/0/folders/1WDeMZrUaPLnqDuS8d5fLt2AWWKQYnw4Q)

🌟 Future Scope

* Vector search for semantic skill matching
* Multi-user recruiter dashboards
* ATS integrations (LinkedIn, Workday)
* Real-time candidate data pipelines
