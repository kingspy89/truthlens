import streamlit as st
import pandas as pd
from datetime import datetime

def educational_interface():
    """Educational resources and training modules"""
    
    st.title("🎓 TruthLens Education Hub")
    st.markdown("**Learn to identify misinformation and improve digital literacy**")
    
    # Education tabs
    tabs = st.tabs([
        "📚 Learning Modules",
        "🧠 Interactive Quiz", 
        "📊 Case Studies",
        "🎯 Training Center",
        "📖 Resources"
    ])
    
    with tabs:
        learning_modules()
    
    with tabs:
        interactive_quiz()
    
    with tabs:
        case_studies()
    
    with tabs:
        training_center()
    
    with tabs:
        educational_resources()

def learning_modules():
    """Interactive learning modules"""
    st.subheader("📚 Digital Literacy Learning Modules")
    
    # Module categories
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown("**Choose a Learning Path:**")
        
        learning_paths = {
            "🔰 Beginner": "Basic misinformation identification",
            "📈 Intermediate": "Advanced analysis techniques", 
            "🎖️ Expert": "Professional investigation methods",
            "👮 Authority": "Law enforcement protocols"
        }
        
        selected_path = st.selectbox("Learning Level", list(learning_paths.keys()))
        st.info(learning_paths[selected_path])
    
    with col2:
        st.markdown(f"**{selected_path} Learning Modules:**")
        
        if "Beginner" in selected_path:
            modules = [
                "📍 What is Misinformation?",
                "🔍 Basic Fact-Checking Techniques",
                "📱 Social Media Literacy",
                "🧠 Cognitive Biases and You",
                "✅ Reliable Source Identification"
            ]
        elif "Intermediate" in selected_path:
            modules = [
                "🔬 Advanced Analysis Methods",
                "🖼️ Image and Video Verification",
                "📊 Statistical Manipulation Detection",
                "🌐 Cross-Platform Investigation",
                "⚖️ Legal and Ethical Considerations"
            ]
        elif "Expert" in selected_path:
            modules = [
                "🕵️ Digital Forensics Techniques",
                "🧬 Psychological Warfare Tactics",
                "🌍 Geopolitical Context Analysis",
                "🤖 AI-Generated Content Detection",
                "📋 Evidence Documentation"
            ]
        else:  # Authority
            modules = [
                "👮 Law Enforcement Protocols",
                "⚖️ Legal Framework and Rights",
                "🚨 Emergency Response Procedures",
                "📊 Threat Assessment Methods",
                "🤝 Inter-Agency Coordination"
            ]
        
        for i, module in enumerate(modules, 1):
            with st.expander(f"Module {i}: {module}"):
                st.write("**Learning Objectives:**")
                st.write("- Understand key concepts and terminology")
                st.write("- Practice hands-on identification techniques")
                st.write("- Complete assessment quiz")
                st.write("- Apply knowledge to real-world scenarios")
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.button(f"▶️ Start Module {i}", key=f"start_{i}")
                with col2:
                    progress = min(i * 20, 100)
                    st.write(f"Progress: {progress}%")
                    st.progress(progress / 100)
                with col3:
                    if progress == 100:
                        st.success("✅ Completed")
                    else:
                        st.info("📚 Available")

def interactive_quiz():
    """Interactive knowledge assessment quiz"""
    st.subheader("🧠 Misinformation Detection Quiz")
    
    if 'quiz_started' not in st.session_state:
        st.session_state.quiz_started = False
        st.session_state.current_question = 0
        st.session_state.score = 0
        st.session_state.answers = []
    
    # Quiz questions database
    quiz_questions = [
        {
            "question": "Which of the following is a common red flag for misinformation?",
            "options": [
                "Multiple credible sources cited",
                "Emotional language and urgent calls to action",
                "Author's credentials clearly displayed",
                "Publication date is recent"
            ],
            "correct": 1,
            "explanation": "Emotional language and urgent calls to action are classic manipulation tactics used in misinformation to bypass critical thinking."
        },
        {
            "question": "When fact-checking an image, what should you do first?",
            "options": [
                "Share it immediately if it looks real",
                "Check the image's metadata and reverse search",
                "Only verify if someone else shared it",
                "Assume it's fake if it's shocking"
            ],
            "correct": 1,
            "explanation": "Always perform a reverse image search and check metadata before drawing conclusions about an image's authenticity."
        },
        {
            "question": "What is 'confirmation bias' in the context of misinformation?",
            "options": [
                "The tendency to create false information",
                "The process of fact-checking claims",
                "The tendency to favor information that confirms existing beliefs",
                "A type of AI bias in detection systems"
            ],
            "correct": 2,
            "explanation": "Confirmation bias makes people more likely to believe and share information that aligns with their existing views, regardless of accuracy."
        },
        {
            "question": "Which source would be MOST reliable for health information?",
            "options": [
                "A random blog post",
                "Your friend's Facebook post",
                "Peer-reviewed medical journal",
                "Celebrity endorsement"
            ],
            "correct": 2,
            "explanation": "Peer-reviewed medical journals undergo rigorous scientific review and are the most reliable source for health information."
        },
        {
            "question": "What should you do when you encounter potential misinformation?",
            "options": [
                "Share it immediately to warn others",
                "Ignore it completely",
                "Verify before sharing and report if confirmed false",
                "Only share with close friends"
            ],
            "correct": 2,
            "explanation": "Always verify information before sharing, and report confirmed misinformation to help prevent its spread."
        }
    ]
    
    if not st.session_state.quiz_started:
        st.markdown("**Test your knowledge of misinformation detection!**")
        st.info("This quiz contains 5 questions covering basic misinformation identification skills.")
        
        if st.button("🚀 Start Quiz", type="primary"):
            st.session_state.quiz_started = True
            st.rerun()
    
    elif st.session_state.current_question < len(quiz_questions):
        # Current question
        q = quiz_questions[st.session_state.current_question]
        
        st.markdown(f"**Question {st.session_state.current_question + 1} of {len(quiz_questions)}:**")
        st.markdown(f"### {q['question']}")
        
        # Answer options
        selected_answer = st.radio(
            "Choose your answer:",
            q['options'],
            key=f"q_{st.session_state.current_question}"
        )
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("Submit Answer", type="primary"):
                # Check answer
                selected_index = q['options'].index(selected_answer)
                is_correct = selected_index == q['correct']
                
                if is_correct:
                    st.success("✅ Correct!")
                    st.session_state.score += 1
                else:
                    st.error("❌ Incorrect")
                
                st.info(f"**Explanation:** {q['explanation']}")
                st.session_state.answers.append({
                    'question': q['question'],
                    'selected': selected_answer,
                    'correct': q['options'][q['correct']],
                    'is_correct': is_correct
                })
                
                st.session_state.current_question += 1
                
                if st.button("Next Question →"):
                    st.rerun()
        
        with col2:
            progress = (st.session_state.current_question + 1) / len(quiz_questions)
            st.progress(progress)
            st.write(f"Progress: {st.session_state.current_question + 1}/{len(quiz_questions)}")
    
    else:
        # Quiz completed
        st.success("🎉 Quiz Completed!")
        
        score_percentage = (st.session_state.score / len(quiz_questions)) * 100
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Final Score", f"{st.session_state.score}/{len(quiz_questions)}")
        with col2:
            st.metric("Percentage", f"{score_percentage:.1f}%")
        with col3:
            if score_percentage >= 80:
                st.success("🏆 Excellent!")
            elif score_percentage >= 60:
                st.info("👍 Good Job!")
            else:
                st.warning("📚 Keep Learning!")
        
        # Show detailed results
        st.subheader("📊 Detailed Results")
        
        for i, answer in enumerate(st.session_state.answers, 1):
            with st.expander(f"Question {i}: {'✅' if answer['is_correct'] else '❌'}"):
                st.write(f"**Question:** {answer['question']}")
                st.write(f"**Your Answer:** {answer['selected']}")
                st.write(f"**Correct Answer:** {answer['correct']}")
                
                if answer['is_correct']:
                    st.success("Correct! ✅")
                else:
                    st.error("Incorrect ❌")
        
        if st.button("🔄 Retake Quiz"):
            # Reset quiz state
            st.session_state.quiz_started = False
            st.session_state.current_question = 0
            st.session_state.score = 0
            st.session_state.answers = []
            st.rerun()

def case_studies():
    """Real-world case studies and examples"""
    st.subheader("📊 Real-World Case Studies")
    
    case_study_categories = st.selectbox(
        "Select Case Study Category:",
        ["🏥 Health Misinformation", "🗳️ Election Misinformation", "🌍 Climate Change Denial", "💰 Financial Scams", "🚨 Crisis Misinformation"]
    )
    
    if "Health" in case_study_categories:
        display_health_case_study()
    elif "Election" in case_study_categories:
        display_election_case_study()
    elif "Climate" in case_study_categories:
        display_climate_case_study()
    elif "Financial" in case_study_categories:
        display_financial_case_study()
    else:
        display_crisis_case_study()

def display_health_case_study():
    """Health misinformation case study"""
    st.markdown("### 🏥 Case Study: COVID-19 Vaccine Misinformation")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        **Background:**
        During the COVID-19 pandemic, false claims about vaccines spread rapidly on social media, 
        including statements about microchips, DNA alteration, and exaggerated side effects.
        
        **The Claim:**
        "COVID-19 vaccines contain microchips for government tracking and alter your DNA permanently."
        
        **Red Flags Identified:**
        - Lack of credible scientific sources
        - Appeal to fear and paranoia
        - Contradicts established scientific consensus
        - Uses absolute language without nuance
        """)
    
    with col2:
        st.info("""
        **Learning Points:**
        - Always check medical claims against peer-reviewed research
        - Be wary of health advice from non-medical sources
        - Understand the difference between correlation and causation
        - Verify through official health organizations
        """)
    
    st.markdown("""
    **Fact-Check Results:**
    - ❌ **Microchips:** No evidence of microchips in any approved vaccine
    - ❌ **DNA Alteration:** mRNA vaccines don't enter cell nucleus where DNA is stored
    - ✅ **Side Effects:** Real but typically mild and temporary
    - ✅ **Efficacy:** Proven effective in preventing severe disease
    
    **Impact:** This misinformation contributed to vaccine hesitancy and potentially preventable deaths.
    
    **How to Verify Health Claims:**
    1. Check WHO, CDC, or your national health authority
    2. Look for peer-reviewed research on PubMed
    3. Consult with healthcare professionals
    4. Be skeptical of miracle cures or conspiracy theories
    """)

def display_election_case_study():
    """Election misinformation case study"""
    st.markdown("### 🗳️ Case Study: Election Fraud Claims")
    
    st.markdown("""
    **Background:**
    False claims about election fraud can undermine democratic processes and public trust.
    
    **Common Misinformation Tactics:**
    - Cherry-picking isolated incidents
    - Misrepresenting normal election processes
    - Using emotional language to create urgency
    - Spreading unverified claims from unreliable sources
    
    **Verification Process:**
    1. Check with official election authorities
    2. Cross-reference with multiple credible news sources
    3. Look for evidence from independent election observers
    4. Understand the legal processes for challenging results
    """)

def display_climate_case_study():
    """Climate change denial case study"""
    st.markdown("### 🌍 Case Study: Climate Change Misinformation")
    
    st.markdown("""
    **Background:**
    Climate change misinformation often uses selective data presentation and appeals to economic fears.
    
    **Common Denial Tactics:**
    - Cherry-picking short-term weather events
    - Misrepresenting scientific uncertainty
    - False balance in media coverage
    - Economic fear-mongering about climate action
    
    **Scientific Consensus:**
    97% of climate scientists agree that human activities are the primary driver of recent climate change.
    """)

def display_financial_case_study():
    """Financial scam case study"""
    st.markdown("### 💰 Case Study: Cryptocurrency Scams")
    
    st.markdown("""
    **Background:**
    Get-rich-quick schemes often use misinformation to lure victims into financial scams.
    
    **Warning Signs:**
    - Promises of guaranteed high returns
    - Pressure to act quickly
    - Celebrity endorsements (often fake)
    - Lack of regulatory compliance
    - Request for upfront payments
    """)

def display_crisis_case_study():
    """Crisis misinformation case study"""
    st.markdown("### 🚨 Case Study: Natural Disaster Misinformation")
    
    st.markdown("""
    **Background:**
    During emergencies, false information can spread rapidly and potentially endanger lives.
    
    **Common Crisis Misinformation:**
    - False evacuation orders
    - Fake damage reports
    - Rumors about government response
    - Scam charity appeals
    
    **Verification During Crisis:**
    - Check official emergency management sources
    - Verify through local news media
    - Be cautious of social media rumors
    - Report false information to authorities
    """)

def training_center():
    """Training center for different user groups"""
    st.subheader("🎯 Professional Training Center")
    
    training_programs = st.selectbox(
        "Select Training Program:",
        ["👤 General Public", "📰 Journalists", "🎓 Educators", "👮 Law Enforcement", "🏢 Corporate Teams"]
    )
    
    if "General Public" in training_programs:
        st.markdown("""
        ### 👤 Public Digital Literacy Training
        
        **Program Overview:**
        A comprehensive program to help citizens identify and combat misinformation.
        
        **Training Modules:**
        1. **Basic Media Literacy** (2 hours)
           - Understanding information sources
           - Identifying bias and manipulation
        
        2. **Fact-Checking Fundamentals** (3 hours)
           - Using fact-checking websites
           - Verifying images and videos
           - Cross-referencing sources
        
        3. **Social Media Awareness** (2 hours)
           - Understanding algorithms and filter bubbles
           - Responsible sharing practices
        
        **Certification:** Digital Literacy Certificate upon completion
        """)
    
    elif "Journalists" in training_programs:
        st.markdown("""
        ### 📰 Journalism Misinformation Training
        
        **Specialized Training for Media Professionals**
        
        **Advanced Modules:**
        1. **Advanced Verification Techniques** (4 hours)
        2. **Open Source Intelligence (OSINT)** (6 hours)
        3. **Ethical Reporting on Misinformation** (3 hours)
        4. **Digital Forensics for Newsrooms** (5 hours)
        
        **Tools Training:**
        - Reverse image search techniques
        - Video verification tools
        - Social media investigation
        - Blockchain verification
        """)
    
    elif "Educators" in training_programs:
        st.markdown("""
        ### 🎓 Educator Training Program
        
        **Teaching Digital Literacy in Schools**
        
        **Curriculum Development:**
        - Age-appropriate misinformation education
        - Interactive classroom activities
        - Assessment strategies
        - Parent engagement approaches
        
        **Resource Package:**
        - Lesson plans and worksheets
        - Video resources
        - Student assessment tools
        - Parent information packets
        """)
    
    elif "Law Enforcement" in training_programs:
        st.markdown("""
        ### 👮 Law Enforcement Training
        
        **Misinformation Investigation Protocols**
        
        **Specialized Training:**
        1. **Digital Evidence Collection** (8 hours)
        2. **Social Media Investigation** (6 hours)
        3. **Legal Framework and Rights** (4 hours)
        4. **Threat Assessment** (5 hours)
        5. **Inter-agency Coordination** (3 hours)
        
        **Certification:** Law Enforcement Digital Investigation Certificate
        """)
    
    else:  # Corporate
        st.markdown("""
        ### 🏢 Corporate Misinformation Training
        
        **Protecting Your Organization**
        
        **Business-Focused Training:**
        - Brand protection from misinformation
        - Employee social media guidelines
        - Crisis communication strategies
        - Vendor and partner verification
        
        **Risk Management:**
        - Reputation monitoring
        - Incident response planning
        - Legal considerations
        - Insurance implications
        """)
    
    # Registration form
    st.subheader("📝 Training Registration")
    
    with st.form("training_registration"):
        col1, col2 = st.columns(2)
        
        with col1:
            name = st.text_input("Full Name")
            email = st.text_input("Email Address")
            organization = st.text_input("Organization/Company")
        
        with col2:
            phone = st.text_input("Phone Number")
            experience = st.selectbox("Experience Level", ["Beginner", "Intermediate", "Advanced"])
            preferred_format = st.selectbox("Preferred Format", ["Online", "In-Person", "Hybrid"])
        
        additional_info = st.text_area("Additional Information or Special Requirements")
        
        if st.form_submit_button("📝 Register for Training", type="primary"):
            st.success(f"✅ Registration submitted successfully!")
            st.info(f"We'll contact you at {email} within 2 business days with training details.")

def educational_resources():
    """Educational resources and references"""
    st.subheader("📖 Educational Resources & References")
    
    resource_tabs = st.tabs([
        "🔗 Useful Links",
        "📚 Recommended Reading", 
        "🎥 Video Resources",
        "🛠️ Tools & Websites",
        "📊 Research Papers"
    ])
    
    with resource_tabs:
        st.markdown("""
        ### 🔗 Essential Links for Fact-Checking
        
        **Fact-Checking Organizations:**
        - [Snopes](https://www.snopes.com/) - General fact-checking
        - [FactCheck.org](https://www.factcheck.org/) - Political fact-checking
        - [PolitiFact](https://www.politifact.com/) - Political claims verification
        - [AP Fact Check](https://apnews.com/hub/ap-fact-check) - Associated Press fact-checking
        
        **Media Literacy Organizations:**
        - [Common Sense Media](https://www.commonsensemedia.org/) - Digital citizenship
        - [News Literacy Project](https://newslit.org/) - News literacy education
        - [First Draft](https://firstdraftnews.org/) - Verification training
        
        **Government Resources:**
        - [CISA - Misinformation](https://www.cisa.gov/topics/election-security/misinformation-disinformation-and-malinformation) - Official cybersecurity guidance
        - [FTC Consumer Information](https://consumer.ftc.gov/) - Scam and fraud prevention
        """)
    
    with resource_tabs:
        st.markdown("""
        ### 📚 Recommended Reading
        
        **Books:**
        - "The Misinformation Age" by Cailin O'Connor and James Owen Weatherall
        - "Factfulness" by Hans Rosling
        - "The Death of Expertise" by Tom Nichols
        - "Network Propaganda" by Yochai Benkler, Robert Faris, and Hal Roberts
        
        **Academic Articles:**
        - "The Science of Fake News" - Science Magazine
        - "Misinformation and Its Correction" - Psychological Science in the Public Interest
        - "The Spread of True and False News Online" - Science Magazine
        """)
    
    with resource_tabs:
        st.markdown("""
        ### 🎥 Educational Videos
        
        **Documentary Recommendations:**
        - "The Social Dilemma" (Netflix) - Social media and misinformation
        - "After Truth: Disinformation and the Cost of Fake News" (HBO)
        - "The Great Hack" (Netflix) - Data manipulation and elections
        
        **Educational Channels:**
        - Crash Course Media Literacy
        - TED-Ed Critical Thinking Series
        - BBC Reality Check
        """)
    
    with resource_tabs:
        st.markdown("""
        ### 🛠️ Verification Tools & Websites
        
        **Image Verification:**
        - [TinEye](https://tineye.com/) - Reverse image search
        - [Google Images](https://images.google.com/) - Reverse image search
        - [InVID](https://www.invid-project.eu/tools-and-services/invid-verification-plugin/) - Video verification
        
        **Social Media Verification:**
        - [Hoaxy](https://hoaxy.osome.iu.edu/) - Track claim spread
        - [Botometer](https://botometer.osome.iu.edu/) - Bot detection
        - [CrowdTangle](https://www.crowdtangle.com/) - Social media monitoring
        
        **Website Analysis:**
        - [Whois Lookup](https://whois.net/) - Domain information
        - [Archive.org](https://archive.org/) - Website history
        - [AllSides](https://www.allsides.com/) - Media bias ratings
        """)
    
    with resource_tabs:
        st.markdown("""
        ### 📊 Research Papers & Studies
        
        **Recent Research:**
        - "Misinformation in Social Media: Definition, Manipulation, and Detection" (2021)
        - "The COVID-19 'Infodemic': How Misinformation Spreads" (2020)
        - "Psychological Factors in Misinformation Spread" (2021)
        - "AI-Generated Text and the Future of Misinformation" (2023)
        
        **Data Sources:**
        - MIT Misinformation Database
        - Reuters Institute Digital News Report
        - Pew Research Center Internet & Technology
        - Oxford Internet Institute Research
        """)
    
    # Resource request form
    st.subheader("📝 Request Additional Resources")
    
    with st.form("resource_request"):
        resource_type = st.selectbox("What type of resource are you looking for?", 
                                   ["Training Materials", "Research Papers", "Tools", "Case Studies", "Other"])
        topic = st.text_input("Specific Topic or Area of Interest")
        description = st.text_area("Describe what you need help with")
        contact_email = st.text_input("Your Email (for response)")
        
        if st.form_submit_button("📝 Submit Request"):
            st.success("✅ Resource request submitted! We'll respond within 3 business days.")
