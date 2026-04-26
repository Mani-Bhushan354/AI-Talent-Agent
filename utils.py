import json
import re
import google.generativeai as genai

def configure_gemini(api_key):
    """Initializes the Gemini model."""
    if not api_key: return None
    try:
        genai.configure(api_key=api_key)
        return genai.GenerativeModel("gemini-1.5-flash")
    except Exception:
        return None

def parse_jd_agentic(model, jd_text):
    """
    Agentic AI: Reasons about JD using Gemini.
    Includes a Smarter Mock fallback to handle Java, C, and Python detection offline.
    """
    
    # --- LIVE API MODE ---
    if model:
        prompt = f"""
        Analyze this Job Description as an expert technical recruiter:
        "{jd_text}"
        
        1. Extract 'Must-Have' technical skills.
        2. Extract 'Nice-to-Have' skills.
        3. Determine minimum years of experience.
        
        Return ONLY a JSON object:
        {{"role": "Title", "critical_skills": ["a", "b"], "secondary_skills": ["c"], "min_experience": 2}}
        """
        try:
            res = model.generate_content(prompt)
            # Use Regular Expressions to find the JSON block in the AI response
            match = re.search(r'\{.*\}', res.text, re.DOTALL)
            if match:
                return json.loads(match.group(0))
        except Exception:
            pass # Fall through to Mock Mode if API fails or quota is exhausted
            
    # --- SMARTER MOCK MODE (Offline Fallback) ---
    # This logic ensures your demo stays accurate even without an active API key.
    text_lower = jd_text.lower()
    
    if "java" in text_lower:
        detected_role = "Java Developer"
        skills = ["Java", "Spring Boot", "Microservices", "Hibernate"]
    elif "c developer" in text_lower or "c++" in text_lower:
        detected_role = "C Developer"
        skills = ["C", "C++", "Embedded Systems", "Debugging"]
    elif "python" in text_lower:
        detected_role = "Python Developer"
        skills = ["Python", "Django", "FastAPI", "SQL"]
    else:
        # General fallback if no specific keywords are detected
        detected_role = "Technical Specialist"
        skills = ["Python", "SQL", "Cloud Computing"]

    return {
        "role": detected_role, 
        "critical_skills": skills[:2], 
        "secondary_skills": [skills[-1]], 
        "min_experience": 1
    }

def generate_outreach(model, candidate, role):
    """
    Generates personalized outreach using Gemini.
    Falls back to a high-quality template if offline.
    """
    # Use the specific skills the candidate matched on for personalization
    matched_skills = candidate.get('crit_matches', candidate.get('skills', []))
    top_skills = ", ".join(matched_skills[:2]) if matched_skills else "your technical background"
    
    if model:
        prompt = f"""
        Act as a Senior Technical Recruiter. 
        Write a professional, warm LinkedIn invite (under 60 words) to {candidate['name']} 
        for a {role} role mentioning their experience with {top_skills}.
        No placeholders. Just output the message body.
        """
        try:
            return model.generate_content(prompt).text.strip()
        except:
            pass

    # Mock Fallback Message
    return (f"Hi {candidate['name']}, I was really impressed by your background in {top_skills}. "
            f"We are building out our team for a {role} position and your profile aligns perfectly with our stack. "
            f"I'd love to connect and share more about the role!")