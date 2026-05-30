import streamlit as st
import re

st.set_page_config(page_title="GNITS IT Syllabus Assistant", page_icon="💻", layout="wide")

# Custom CSS
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
    }
    .main-header {
        text-align: center;
        padding: 2rem;
        background: linear-gradient(135deg, #e94560 0%, #533483 100%);
        border-radius: 20px;
        margin-bottom: 2rem;
    }
    .main-header h1 {
        font-size: 2rem;
        color: white;
    }
    .main-header p {
        color: rgba(255,255,255,0.9);
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
        border: none;
    }
    .nav-item {
        padding: 10px;
        margin: 5px 0;
        border-radius: 10px;
        cursor: pointer;
        text-align: center;
        background: rgba(255,255,255,0.1);
        transition: all 0.3s ease;
    }
    .nav-item:hover {
        background: linear-gradient(135deg, #e94560 0%, #533483 100%);
        transform: translateX(5px);
    }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="main-header">
    <h1>💻 GNITS IT Syllabus Assistant</h1>
    <p>R25 Regulations (2025-2026) | I, II, III, IV Years | Complete Syllabus Guide</p>
</div>
""", unsafe_allow_html=True)

# ============ COMPLETE IT SYLLABUS DATABASE ============

IT_SYLLABUS = {
    # I YEAR I SEMESTER
    "i_year_i_sem": """📚 **I YEAR I SEMESTER (R25) - 20 Credits**

| Course | Subject | Credits |
|--------|---------|---------|
| BSC | Matrices and Calculus | 4 |
| BSC | Advanced Engineering Physics | 3 |
| ESC | Programming for Problem Solving | 3 |
| ESC | Basic Electrical Engineering | 3 |
| MEC | Engineering Drawing & CAD | 3 |
| Lab | Advanced Engineering Physics Lab | 1 |
| Lab | Programming for Problem Solving Lab | 1 |
| Lab | Basic Electrical Engineering Lab | 1 |
| Lab | IT Workshop | 1 |

**Detailed Subjects:**
• Matrices and Calculus - Rank, Eigen values, Partial Derivatives, Multiple Integrals
• Advanced Engineering Physics - Crystallography, Quantum Mechanics, Lasers, Fibre Optics
• Programming for Problem Solving - C programming, Arrays, Functions, Pointers, Files
• Basic Electrical Engineering - DC/AC Circuits, Transformers, Electrical Machines
• Engineering Drawing & CAD - Orthographic projections, Isometric views, AutoCAD""",

    # I YEAR II SEMESTER
    "i_year_ii_sem": """📚 **I YEAR II SEMESTER (R25) - 20 Credits**

| Course | Subject | Credits |
|--------|---------|---------|
| BSC | ODE and Vector Calculus | 3 |
| BSC | Engineering Chemistry | 3 |
| ESC | Data Structures | 3 |
| ESC | Basic Electronics | 3 |
| HSC | English for Skill Enhancement | 3 |
| Lab | Engineering Chemistry Lab | 1 |
| Lab | Data Structures using C Lab | 1 |
| Lab | English Language & Communication Skills Lab | 1 |
| Lab | Engineering Workshop | 1 |
| Lab | Python Programming Lab | 1 |

**Detailed Subjects:**
• ODE and Vector Calculus - Differential Equations, Laplace Transforms, Vector Calculus
• Engineering Chemistry - Water Treatment, Electrochemistry, Polymers, Energy Sources
• Data Structures - Arrays, Linked Lists, Stacks, Queues, Trees, Graphs, Sorting
• Basic Electronics - Diodes, BJT, FET, Amplifiers, Rectifiers
• Python Programming Lab - Python basics, Lists, Dictionaries, Functions, GUI""",

    # II YEAR I SEMESTER
    "ii_year_i_sem": """📚 **II YEAR I SEMESTER (R25) - 22 Credits**

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
| SDC | Data Visualization (Power BI/Tableau) | 1 |

**Detailed Subjects:**
• Java Programming - OOP concepts, Inheritance, Exception handling, Multithreading, JDBC
• Web Programming - HTML, CSS, JavaScript, React, Node.js
• Introduction to IoT - IoT Architecture, Sensors, Raspberry Pi, Cloud Integration
• Computer Organization - CPU, Memory, I/O, 8086 Microprocessor
• Data Visualization - Power BI, Tableau, Google Charts""",

    # II YEAR II SEMESTER
    "ii_year_ii_sem": """📚 **II YEAR II SEMESTER (R25) - 20 Credits**

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
| MC | Indian Knowledge System | 1 |

**Detailed Subjects:**
• Full Stack Development - MERN stack, Spring Boot, REST APIs
• Operating Systems - Process, Threads, Scheduling, Memory Management, File Systems
• Database Management Systems - SQL, Normalization, Transactions, Indexing
• Algorithm Design - Divide & Conquer, Greedy, Dynamic Programming, NP-Completeness
• UI Design - Flutter - Cross-platform mobile app development""",

    # III YEAR I SEMESTER
    "iii_year_i_sem": """📚 **III YEAR I SEMESTER (R25) - 21 Credits**

| Course | Subject | Credits |
|--------|---------|---------|
| PC | Software Engineering | 3 |
| PC | Machine Learning | 3 |
| PC | Data Communications and Computer Networks | 3 |
| PE1 | Professional Elective-I (Any one) | 3 |
|     | • Distributed Systems | |
|     | • Artificial Intelligence | |
|     | • Number Theory & Cryptography | |
|     | • Optimization Techniques | |
| OE1 | Open Elective-I | 2 |
| Lab | Software Engineering Lab | 1 |
| Lab | Machine Learning Lab | 1 |
| Lab | Computer Networks Lab | 1 |
| PW | Field Based Project/Internship | 2 |
| SDC | Prompt Engineering | 1 |
| MC | Gender Sensitization/Human Values | 1 |

**Detailed Subjects:**
• Software Engineering - SDLC, Agile, UML, Testing
• Machine Learning - Supervised/Unsupervised Learning, Regression, Classification
• Computer Networks - OSI Model, TCP/IP, Routing, Congestion Control""",

    # III YEAR II SEMESTER
    "iii_year_ii_sem": """📚 **III YEAR II SEMESTER (R25) - 20 Credits**

| Course | Subject | Credits |
|--------|---------|---------|
| PC | Information Security | 3 |
| PC | Automata & Compiler Design | 3 |
| HSC | Business Economics and Financial Analysis | 3 |
| PE2 | Professional Elective-II (Any one) | 3 |
|     | • High Performance Computing | |
|     | • Deep Learning | |
|     | • Web Security | |
|     | • Software Testing Methodology | |
| OE2 | Open Elective-II | 2 |
| Lab | Information Security Lab | 1 |
| Lab | Automata & Compiler Design Lab | 1 |
| Lab | Development Operations (DevOps) Lab | 1 |
| HSC | Employability and Soft Skills Lab | 1 |
| SDC | Big Data - Spark | 1 |
| MC | Environmental Science | 1 |

**Detailed Subjects:**
• Information Security - Cryptography, Network Security, Cyber Attacks
• Automata & Compiler Design - Finite Automata, Parsing, Code Optimization
• DevOps Lab - CI/CD, Docker, Kubernetes, Jenkins
• Deep Learning - Neural Networks, CNN, RNN, Transformers""",

    # IV YEAR I SEMESTER
    "iv_year_i_sem": """📚 **IV YEAR I SEMESTER (R25) - 21 Credits**

| Course | Subject | Credits |
|--------|---------|---------|
| PC | Cloud Computing | 3 |
| PC | Natural Language Processing | 3 |
| HSC | Fundamentals of Management | 3 |
| PE3 | Professional Elective-III (Any one) | 3 |
|     | • Distributed Databases | |
|     | • Data Analytics | |
|     | • Secure Coding Principles | |
|     | • Mobile Computing | |
| PE4 | Professional Elective-IV (Any one) | 3 |
|     | • Scalable Architecture for Large Apps | |
|     | • Data Mining | |
|     | • Blockchain Technology | |
|     | • 5G Technologies | |
| OE3 | Open Elective-III | 2 |
| Lab | Cloud Computing Lab | 1 |
| Lab | Natural Language Processing Lab | 1 |
| PW | Industry Oriented Mini Project/Internship | 2 |

**Detailed Subjects:**
• Cloud Computing - AWS, Azure, Virtualization, Serverless
• Natural Language Processing - Text Processing, N-Grams, Sentiment Analysis
• Blockchain Technology - Bitcoin, Ethereum, Smart Contracts, Hyperledger
• Data Mining - Association Rules, Classification, Clustering""",

    # IV YEAR II SEMESTER
    "iv_year_ii_sem": """📚 **IV YEAR II SEMESTER (R25) - 20 Credits**

| Course | Subject | Credits |
|--------|---------|---------|
| PE5 | Professional Elective-V (Any one) | 3 |
|     | • Edge/Fog Computing | |
|     | • Reinforcement Learning | |
|     | • Cloud Security | |
|     | • Quantum Computing | |
| PE6 | Professional Elective-VI (Any one) | 3 |
|     | • Augmented Reality & Virtual Reality | |
|     | • Generative AI | |
|     | • Digital Forensics | |
|     | • Storage Area Networks | |
| PW | Project Work | 14 |

**Detailed Subjects:**
• Project Work - Major final year project (14 credits)
• Generative AI - LLMs, GPT, Diffusion Models, Prompt Engineering
• Reinforcement Learning - Markov Decision Process, Q-Learning
• AR/VR - Unity/Unreal, 3D Modeling, Immersive Experiences
• Quantum Computing - Qubits, Quantum Gates, Shor's Algorithm""",

    "attendance": """📊 **ATTENDANCE REQUIREMENTS (R25):**

• Minimum 75% attendance required to appear for exams
• Shortage up to 10% (65-74%) can be condoned
• Below 65% → NO condonation, detained
• Two hours attendance counted if appears for mid-term exam""",

    "grading": """🎯 **GRADING SYSTEM (R25):**

| % Marks | Grade | Grade Points |
|---------|-------|--------------|
| ≥ 90% | O | 10 |
| 80-89% | A+ | 9 |
| 70-79% | A | 8 |
| 60-69% | B+ | 7 |
| 50-59% | B | 6 |
| 40-49% | C | 5 |
| < 40% | F | 0 |

**Passing:** 35% in CIE, 35% in SEE, overall 40%""",

    "sgpa_cgpa": """📊 **SGPA & CGPA CALCULATION:**

**SGPA** = Σ(Credit × Grade Point) / Σ(Credits)
**CGPA** = Σ(Credit Points for best 160 credits) / Σ(Credits)
**Percentage** = (CGPA - 0.5) × 10

**Class Classification:**
• First Class with Distinction: CGPA ≥ 7.5
• First Class: CGPA ≥ 6.5
• Second Class: CGPA ≥ 5.5
• Pass Class: CGPA ≥ 5.0""",

    "exam_pattern": """📝 **EXAM PATTERN (R25):**

**Theory Courses (100 marks):**
• CIE: 40 marks (2 Mid-Terms avg:30, Assignments:5, Viva:5)
• SEE: 60 marks (Part-A:10, Part-B:50)
• Duration: 3 hours

**Practical Courses:**
• CIE: 40 marks
• SEE: 60 marks (conducted by two examiners)""",

    "open_electives": """📚 **OPEN ELECTIVES OFFERED:**

**By CSE:** OS Fundamentals, SQL, Computer Networks, Software Engineering
**By IT:** Java Programming, Scripting Languages, Full Stack, DBMS, Big Data, DevOps
**By CSM/CSD:** AI Fundamentals, Machine Learning, Data Mining, R Programming, NLP
**By ECE:** Biomedical Electronics, Image Processing, Wearable Devices
**By H&M:** IPR, Investment, Operations Research, Marketing Management"""
}

def get_response(question):
    q = question.lower().strip()
    
    # Greetings
    if re.search(r'^(hi|hello|hey|namaste)', q):
        return "Hello! 👋 I'm GNITS IT Syllabus Assistant. Ask me about:\n\n• 📚 I, II, III, IV Year IT syllabus\n• 📝 Exam Pattern & Grading\n• 🎯 Attendance Rules\n• 💻 Professional Electives\n• 🔓 Open Electives\n\nWhat would you like to know?"
    
    # I Year
    if re.search(r'(i year|1st year|first year|semester 1|semester i|i-i)', q):
        return IT_SYLLABUS["i_year_i_sem"]
    if re.search(r'(i year ii|1st year 2nd|i-ii|second semester first year)', q):
        return IT_SYLLABUS["i_year_ii_sem"]
    
    # II Year
    if re.search(r'(ii year|2nd year|second year|ii-i|ii year i)', q):
        return IT_SYLLABUS["ii_year_i_sem"]
    if re.search(r'(ii year ii|2nd year 2nd|ii-ii)', q):
        return IT_SYLLABUS["ii_year_ii_sem"]
    
    # III Year
    if re.search(r'(iii year|3rd year|third year|iii-i)', q):
        return IT_SYLLABUS["iii_year_i_sem"]
    if re.search(r'(iii year ii|3rd year 2nd|iii-ii)', q):
        return IT_SYLLABUS["iii_year_ii_sem"]
    
    # IV Year
    if re.search(r'(iv year|4th year|fourth year|final year|iv-i)', q):
        return IT_SYLLABUS["iv_year_i_sem"]
    if re.search(r'(iv year ii|4th year 2nd|final semester|iv-ii)', q):
        return IT_SYLLABUS["iv_year_ii_sem"]
    
    # Attendance
    if re.search(r'(attendance|absent|condonation|75%)', q):
        return IT_SYLLABUS["attendance"]
    
    # Grading
    if re.search(r'(grade|grading|gpa|sgpa|cgpa|percentage|class)', q):
        return IT_SYLLABUS["grading"] + "\n\n" + IT_SYLLABUS["sgpa_cgpa"]
    
    # Exam pattern
    if re.search(r'(exam|mid|see|cie|evaluation|marks)', q):
        return IT_SYLLABUS["exam_pattern"]
    
    # Open Electives
    if re.search(r'(open elective|oe)', q):
        return IT_SYLLABUS["open_electives"]
    
    # Professional Electives
    if re.search(r'(professional elective|pe)', q):
        return """📚 **PROFESSIONAL ELECTIVES (R25 IT):**

**PE-1 (III-I):** Distributed Systems | AI | Number Theory & Cryptography | Optimization Techniques
**PE-2 (III-II):** High Performance Computing | Deep Learning | Web Security | Software Testing
**PE-3 (IV-I):** Distributed Databases | Data Analytics | Secure Coding | Mobile Computing
**PE-4 (IV-I):** Scalable Architecture | Data Mining | Blockchain | 5G Technologies
**PE-5 (IV-II):** Edge/Fog Computing | Reinforcement Learning | Cloud Security | Quantum Computing
**PE-6 (IV-II):** AR/VR | Generative AI | Digital Forensics | Storage Area Networks"""
    
    # Year overview
    if re.search(r'(all years|complete syllabus|full syllabus)', q):
        return """📚 **COMPLETE IT SYLLABUS OVERVIEW (R25):**

**I Year:** Matrices, Physics, C Programming, Data Structures, Python, Electronics
**II Year:** Java, Web Programming, IoT, OS, DBMS, Full Stack, Algorithm Design
**III Year:** Software Engineering, Machine Learning, Networks, Security, DevOps, Deep Learning
**IV Year:** Cloud Computing, NLP, Blockchain, Project Work, Generative AI

Ask me about specific semesters for detailed subjects!"""
    
    # Default
    return """😊 **I'm GNITS IT Syllabus Assistant (R25)!**

Ask me about:

📚 **COURSE STRUCTURE**
• I Year - I & II Sem (Basic Sciences, Programming)
• II Year - I & II Sem (Core IT subjects)
• III Year - I & II Sem (Advanced IT)
• IV Year - I & II Sem (Specializations, Project)

📋 **ACADEMIC RULES**
• Attendance (75% required)
• Grading system (O to F)
• SGPA/CGPA calculation
• Exam pattern

🎓 **ELECTIVES**
• Professional Electives (PE1-PE6)
• Open Electives (OE1-OE3)

**Try asking:**
• "What are I year IT subjects?"
• "Tell me about III year II semester"
• "List professional electives"
• "Attendance requirement?" """

# Initialize session
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'current_page' not in st.session_state:
    st.session_state.current_page = "Chat"
if 'selected_syllabus' not in st.session_state:
    st.session_state.selected_syllabus = None

# Sidebar Navigation
with st.sidebar:
    st.markdown("### 💻 Navigation")
    
    # Chat option
    if st.button("💬 Chat with Assistant", use_container_width=True):
        st.session_state.current_page = "Chat"
        st.rerun()
    
    st.markdown("---")
    st.markdown("### 📚 IT Syllabus")
    
    # Syllabus navigation buttons
    syllabus_options = {
        "📖 I Year I Sem": "i_year_i_sem",
        "📖 I Year II Sem": "i_year_ii_sem",
        "📖 II Year I Sem": "ii_year_i_sem",
        "📖 II Year II Sem": "ii_year_ii_sem",
        "📖 III Year I Sem": "iii_year_i_sem",
        "📖 III Year II Sem": "iii_year_ii_sem",
        "📖 IV Year I Sem": "iv_year_i_sem",
        "📖 IV Year II Sem": "iv_year_ii_sem",
        "📋 Attendance Rules": "attendance",
        "🎯 Grading System": "grading",
        "📝 Exam Pattern": "exam_pattern"
    }
    
    for label, key in syllabus_options.items():
        if st.button(label, use_container_width=True):
            st.session_state.current_page = "Syllabus"
            st.session_state.selected_syllabus = key
            st.rerun()
    
    st.markdown("---")
    
    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# Main content area
if st.session_state.current_page == "Chat":
    # Chat interface
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
                    <strong>💻 IT Assistant</strong><br>{msg["content"]}
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    # Chat input
    question = st.chat_input("Ask about IT syllabus, courses, rules...")
    
    if question:
        st.session_state.messages.append({"role": "user", "content": question})
        response = get_response(question)
        st.session_state.messages.append({"role": "assistant", "content": response})
        st.rerun()
    
    if not st.session_state.messages:
        st.info("👋 **Hello!** I'm your GNITS IT Syllabus Assistant. Ask me about I, II, III, IV year IT subjects, semester-wise syllabus, electives, attendance rules, grading system, or exam pattern! 💻")

elif st.session_state.current_page == "Syllabus" and st.session_state.selected_syllabus:
    # Display syllabus content
    content = IT_SYLLABUS.get(st.session_state.selected_syllabus, "Syllabus not found")
    st.markdown(content)
    
    # Back button
    if st.button("← Back to Chat", use_container_width=True):
        st.session_state.current_page = "Chat"
        st.rerun()
