import streamlit as st
import re
import random
from datetime import datetime

st.set_page_config(page_title="GNITS Academic Assistant", page_icon="🎓", layout="wide")

# Custom CSS
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
    }
    .main-header {
        text-align: center;
        padding: 1.5rem;
        background: linear-gradient(135deg, #e94560 0%, #533483 100%);
        border-radius: 20px;
        margin-bottom: 2rem;
    }
    .main-header h1 {
        font-size: 2rem;
        color: white;
        margin: 0;
    }
    .user-message {
        background: linear-gradient(135deg, #e94560 0%, #533483 100%);
        color: white;
        padding: 12px 18px;
        border-radius: 20px;
        margin: 10px 0;
        max-width: 75%;
        float: right;
        clear: both;
    }
    .bot-message {
        background: rgba(255,255,255,0.1);
        color: white;
        padding: 12px 18px;
        border-radius: 20px;
        margin: 10px 0;
        max-width: 75%;
        float: left;
        clear: both;
        backdrop-filter: blur(10px);
    }
    .stButton > button {
        background: linear-gradient(135deg, #e94560 0%, #533483 100%);
        color: white;
        border-radius: 25px;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="main-header">
    <h1>🎓 GNITS Academic Assistant</h1>
    <p>R22 & R25 Regulations | Course Structure | Syllabus | Exam Rules</p>
</div>
""", unsafe_allow_html=True)

# Initialize session
if 'messages' not in st.session_state:
    st.session_state.messages = []

# ============ COMPLETE KNOWLEDGE BASE ============

# Academic Regulations Database
ACADEMIC_RULES = {
    "attendance": """📊 **ATTENDANCE REQUIREMENTS (Clause 7.0):**
    
• Minimum 75% attendance required to appear for exams
• Shortage up to 10% (65-74%) can be condoned by College Academic Committee
• Below 65% attendance → NO condonation, detained
• Two periods attendance considered if student appears for mid-term exam
• Condonation fee payable as per college norms""",

    "promotion": """📈 **PROMOTION RULES (Clause 14.0 - R25 / 8.0 - R22):**

**R25 Regulations:**
• I Year I to II Sem: Regular course + attendance requirement
• I Year II to II Year I: Must secure 25% of total credits up to I Year II Sem
• II Year I to II Sem: Regular course + attendance
• II Year II to III Year I: Must secure 25% credits up to II Year II Sem
• III Year I to II Sem: Regular course + attendance
• III Year II to IV Year I: Regular course + attendance

**R22 Regulations:**
• I to II Year: Need 20 credits out of 40
• II to III Year: Need 48 credits out of 80
• III to IV Year: Need 72 credits out of 120""",

    "grading": """🎯 **GRADING SYSTEM (Clause 10.3):**

| % Marks | Grade | Grade Points |
|---------|-------|--------------|
| ≥ 90% | O (Outstanding) | 10 |
| 80-89% | A+ (Excellent) | 9 |
| 70-79% | A (Very Good) | 8 |
| 60-69% | B+ (Good) | 7 |
| 50-59% | B (Average) | 6 |
| 40-49% | C (Pass) | 5 |
| < 40% | F (Fail) | 0 |

**Passing Criteria:** Minimum 35% in CIE (14/40), 35% in SEE (21/60), and overall 40% (40/100)""",

    "evaluation": """📝 **EVALUATION SCHEME (Clause 9.0):**

**Theory Courses (100 marks):**
• CIE (Internal): 40 marks
  - Two Mid-Term Exams (avg of 2): 30 marks
  - Assignments (avg of 2): 5 marks
  - Viva/PPT/Case Study: 5 marks
• SEE (End Sem Exam): 60 marks
  - Part-A: 10 marks (5 questions × 2 marks)
  - Part-B: 50 marks (5 questions × 10 marks, with either/or choice)

**Practical/Lab Courses (100 marks):**
• CIE: 40 marks (day-to-day:20, internal lab exam:20)
• SEE: 60 marks (conducted by two examiners)""",

    "sgpa_cgpa": """📊 **SGPA & CGPA CALCULATION (Clause 10.9-10.11):**

**SGPA** = Σ(Credit × Grade Point) / Σ(Credits)
→ Calculated when all courses in semester are cleared
→ Rounded to 2 decimal places

**CGPA** = Σ(Credit Points for best 160 credits) / Σ(Credits for those courses)

**Conversion to Percentage:** % = (CGPA - 0.5) × 10

**Class Classification (R25):**
• First Class with Distinction: CGPA ≥ 7.5 (first attempt only)
• First Class: CGPA ≥ 6.5
• Second Class: CGPA ≥ 5.5
• Pass Class: CGPA ≥ 5.0""",

    "exam_rules": """📋 **EXAMINATION RULES (Clause 9.0):**

• Mid-Term Exams: 2 per semester (30 marks each, 2 hours duration)
  - Part-A: 10 marks (MCQ/Fill blanks/Match)
  - Part-B: 20 marks (6 questions, answer 4 of 5 marks each)
• CBT (Computer Based Test): Available for missed mid-term or improvement
• SEE: 3 hours duration
• Grace Marks: Up to 0.15% of total marks for eligible students""",

    "malpractice": """⚠️ **MALPRACTICE PENALTIES:**

• Possessing unauthorized material → Expulsion from that subject
• Copying → Expulsion from all subjects of that semester
• Impersonation → Debarred for 2 semesters, seat forfeited
• Using mobile phone → Expulsion from all subjects
• Misconduct → Debarred, seat forfeited"""
}

# Course Structure Database (R25 - IT)
COURSE_STRUCTURE = {
    "i_year_i_sem": """📚 **I Year I Semester (R25) - 20 Credits**

| Course | Subject | Credits |
|--------|---------|---------|
| BSC | Matrices and Calculus | 4 |
| BSC | Advanced Engineering Physics | 3 |
| ESC | Programming for Problem Solving | 3 |
| ESC | Basic Electrical Engineering | 3 |
| MEC | Engineering Drawing & CAD | 3 |
| Lab | Advanced Engineering Physics Lab | 1 |
| Lab | Programming Lab | 1 |
| Lab | Basic Electrical Engineering Lab | 1 |
| Lab | IT Workshop | 1 |""",

    "i_year_ii_sem": """📚 **I Year II Semester (R25) - 20 Credits**

| Course | Subject | Credits |
|--------|---------|---------|
| BSC | ODE and Vector Calculus | 3 |
| BSC | Engineering Chemistry | 3 |
| ESC | Data Structures | 3 |
| ESC | Basic Electronics | 3 |
| HSC | English for Skill Enhancement | 3 |
| Lab | Engineering Chemistry Lab | 1 |
| Lab | Data Structures Lab | 1 |
| Lab | English Language & Comm Skills Lab | 1 |
| Lab | Engineering Workshop | 1 |
| Lab | Python Programming Lab | 1 |""",

    "ii_year_i_sem": """📚 **II Year I Semester (R25) - 22 Credits**

| Course | Subject | Credits |
|--------|---------|---------|
| BSC | Mathematical & Statistical Foundations | 3 |
| PC | Computer Organization & Microprocessor | 3 |
| PC | Java Programming | 3 |
| PC | Web Programming | 3 |
| PC | Introduction to IoT | 3 |
| HSC | Innovation and Entrepreneurship | 2 |
| Lab | Computational Mathematics Lab | 1 |
| Lab | Java Programming Lab | 1 |
| Lab | Web Programming Lab | 1 |
| Lab | Internet of Things Lab | 1 |
| SDC | Data Visualization (Power BI/Tableau) | 1 |""",

    "ii_year_ii_sem": """📚 **II Year II Semester (R25) - 20 Credits**

| Course | Subject | Credits |
|--------|---------|---------|
| PC | Discrete Mathematics | 3 |
| PC | Full Stack Development | 3 |
| PC | Operating Systems | 3 |
| PC | Database Management Systems | 3 |
| PC | Algorithm Design and Analysis | 3 |
| Lab | Full Stack Development Lab | 1 |
| Lab | Operating Systems Lab | 1 |
| Lab | DBMS Lab | 1 |
| SDC | UI Design - Flutter | 1 |
| MC | Indian Knowledge System | 1 |"""
}

# R22 Syllabus Database (CSE)
R22_SYLLABUS = {
    "cse_courses": """📖 **CSE Courses (R22 Regulations):**

**I Year:**
• Linear Algebra and Multivariable Calculus
• Programming for Problem Solving
• Basic Electrical Engineering
• Engineering Graphics
• Applied Chemistry, Applied Physics
• Data Structures
• Python Programming

**II Year:**
• Probability and Statistics
• Design and Analysis of Algorithms
• Database Management Systems
• Digital Logic Design
• Object Oriented Programming through JAVA
• Operating Systems
• Computer Organization and Architecture
• Software Engineering

**III Year:**
• Full Stack Development
• Computer Networks
• Machine Learning
• Automata and Compiler Design
• Computer Vision and Pattern Recognition

**IV Year:**
• Cryptography and Network Security
• Natural Language Processing
• Deep Learning
• Blockchain Technologies
• Project Work""",

    "exam_pattern": """📝 **R22 Exam Pattern:**

**Theory Subjects (100 marks):**
• CIE: 40 marks
  - Two Mid-Term Exams (avg): 30 marks
  - Assignments (2 assignments avg): 5 marks
  - Subject Viva/PPT: 5 marks
• SEE: 60 marks
  - Part-A (10 compulsory questions of 1 mark each): 10 marks
  - Part-B (5 questions of 10 marks each, either/or choice): 50 marks

**Practical Subjects (100 marks):**
• CIE: 40 marks (day-to-day:20, internal lab exam:20)
• SEE: 60 marks (conducted by two examiners)""",

    "electives": """📚 **Professional Electives (R22 CSE):**

**PE-1 (III Year I Sem):**
• Advanced Computer Architecture
• Data Mining
• Computer Graphics
• Artificial Intelligence

**PE-2 (III Year I Sem):**
• Principles of Programming Languages
• Software Testing Methodologies
• Cloud Computing
• Distributed Systems

**PE-3 (III Year II Sem):**
• Information Retrieval Systems
• Soft Computing
• Agile Methodology
• Graph Theory

**PE-4 (IV Year I Sem):**
• Data Science using R
• Internet of Things
• DevOps

**PE-5 (IV Year I Sem):**
• Natural Language Processing
• Big Data Analytics
• Deep Learning
• Blockchain Technologies"""
}

# Complete Academic Information
ACADEMIC_INFO = """
GNITS Academic Information (R25 & R22 Regulations)

CREDIT REQUIREMENTS:
- Total Credits for B.Tech: 160 credits (164 registered, best 160 considered)
- Each semester: ~20 credits
- Minimum passing: 'C' grade (GP ≥ 5)
- Maximum duration: 8 years from admission

COURSE CLASSIFICATION:
- BSC: Basic Sciences (Maths, Physics, Chemistry)
- ESC: Engineering Sciences
- HSC: Humanities & Social Sciences
- PC: Professional Core
- PE: Professional Electives
- OE: Open Electives
- PW: Project Work
- SDC: Skill Development Courses
- MC: Mandatory Courses (no credits)

HONORS & MINOR DEGREES:
- Honors: 20 additional credits in same branch (CGPA ≥ 7.5 required)
- Minor: 18 additional credits in other branch (no backlogs)
- Available from III Year onwards

LATERAL ENTRY SCHEME (LES):
- Duration: 3 years (II to IV Year)
- Credits needed: 120
- Maximum: 6 academic years

EXIT OPTION (MEME Scheme):
- After II Year: 2-Year UG Diploma (requires 2 additional credits via internship)
- Re-entry allowed within 4 years

SUPPLEMENTARY EXAMS:
- Conducted at end of each semester
- Advanced supplementary for IV Year II Sem courses
- Internal marks carried forward
"""

def get_academic_response(user_input):
    text = user_input.lower().strip()
    
    # Greetings
    if re.search(r'^(hi|hello|hey|namaste|good morning|good afternoon)', text):
        return "Hello! 👋 I'm GNITS Academic Assistant. I can help you with:\n\n• 📋 Academic Regulations (R22/R25)\n• 📚 Course Structure & Syllabus\n• 📝 Exam Rules & Grading\n• 🎯 Attendance & Promotion Rules\n• ✅ Fee Structure & Admissions\n• 🎓 Placements & Facilities\n\nWhat would you like to know?"
    
    # Attendance related
    if re.search(r'(attendance|absent|condonation|shortage)', text):
        return ACADEMIC_RULES["attendance"]
    
    # Promotion rules
    if re.search(r'(promotion|promoted|next semester|year to next)', text):
        return ACADEMIC_RULES["promotion"]
    
    # Grading related
    if re.search(r'(grade|grading|gpa|sgpa|cgpa|percentage|class|distinction)', text):
        return ACADEMIC_RULES["sgpa_cgpa"]
    
    # Exam related
    if re.search(r'(exam|mid|semester end|see|cie|internal|external|evaluation|marks|passing)', text):
        return ACADEMIC_RULES["evaluation"]
    
    # Malpractice
    if re.search(r'(malpractice|cheating|copy|disciplinary|penalty|misconduct)', text):
        return ACADEMIC_RULES["malpractice"]
    
    # Course structure
    if re.search(r'(i year|1st year|first year|semester 1|semester i|i-i)', text):
        return COURSE_STRUCTURE["i_year_i_sem"]
    if re.search(r'(i year ii|1st year 2nd|i-ii|second semester first year)', text):
        return COURSE_STRUCTURE["i_year_ii_sem"]
    if re.search(r'(ii year|2nd year|second year|ii-i|ii year i)', text):
        return COURSE_STRUCTURE["ii_year_i_sem"]
    if re.search(r'(ii year ii|2nd year 2nd|ii-ii)', text):
        return COURSE_STRUCTURE["ii_year_ii_sem"]
    
    # R22 specific
    if re.search(r'(r22|old regulation|previous regulation)', text):
        if re.search(r'(course|subject|syllabus|curriculum)', text):
            return R22_SYLLABUS["cse_courses"]
        if re.search(r'(exam|paper pattern|question paper)', text):
            return R22_SYLLABUS["exam_pattern"]
        if re.search(r'(elective|pe|professional elective)', text):
            return R22_SYLLABUS["electives"]
    
    # Electives
    if re.search(r'(elective|professional elective|oe|open elective)', text):
        return R22_SYLLABUS["electives"]
    
    # Credits
    if re.search(r'(credit|total credits|how many credits|credit requirement)', text):
        return ACADEMIC_INFO
    
    # Honors/Minor
    if re.search(r'(honors|honours|minor degree|additional credits)', text):
        return ACADEMIC_INFO
    
    # Lateral entry
    if re.search(r'(lateral|les|diploma|direct second year)', text):
        return ACADEMIC_INFO
    
    # Exit option
    if re.search(r'(exit|leave|dropout|diploma|meme)', text):
        return ACADEMIC_INFO
    
    # Admissions/Fee
    if re.search(r'(admission|fee|fees|cost|tuition|eapcet|gate)', text):
        return "📝 **ADMISSIONS & FEES**\n\n**UG Admissions:**\n• TG-EAPCET exam required\n• Eligibility: 10+2 with PCM\n\n**PG Admissions:**\n• Based on GATE or TS-PGECET\n\n**Fee Structure:**\n• B.Tech: ₹1,62,000 per year + JNTUH fees\n• M.Tech: ₹1,12,000 per year\n\n📞 Contact Admissions: 040-29565856"
    
    # Placements
    if re.search(r'(placement|package|recruiter|company|job|lpa|salary|microsoft|servicenow|deloitte)', text):
        return "🏆 **PLACEMENT HIGHLIGHTS**\n\n✨ **Highest Package:** 50 LPA (Microsoft)\n✨ **Second Highest:** 42.6 LPA (ServiceNow)\n\n🏢 **Top Recruiters:**\n• Microsoft - 50 LPA\n• ServiceNow - 42.6 LPA\n• Deloitte\n• Snowflake\n• PwC\n\n💪 Strong placement record with excellent opportunities!"
    
    # Facilities
    if re.search(r'(library|hostel|canteen|sports|facility|lab|campus)', text):
        return "📚 **FACILITIES**\n\n📖 **Library:** 8 AM to 8 PM (Monday-Saturday)\n🏠 **Hostel:** Girls hostel with 24/7 security\n🏃‍♀️ **Sports:** Indoor badminton, table tennis, volleyball, basketball\n🍽️ **Canteen:** Vegetarian and non-vegetarian options\n💻 **Labs:** State-of-the-art computer and engineering labs"
    
    # Clubs
    if re.search(r'(club|clubs|event|fest|hackathon|splash|coding|robotics|edc|cultural)', text):
        return "🎉 **CLUBS & EVENTS**\n\n💻 **Coding Club** - CodeChef, LeetCode competitions\n🤖 **Robotics Club**\n💡 **Entrepreneurship Development Cell (EDC)**\n🎭 **Cultural Committee** - Splash annual fest\n🔧 **Technical Club** - GNITS ACM Student Chapter\n\n📅 **Upcoming:** IEEE ICoECIT-2026 (March 2026), Splash 2026 (October 2026), Hackathon (February 2026)"
    
    # Contacts
    if re.search(r'(contact|phone|number|email|principal|admission|placement cell)', text):
        return "📞 **IMPORTANT CONTACTS**\n\n👩‍💼 **Principal Office:** 040-29565850\n📝 **Admissions:** 040-29565856\n🏢 **Training & Placement Cell:** 040-29565860\n📚 **Library:** 040-29565870\n\n🕐 Office hours: 9:30 AM to 5:00 PM (Monday-Friday)"
    
    # Default response
    return """😊 **I'm here to help with GNITS information!**

You can ask me about:

📋 **ACADEMIC REGULATIONS**
• Attendance requirements & condonation
• Promotion rules (R22 & R25)
• Grading system (SGPA/CGPA)
• Exam pattern & evaluation
• Malpractice penalties

📚 **COURSE STRUCTURE**
• I Year, II Year, III Year, IV Year courses
• R22 syllabus details
• Professional Electives list
• Credit requirements

🎓 **ADMISSIONS & FEES**
• UG/PG admission process
• Fee structure

🏆 **PLACEMENTS & FACILITIES**
• Placement records
• Library, Hostel, Sports

Just type your question! Example: "What is the attendance requirement?" or "Tell me about R22 syllabus" """ 

# Sidebar
with st.sidebar:
    st.markdown("### 🤖 About This Assistant")
    st.markdown("""
    I can help you with:
    - 📋 **R22 & R25 Regulations**
    - 📚 **Course Structure**
    - 📝 **Exam Rules**
    - 🎯 **Attendance & Promotion**
    - ✅ **Grading System**
    - 🎓 **Admissions & Fees**
    """)
    
    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()
    
    st.markdown("---")
    st.markdown("### 📌 Quick Links")
    st.markdown("[🌐 GNITS Website](https://gnits.ac.in)")

# Quick questions
st.markdown("### 💡 Quick Questions")
cols = st.columns(4)

questions = {
    "📊 Attendance": "What is the attendance requirement?",
    "🎯 SGPA/CGPA": "How is CGPA calculated?",
    "📚 I Year Syllabus": "Tell me about I year I semester courses",
    "🎓 Placements": "What is the highest placement package?"
}

for i, (label, q) in enumerate(questions.items()):
    if cols[i].button(label, use_container_width=True):
        st.session_state.messages.append({"role": "user", "content": q})
        st.rerun()

st.markdown("---")

# Chat display
st.markdown("### 💬 Chat with GNITS Academic Assistant")

for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f"""
        <div style="display: flex; justify-content: flex-end;">
            <div class="user-message">
                <strong>You</strong><br>{msg["content"]}
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div style="display: flex; justify-content: flex-start;">
            <div class="bot-message">
                <strong>🎓 GNITS Assistant</strong><br>{msg["content"]}
            </div>
        </div>
        """, unsafe_allow_html=True)

# Input
question = st.chat_input("Type your question about GNITS academics...")

if question:
    st.session_state.messages.append({"role": "user", "content": question})
    response = get_academic_response(question)
    st.session_state.messages.append({"role": "assistant", "content": response})
    st.rerun()

# Welcome message
if not st.session_state.messages:
    st.info("👋 **Hello!** I'm your GNITS Academic Assistant. Ask me about attendance rules, promotion criteria, grading system, course structure, syllabus, placements, or anything about GNITS! 😊")
