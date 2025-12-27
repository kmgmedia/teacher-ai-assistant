"""
AI Teaching Assistant - Streamlit Dashboard
User-friendly interface for teachers to generate lesson notes, reports, and parent messages.
Version: 2.0 - With Analytics Dashboard and Multi-Teacher Support
"""
import streamlit as st
import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Page configuration
st.set_page_config(
    page_title="AI Teaching Assistant",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Import core modules
from core.logic.lesson_generator import generate_lesson
from core.logic.report_generator import generate_report
from core.logic.parent_writer import generate_parent_message
from core.logic.analytics import (
    calculate_class_statistics,
    get_subject_performance,
    get_grade_performance,
    get_top_students,
    get_struggling_students,
    get_behavior_distribution,
    get_teacher_performance
)
from integrations.google_sheets import read_student_data, get_student_by_name, write_report_to_sheet

# =====================================================
# PERFORMANCE OPTIMIZATION: Data Caching
# =====================================================

@st.cache_data(ttl=300)  # Cache for 5 minutes
def load_students_cached():
    """
    Load student data with caching to avoid repeated API calls.
    Cache refreshes every 5 minutes.
    Returns empty list if not configured or on error.
    """
    try:
        # Check if Google Sheets is configured
        from config import settings
        if not settings.GOOGLE_SHEETS_CREDENTIALS or not settings.GOOGLE_SHEET_ID:
            return []
        data = read_student_data()
        return data if data else []
    except Exception as e:
        # Silently return empty list on error - don't crash the app
        return []

@st.cache_data(ttl=300)
def get_student_cached(student_name):
    """
    Get individual student data with caching.
    Returns None if not found or not configured.
    """
    try:
        # Check if Google Sheets is configured
        from config import settings
        if not settings.GOOGLE_SHEETS_CREDENTIALS or not settings.GOOGLE_SHEET_ID:
            return None
        student = get_student_by_name(student_name)
        return student
    except Exception as e:
        # Silently return None on error
        return None

# Custom CSS
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .success-box {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        color: #155724;
    }
    .error-box {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #f8d7da;
        border: 1px solid #f5c6cb;
        color: #721c24;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if 'generated_content' not in st.session_state:
    st.session_state.generated_content = None

# Header
st.markdown('<h1 class="main-header">🎓 AI Teaching Assistant</h1>', unsafe_allow_html=True)
st.markdown("---")

# Sidebar navigation
st.sidebar.title("📋 Navigation")

# Check if Google Sheets is configured to show/hide View Students
from config import settings
sheets_configured = bool(settings.GOOGLE_SHEETS_CREDENTIALS and settings.GOOGLE_SHEET_ID)

# Teacher selector (if Google Sheets is configured)
if sheets_configured:
    st.sidebar.markdown("### 👨‍🏫 Select Teacher")
    try:
        # Load student data to get unique teachers
        import pandas as pd
        students_data = load_students_cached()
        if students_data and len(students_data) > 0:
            df_students = pd.DataFrame(students_data)
            if 'Teacher' in df_students.columns:
                teachers = sorted(df_students['Teacher'].unique().tolist())
                selected_teacher = st.sidebar.selectbox(
                    "View as:",
                    options=["All Teachers"] + teachers,
                    key="teacher_filter"
                )
                st.session_state['selected_teacher'] = selected_teacher
            else:
                st.session_state['selected_teacher'] = "All Teachers"
        else:
            st.session_state['selected_teacher'] = "All Teachers"
    except Exception as e:
        st.sidebar.warning(f"Could not load teachers: {e}")
        st.session_state['selected_teacher'] = "All Teachers"
    
    st.sidebar.markdown("---")

if sheets_configured:
    page_options = ["🏠 Home", "📊 Analytics", "📝 Lesson Generator", "📊 Report Generator", "💌 Parent Message", "👥 View Students"]
else:
    page_options = ["🏠 Home", "📝 Lesson Generator", "📊 Report Generator", "💌 Parent Message"]

page = st.sidebar.radio(
    "Choose a tool:",
    page_options
)

st.sidebar.markdown("---")
st.sidebar.info("💡 **Tip**: All generated content is automatically saved to the `data/output/` folder!")


# HOME PAGE
if page == "🏠 Home":
    st.header("Welcome to Your AI Teaching Assistant! 👋")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🎯 What Can I Do?")
        st.markdown("""
        - **📝 Generate Lesson Notes**: Create structured, engaging lesson plans
        - **📊 Write Student Reports**: Professional progress reports in seconds
        - **💌 Draft Parent Messages**: Personalized communication templates
        - **👥 Manage Students**: View and access student data from Google Sheets
        """)
    
    with col2:
        st.subheader("🚀 Quick Start")
        st.markdown("""
        1. **Select a tool** from the sidebar
        2. **Fill in the details** (or pull from Google Sheets)
        3. **Click Generate** and get instant results!
        4. **Copy or download** your content
        """)
    
    st.markdown("---")
    
    # Quick stats
    st.subheader("📈 Quick Stats")
    try:
        students = load_students_cached()  # Use cached data
        if students:
            col1, col2, col3 = st.columns(3)
            
            with col1:
                # Count unique students by name
                unique_names = set([s.get('Name', '') for s in students if s.get('Name')])
                st.metric("Total Students", len(unique_names))
            
            with col2:
                # Handle non-numeric scores safely
                scores = []
                for s in students:
                    try:
                        score = s.get('Score', 0)
                        if score:
                            scores.append(float(score))
                    except (ValueError, TypeError):
                        pass
                avg_score = sum(scores) / len(scores) if scores else 0
                st.metric("Average Score", f"{avg_score:.1f}")
            
            with col3:
                subjects = set([s.get('Subject', '') for s in students if s.get('Subject')])
                st.metric("Subjects", len(subjects))
        else:
            st.info("📊 No students loaded yet. Add students to your Google Sheet to see stats here.")
            
    except Exception as e:
        st.error(f"❌ Unable to load students: {str(e)}")


# ANALYTICS DASHBOARD PAGE
elif page == "📊 Analytics":
    st.header("📊 Analytics Dashboard")
    st.markdown("Comprehensive performance insights and trends")
    
    # Add refresh button
    col1, col2, col3 = st.columns([2, 1, 1])
    with col2:
        if st.button("🔄 Refresh Data", help="Clear cache and reload analytics", key="analytics_refresh"):
            st.cache_data.clear()
            st.success("Data refreshed!")
            st.rerun()
    
    try:
        import pandas as pd
        students_data = load_students_cached()
        
        if not students_data:
            st.info("📊 No data available. Add students to your Google Sheet to view analytics.")
        else:
            df = pd.DataFrame(students_data)
            
            # Apply teacher filter if selected
            selected_teacher = st.session_state.get('selected_teacher', 'All Teachers')
            if selected_teacher != "All Teachers" and 'Teacher' in df.columns:
                df = df[df['Teacher'] == selected_teacher]
                st.info(f"👨‍🏫 Showing analytics for: **{selected_teacher}**")
            
            if df.empty:
                st.warning("No data available for the selected teacher.")
            else:
                # Overall Statistics
                st.subheader("📈 Overall Performance")
                stats = calculate_class_statistics(df)
                
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("Total Students", stats.get('total_students', 0))
                with col2:
                    st.metric("Average Score", f"{stats.get('average_score', 0):.1f}")
                with col3:
                    st.metric("Median Score", f"{stats.get('median_score', 0):.1f}")
                with col4:
                    st.metric("Total Subjects", stats.get('total_subjects', 0))
                
                st.markdown("---")
                
                # Subject Performance
                col_left, col_right = st.columns(2)
                
                with col_left:
                    st.subheader("📚 Subject Performance")
                    subject_perf = get_subject_performance(df)
                    if not subject_perf.empty:
                        st.dataframe(subject_perf, hide_index=True, use_container_width=True)
                        
                        # Bar chart for subject averages
                        st.bar_chart(subject_perf.set_index('Subject')['Average'])
                    else:
                        st.info("No subject data available")
                
                with col_right:
                    st.subheader("🎓 Grade Performance")
                    grade_perf = get_grade_performance(df)
                    if not grade_perf.empty:
                        st.dataframe(grade_perf, hide_index=True, use_container_width=True)
                        
                        # Bar chart for grade averages
                        st.bar_chart(grade_perf.set_index('Grade')['Average Score'])
                    else:
                        st.info("No grade data available")
                
                st.markdown("---")
                
                # Top and Struggling Students
                col_top, col_struggling = st.columns(2)
                
                with col_top:
                    st.subheader("🌟 Top Performers")
                    top_n = st.slider("Show top", 3, 10, 5, key="top_slider")
                    top_students = get_top_students(df, n=top_n)
                    if not top_students.empty:
                        st.dataframe(top_students, hide_index=True, use_container_width=True)
                    else:
                        st.info("No student data available")
                
                with col_struggling:
                    st.subheader("🎯 Students Needing Support")
                    threshold = st.slider("Score threshold", 0, 100, 60, key="threshold_slider")
                    struggling = get_struggling_students(df, threshold=threshold, n=top_n)
                    if not struggling.empty:
                        st.dataframe(struggling, hide_index=True, use_container_width=True)
                    else:
                        st.success("All students are performing above threshold!")
                
                st.markdown("---")
                
                # Behavior Distribution
                st.subheader("😊 Behavior Overview")
                behavior_dist = get_behavior_distribution(df)
                if behavior_dist:
                    col1, col2 = st.columns([2, 1])
                    with col1:
                        # Display as bar chart
                        behavior_df = pd.DataFrame(list(behavior_dist.items()), columns=['Behavior', 'Count'])
                        st.bar_chart(behavior_df.set_index('Behavior'))
                    with col2:
                        # Display as table
                        st.dataframe(behavior_df, hide_index=True, use_container_width=True)
                else:
                    st.info("No behavior data available")
                
                # Teacher Comparison (only if All Teachers is selected)
                if selected_teacher == "All Teachers" and 'Teacher' in df.columns:
                    st.markdown("---")
                    st.subheader("👨‍🏫 Teacher Performance Comparison")
                    teacher_perf = get_teacher_performance(df)
                    if not teacher_perf.empty:
                        st.dataframe(teacher_perf, hide_index=True, use_container_width=True)
                        
                        # Bar chart for teacher averages
                        st.bar_chart(teacher_perf.set_index('Teacher')['Average Score'])
                    else:
                        st.info("No teacher data available")
    
    except Exception as e:
        st.error(f"❌ Error loading analytics: {str(e)}")
        import traceback
        with st.expander("Show error details"):
            st.code(traceback.format_exc())


# LESSON GENERATOR PAGE
elif page == "📝 Lesson Generator":
    st.header("📝 Lesson Note Generator")
    st.markdown("Create structured, age-appropriate lesson plans")
    
    col1, col2 = st.columns(2)
    
    with col1:
        subject = st.text_input("Subject *", placeholder="e.g., Mathematics, Science")
        topic = st.text_input("Topic *", placeholder="e.g., Introduction to Fractions")
        age_group = st.text_input("Age Group *", placeholder="e.g., 7-8 years (Grade 2)")
    
    with col2:
        duration = st.number_input("Duration (minutes)", min_value=15, max_value=180, value=60, step=15)
        objectives = st.text_area(
            "Learning Objectives *",
            placeholder="e.g., Students will understand what fractions are and identify halves and quarters",
            height=100
        )
    
    st.markdown("---")
    
    if st.button("🚀 Generate Lesson Note", type="primary", width="stretch"):
        if not subject or not topic or not age_group or not objectives:
            st.error("❌ Please fill in all required fields (marked with *)")
        else:
            with st.spinner("✨ Generating your lesson note..."):
                try:
                    result = generate_lesson(subject, topic, age_group, objectives, duration)
                    
                    if result['success']:
                        st.success("✅ Lesson note generated successfully!")
                        st.markdown("### 📄 Your Lesson Note:")
                        st.markdown(result['lesson_note'])
                        
                        # Download button
                        st.download_button(
                            label="⬇️ Download as Text File",
                            data=result['lesson_note'],
                            file_name=f"lesson_{subject}_{topic}.txt".replace(" ", "_"),
                            mime="text/plain"
                        )
                        
                        st.info(f"💾 Saved to: `{result['metadata']['output_file']}`")
                    else:
                        st.error(f"❌ Error: {result.get('error', 'Unknown error')}")
                        
                except Exception as e:
                    st.error(f"❌ An error occurred: {str(e)}")


# REPORT GENERATOR PAGE
elif page == "📊 Report Generator":
    st.header("📊 Student Report Generator")
    st.markdown("Create professional progress reports")
    
    # Check if Google Sheets is configured
    from config import settings
    sheets_available = bool(settings.GOOGLE_SHEETS_CREDENTIALS and settings.GOOGLE_SHEET_ID)
    
    # Option to load from Google Sheets (only if configured)
    if sheets_available:
        use_sheets = st.checkbox("📊 Load student data from Google Sheets", value=False)
    else:
        use_sheets = False
        st.info("ℹ️ Using manual input mode (Google Sheets not configured)")
    
    if use_sheets:
        try:
            students = load_students_cached()  # Use cached data
            
            # Get unique student names
            import pandas as pd
            df_all = pd.DataFrame(students)
            
            # Apply teacher filter if selected
            selected_teacher = st.session_state.get('selected_teacher', 'All Teachers')
            if selected_teacher != "All Teachers" and 'Teacher' in df_all.columns:
                df_all = df_all[df_all['Teacher'] == selected_teacher]
            
            unique_students = sorted(df_all['Name'].unique()) if 'Name' in df_all.columns else []
            
            selected_student = st.selectbox("Select Student *", unique_students)
            
            if selected_student:
                # Get all records for this student
                student_records = df_all[df_all['Name'] == selected_student] if 'Name' in df_all.columns else pd.DataFrame()
                
                # Aggregate data for the report
                all_subjects = student_records['Subject'].tolist() if 'Subject' in student_records.columns else []
                all_notes = student_records['Notes'].tolist() if 'Notes' in student_records.columns else []
                all_behaviors = student_records['Behavior'].tolist() if 'Behavior' in student_records.columns else []
                
                # Combine notes and behaviors
                combined_notes = "\n".join([f"- {subj}: {note}" for subj, note in zip(all_subjects, all_notes)])
                combined_behavior = "\n".join([f"- {subj}: {beh}" for subj, beh in zip(all_subjects, all_behaviors)])
                
                col1, col2 = st.columns(2)
                
                with col1:
                    student_name = st.text_input("Student Name *", value=selected_student)
                    period = st.text_input("Period *", value="Term 1 (2025)", placeholder="e.g., Term 1, Q2 2025")
                    subject = st.text_input("Subject *", value="Overall Progress", placeholder="e.g., Overall Progress or specific subject")
                
                with col2:
                    performance_notes = st.text_area(
                        "Performance Notes * (All Subjects)",
                        value=combined_notes if combined_notes else "No performance notes available",
                        height=150,
                        placeholder="Academic observations and achievements"
                    )
                    behavior_notes = st.text_area(
                        "Behavior Notes * (All Subjects)",
                        value=combined_behavior if combined_behavior else "No behavior notes available",
                        height=150,
                        placeholder="Social-emotional and behavioral observations"
                    )
                    save_to_sheets = st.checkbox("💾 Save report back to Google Sheets", value=True)
        
        except Exception as e:
            st.error(f"❌ Unable to load students from Google Sheets: {str(e)}")
            use_sheets = False
    
    if not use_sheets:
        col1, col2 = st.columns(2)
        
        with col1:
            student_name = st.text_input("Student Name *", placeholder="e.g., Emma Johnson")
            period = st.text_input("Period *", placeholder="e.g., Term 1, Q2 2025")
            subject = st.text_input("Subject *", placeholder="e.g., Overall Progress, Math")
        
        with col2:
            performance_notes = st.text_area(
                "Performance Notes *",
                height=100,
                placeholder="Academic observations and achievements"
            )
            behavior_notes = st.text_area(
                "Behavior Notes *",
                height=100,
                placeholder="Social-emotional and behavioral observations"
            )
            save_to_sheets = False
    
    st.markdown("---")
    
    if st.button("🚀 Generate Report", type="primary", width="stretch"):
        if not student_name or not period or not subject or not performance_notes or not behavior_notes:
            st.error("❌ Please fill in all required fields (marked with *)")
        else:
            with st.spinner("✨ Generating your report..."):
                try:
                    result = generate_report(student_name, period, subject, performance_notes, behavior_notes)
                    
                    if result['success']:
                        st.success("✅ Report generated successfully!")
                        st.markdown("### 📄 Progress Report:")
                        st.markdown(result['report'])
                        
                        # Save to sheets if requested
                        if save_to_sheets:
                            try:
                                write_report_to_sheet(result['report'], student_name)
                                st.success("✅ Report saved to Google Sheets!")
                            except Exception as e:
                                st.warning(f"⚠️ Could not save to sheets: {str(e)}")
                        
                        # Download button
                        st.download_button(
                            label="⬇️ Download Report",
                            data=result['report'],
                            file_name=f"report_{student_name}_{period}.txt".replace(" ", "_"),
                            mime="text/plain"
                        )
                        
                        st.info(f"💾 Saved to: `{result['metadata']['output_file']}`")
                    else:
                        st.error(f"❌ Error: {result.get('error', 'Unknown error')}")
                        
                except Exception as e:
                    st.error(f"❌ An error occurred: {str(e)}")


# PARENT MESSAGE PAGE
elif page == "💌 Parent Message":
    st.header("💌 Parent Communication Writer")
    st.markdown("Draft personalized messages for parents")
    
    # Get selected teacher if available
    selected_teacher = st.session_state.get('selected_teacher', 'All Teachers')
    default_teacher = selected_teacher if selected_teacher != "All Teachers" else ""
    
    col1, col2 = st.columns(2)
    
    with col1:
        purpose = st.selectbox(
            "Message Purpose *",
            ["appreciation", "reminder", "feedback", "concern"],
            help="What is the main purpose of this message?"
        )
        child_name = st.text_input("Child's Name *", placeholder="e.g., Emma Johnson")
    
    with col2:
        teacher_name = st.text_input("Your Name", value=default_teacher, placeholder="e.g., Ms. Sarah Thompson")
        context = st.text_area(
            "Message Context *",
            height=150,
            placeholder="Provide details about what you want to communicate...\n\nExamples:\n- For appreciation: What did the student do well?\n- For reminder: What event/deadline/requirement?\n- For feedback: What progress or area to discuss?\n- For concern: What issue needs addressing?"
        )
    
    st.markdown("---")
    
    if st.button("🚀 Generate Message", type="primary", width="stretch"):
        if not purpose or not child_name or not context:
            st.error("❌ Please fill in all required fields (marked with *)")
        else:
            with st.spinner("✨ Crafting your message..."):
                try:
                    result = generate_parent_message(purpose, child_name, context, teacher_name)
                    
                    if result['success']:
                        st.success("✅ Message generated successfully!")
                        st.markdown("### 💌 Your Message:")
                        st.markdown(result['message'])
                        
                        # Copy to clipboard helper
                        st.code(result['message'], language=None)
                        
                        # Download button
                        st.download_button(
                            label="⬇️ Download Message",
                            data=result['message'],
                            file_name=f"parent_message_{purpose}_{child_name}.txt".replace(" ", "_"),
                            mime="text/plain"
                        )
                        
                        st.info(f"💾 Saved to: `{result['metadata']['output_file']}`")
                    else:
                        st.error(f"❌ Error: {result.get('error', 'Unknown error')}")
                        
                except Exception as e:
                    st.error(f"❌ An error occurred: {str(e)}")


# VIEW STUDENTS PAGE
elif page == "👥 View Students":
    st.header("👥 Student Data")
    st.markdown("View and manage your students from Google Sheets")
    
    # Add refresh button at the top
    col1, col2, col3 = st.columns([2, 1, 1])
    with col2:
        if st.button("🔄 Refresh Data", help="Clear cache and reload from Google Sheets"):
            st.cache_data.clear()
            st.success("Cache cleared! Reloading...")
            st.rerun()
    
    try:
        students = load_students_cached()  # Use cached data
        
        if students:
            # Get unique student names
            import pandas as pd
            df_all = pd.DataFrame(students)
            
            # Apply teacher filter if selected
            selected_teacher = st.session_state.get('selected_teacher', 'All Teachers')
            if selected_teacher != "All Teachers" and 'Teacher' in df_all.columns:
                df_all = df_all[df_all['Teacher'] == selected_teacher]
                st.info(f"👨‍🏫 Showing students for: **{selected_teacher}**")
            
            unique_students = df_all['Name'].unique() if 'Name' in df_all.columns else []
            
            st.success(f"✅ Found {len(unique_students)} students with {len(df_all)} total subject records")
            
            # Grade filter
            grades = sorted(df_all['Grade'].unique()) if 'Grade' in df_all.columns else []
            
            col_filter1, col_filter2 = st.columns(2)
            with col_filter1:
                grade_filter = st.selectbox(
                    "🎓 Filter by Grade:",
                    ["All Grades"] + list(grades),
                    help="Select a specific grade to view only those students"
                )
            
            with col_filter2:
                view_mode = st.radio(
                    "📊 View Mode:",
                    ["Student Summary", "All Subject Records"],
                    horizontal=True,
                    help="Summary shows each student once with averages. Records shows all subject entries."
                )
            
            # Apply grade filter
            if grade_filter != "All Grades":
                df_all = df_all[df_all['Grade'] == grade_filter]
                unique_students = df_all['Name'].unique() if 'Name' in df_all.columns else []
                st.info(f"📋 Showing {len(unique_students)} students from {grade_filter}")
            
            if view_mode == "Student Summary":
                # Aggregate data by student
                if 'Name' in df_all.columns and 'Score' in df_all.columns:
                    # Convert Score to numeric, replacing non-numeric with NaN
                    df_all['Score'] = pd.to_numeric(df_all['Score'], errors='coerce')
                    
                    summary = df_all.groupby('Name').agg({
                        'Score': lambda x: x.mean() if x.notna().any() else 0,
                        'Subject': lambda x: ', '.join(x.unique()[:3]) + ('...' if len(x.unique()) > 3 else ''),
                        'Behavior': lambda x: x.mode()[0] if len(x.mode()) > 0 else 'N/A'
                    }).reset_index()
                    summary.columns = ['Name', 'Average Score', 'Subjects', 'Overall Behavior']
                    summary['Average Score'] = summary['Average Score'].round(1)
                    st.dataframe(summary, width="stretch", hide_index=True)
                else:
                    st.warning("Missing required columns (Name, Score) in your sheet")
            else:
                # Show all records
                st.dataframe(df_all, width="stretch", hide_index=True)
            
            st.markdown("---")
            
            # Individual student view with ALL subjects
            st.subheader("🔍 View Individual Student")
            selected_name = st.selectbox("Select a student", sorted(unique_students))
            
            if selected_name:
                # Get all records for this student
                student_records = df_all[df_all['Name'] == selected_name] if 'Name' in df_all.columns else pd.DataFrame()
                
                if not student_records.empty:
                    # Show student overview
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.metric("📛 Name", selected_name)
                    with col2:
                        # Safely calculate average score
                        if 'Score' in student_records.columns:
                            scores = pd.to_numeric(student_records['Score'], errors='coerce')
                            avg_score = scores.mean() if scores.notna().any() else 0
                        else:
                            avg_score = 0
                        st.metric("📊 Average Score", f"{avg_score:.1f}")
                    with col3:
                        num_subjects = len(student_records)
                        st.metric("📚 Subjects", num_subjects)
                    
                    st.markdown("---")
                    st.markdown("### 📚 Subject Breakdown")
                    
                    # Display each subject
                    for idx, record in student_records.iterrows():
                        with st.expander(f"**{record.get('Subject', 'N/A')}** - Score: {record.get('Score', 'N/A')}", expanded=False):
                            col1, col2 = st.columns(2)
                            
                            with col1:
                                st.markdown("**📝 Notes:**")
                                st.info(record.get('Notes', 'No notes available'))
                            
                            with col2:
                                st.markdown("**🎭 Behavior:**")
                                behavior = record.get('Behavior', 'N/A')
                                if behavior == 'Excellent':
                                    st.success(behavior)
                                elif behavior == 'Good':
                                    st.info(behavior)
                                else:
                                    st.warning(behavior)
                                
                                if 'Attendance' in record:
                                    st.markdown(f"**📅 Attendance:** {record.get('Attendance', 'N/A')}")
                else:
                    st.error(f"No data found for {selected_name}")
                    
                    # Quick actions
                    st.markdown("---")
                    st.markdown("**⚡ Quick Actions:**")
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        if st.button("📊 Generate Report for This Student"):
                            st.session_state.page = "📊 Report Generator"
                            st.rerun()
                    
                    with col2:
                        if st.button("💌 Send Parent Message"):
                            st.session_state.page = "💌 Parent Message"
                            st.rerun()
        else:
            from config import settings
            if not settings.GOOGLE_SHEETS_CREDENTIALS or not settings.GOOGLE_SHEET_ID:
                st.info("ℹ️ **Google Sheets not configured** - You can still use all features with manual input!")
                st.markdown("""
                **Available Features:**
                - 📝 **Lesson Generator** - Create lesson notes
                - 📊 **Report Generator** - Write student reports (enter details manually)
                - 💌 **Parent Message** - Draft parent communications
                
                To enable automatic student data loading, add your Google Sheets credentials to the `.env` file.
                """)
            else:
                st.warning("⚠️ No students found in your Google Sheet")
                st.info("💡 Add students to your Google Sheet in the 'Students' tab")
            
    except Exception as e:
        st.error(f"❌ Unable to load students: {str(e)}")
        st.info("💡 Make sure your Google Sheets integration is properly configured")


# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: #666;'>
        <p>Built with ❤️ for educators | AI Teaching Assistant v1.0</p>
    </div>
    """,
    unsafe_allow_html=True
)
