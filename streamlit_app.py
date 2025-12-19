"""
Multi-Step Reasoning Agent - Streamlit Frontend
Interactive web interface for the reasoning agent with test suite capabilities
"""

import streamlit as st
import json
import os
from datetime import datetime
from reasoning_agent import ReasoningAgent, AgentResponse
from test_agent import EASY_TESTS, TRICKY_TESTS, check_answer
import pandas as pd

# Page configuration
st.set_page_config(
    page_title="Multi-Step Reasoning Agent",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        padding: 1rem 0;
    }
    .sub-header {
        font-size: 1.5rem;
        font-weight: bold;
        color: #2c3e50;
        margin-top: 1rem;
    }
    .success-box {
        background-color: #d4edda;
        border-left: 5px solid #28a745;
        padding: 1rem;
        margin: 1rem 0;
        border-radius: 5px;
    }
    .error-box {
        background-color: #f8d7da;
        border-left: 5px solid #dc3545;
        padding: 1rem;
        margin: 1rem 0;
        border-radius: 5px;
    }
    .info-box {
        background-color: #d1ecf1;
        border-left: 5px solid #17a2b8;
        padding: 1rem;
        margin: 1rem 0;
        border-radius: 5px;
    }
    .warning-box {
        background-color: #fff3cd;
        border-left: 5px solid #ffc107;
        padding: 1rem;
        margin: 1rem 0;
        border-radius: 5px;
    }
    .metric-card {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .stButton>button {
        width: 100%;
        background-color: #1f77b4;
        color: white;
        font-weight: bold;
    }
    .check-passed {
        color: #28a745;
        font-weight: bold;
    }
    .check-failed {
        color: #dc3545;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'agent' not in st.session_state:
    st.session_state.agent = None
if 'history' not in st.session_state:
    st.session_state.history = []
if 'test_results' not in st.session_state:
    st.session_state.test_results = None

def initialize_agent(api_key: str, max_retries: int = 2):
    """Initialize the reasoning agent with API key"""
    try:
        #os.environ['GEMINI_API_KEY'] = api_key
        api_key = st.secrets["GEMINI_API_KEY"]
        agent = ReasoningAgent(api_key=api_key, max_retries=max_retries)
        st.session_state.agent = agent
        return True, "Agent initialized successfully! 🎉"
    except Exception as e:
        return False, f"Error initializing agent: {str(e)}"

def display_result(result: AgentResponse, question: str):
    """Display the agent's result in a formatted way"""
    
    # Status indicator
    if result.status == "success":
        st.markdown('<div class="success-box">', unsafe_allow_html=True)
        st.markdown(f"### ✅ Status: {result.status.upper()}")
    else:
        st.markdown('<div class="error-box">', unsafe_allow_html=True)
        st.markdown(f"### ❌ Status: {result.status.upper()}")
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Answer
    st.markdown("### 🎯 Answer")
    st.info(result.answer)
    
    # Reasoning
    st.markdown("### 💭 Reasoning")
    st.write(result.reasoning_visible_to_user)
    
    # Metadata in expandable sections
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📊 Metadata")
        st.write(f"**Retries:** {result.metadata.get('retries', 0)}")
        st.write(f"**Checks Performed:** {len(result.metadata.get('checks', []))}")
    
    with col2:
        st.markdown("### 📋 Plan")
        with st.expander("View Execution Plan"):
            st.text(result.metadata.get('plan', 'N/A'))
    
    # Verification Checks
    st.markdown("### ✓ Verification Checks")
    checks = result.metadata.get('checks', [])
    
    if checks:
        for i, check in enumerate(checks, 1):
            passed = check.get('passed', False)
            check_name = check.get('check_name', 'Unknown Check')
            details = check.get('details', 'No details')
            
            with st.expander(f"{'✅' if passed else '❌'} {check_name}", expanded=False):
                st.write(f"**Status:** {'Passed' if passed else 'Failed'}")
                st.write(f"**Details:** {details}")
    else:
        st.write("No checks available")
    
    # Full JSON
    with st.expander("🔍 View Full JSON Response"):
        st.json(result.to_dict())

def run_test_suite(agent: ReasoningAgent, test_category: str, progress_bar, status_text):
    """Run a test suite and return results"""
    
    if test_category == "Easy":
        tests = EASY_TESTS
    elif test_category == "Tricky":
        tests = TRICKY_TESTS
    else:  # All
        tests = EASY_TESTS + TRICKY_TESTS
    
    results = []
    
    for i, test in enumerate(tests):
        status_text.text(f"Running test {i+1}/{len(tests)}: {test['description']}")
        progress_bar.progress((i + 1) / len(tests))
        
        try:
            result = agent.solve(test['question'])
            answer_correct = check_answer(result.answer, test['expected_answer_contains'])
            
            results.append({
                'Test #': i + 1,
                'Category': 'EASY' if test in EASY_TESTS else 'TRICKY',
                'Description': test['description'],
                'Question': test['question'],
                'Answer': result.answer,
                'Expected': ', '.join(test['expected_answer_contains']),
                'Correct': '✅' if answer_correct else '❌',
                'Status': result.status,
                'Retries': result.metadata['retries'],
                'Checks Passed': all(c['passed'] for c in result.metadata['checks']),
                'Full Result': result.to_dict()
            })
        except Exception as e:
            results.append({
                'Test #': i + 1,
                'Category': 'EASY' if test in EASY_TESTS else 'TRICKY',
                'Description': test['description'],
                'Question': test['question'],
                'Answer': 'ERROR',
                'Expected': ', '.join(test['expected_answer_contains']),
                'Correct': '❌',
                'Status': 'error',
                'Retries': 0,
                'Checks Passed': False,
                'Error': str(e)
            })
    
    return results

def main():
    """Main Streamlit application"""
    
    # Header
    st.markdown('<div class="main-header">🧠 Multi-Step Reasoning Agent</div>', unsafe_allow_html=True)
    st.markdown("---")
    
    # Sidebar for configuration
    with st.sidebar:
        st.markdown("## ⚙️ Configuration")
        
        # API Key input
        api_key = st.text_input(
            "Google Gemini API Key",
            type="password",
            value=os.getenv("GEMINI_API_KEY", ""),
            help="Get your free API key from https://makersuite.google.com/app/apikey"
        )
        
        # Max retries
        max_retries = st.slider(
            "Max Retries",
            min_value=0,
            max_value=5,
            value=2,
            help="Number of retry attempts if verification fails"
        )
        
        # Initialize button
        if st.button("🚀 Initialize Agent"):
            if not api_key:
                st.error("Please provide an API key!")
            else:
                success, message = initialize_agent(api_key, max_retries)
                if success:
                    st.success(message)
                else:
                    st.error(message)
        
        # Agent status
        st.markdown("---")
        st.markdown("## 📊 Agent Status")
        if st.session_state.agent:
            st.success("✅ Agent Ready")
            st.info(f"Max Retries: {st.session_state.agent.max_retries}")
        else:
            st.warning("⚠️ Agent Not Initialized")
        
        # Links
        st.markdown("---")
        st.markdown("## 🔗 Resources")
        st.markdown("[Get API Key](https://makersuite.google.com/app/apikey)")
        st.markdown("[Gemini Documentation](https://ai.google.dev/)")
        
        # History count
        if st.session_state.history:
            st.markdown("---")
            st.markdown(f"## 📚 Query History")
            st.info(f"Total queries: {len(st.session_state.history)}")
            if st.button("Clear History"):
                st.session_state.history = []
                st.rerun()
    
    # Main content area with tabs
    tab1, tab2, tab3 = st.tabs(["🤔 Ask Question", "🧪 Run Tests", "📜 History"])
    
    # Tab 1: Ask Question
    with tab1:
        st.markdown("### Ask the Reasoning Agent")
        
        if not st.session_state.agent:
            st.warning("⚠️ Please initialize the agent first using the sidebar configuration.")
        else:
            # Example questions
            with st.expander("💡 Example Questions"):
                examples = [
                    "If a train leaves at 14:30 and arrives at 18:05, how long is the journey?",
                    "Alice has 3 red apples and twice as many green apples as red. How many apples does she have in total?",
                    "A store offers 20% off, then an additional 10% off the reduced price. What is the total discount on a $100 item?",
                    "Bob is twice as old as Alice. In 5 years, Bob will be 25. How old is Alice now?"
                ]
                for ex in examples:
                    if st.button(ex, key=f"example_{ex[:20]}"):
                        st.session_state.current_question = ex
            
            # Question input
            question = st.text_area(
                "Enter your question:",
                height=100,
                value=st.session_state.get('current_question', ''),
                placeholder="Type your question here... (e.g., 'If a book costs $15 and I have $50, how many books can I buy?')"
            )
            
            col1, col2, col3 = st.columns([1, 1, 2])
            
            with col1:
                solve_button = st.button("🧮 Solve", type="primary")
            
            with col2:
                clear_button = st.button("🗑️ Clear")
            
            if clear_button:
                st.session_state.current_question = ""
                st.rerun()
            
            if solve_button:
                if not question.strip():
                    st.error("Please enter a question!")
                else:
                    with st.spinner("🤔 Thinking... Planning, Executing, and Verifying..."):
                        try:
                            result = st.session_state.agent.solve(question)
                            
                            # Add to history
                            st.session_state.history.append({
                                'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                'question': question,
                                'result': result.to_dict()
                            })
                            
                            # Display result
                            st.markdown("---")
                            display_result(result, question)
                            
                        except Exception as e:
                            st.error(f"❌ Error: {str(e)}")
    
    # Tab 2: Run Tests
    with tab2:
        st.markdown("### 🧪 Test Suite Runner")
        
        if not st.session_state.agent:
            st.warning("⚠️ Please initialize the agent first using the sidebar configuration.")
        else:
            st.info("Run predefined test cases to evaluate the agent's performance on easy and tricky questions.")
            
            # Test category selection
            col1, col2 = st.columns(2)
            
            with col1:
                test_category = st.selectbox(
                    "Select Test Category",
                    options=["All", "Easy", "Tricky"],
                    help="Choose which test suite to run"
                )
            
            with col2:
                st.markdown("### 📈 Test Count")
                if test_category == "Easy":
                    st.metric("Tests to Run", len(EASY_TESTS))
                elif test_category == "Tricky":
                    st.metric("Tests to Run", len(TRICKY_TESTS))
                else:
                    st.metric("Tests to Run", len(EASY_TESTS) + len(TRICKY_TESTS))
            
            # Run tests button
            if st.button("▶️ Run Test Suite", type="primary"):
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                results = run_test_suite(
                    st.session_state.agent,
                    test_category,
                    progress_bar,
                    status_text
                )
                
                st.session_state.test_results = results
                status_text.text("✅ Tests completed!")
                progress_bar.empty()
            
            # Display results if available
            if st.session_state.test_results:
                st.markdown("---")
                st.markdown("### 📊 Test Results")
                
                df = pd.DataFrame(st.session_state.test_results)
                
                # Summary metrics
                total_tests = len(df)
                correct_answers = len(df[df['Correct'] == '✅'])
                success_status = len(df[df['Status'] == 'success'])
                
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.metric("Total Tests", total_tests)
                
                with col2:
                    st.metric(
                        "Correct Answers",
                        f"{correct_answers}/{total_tests}",
                        delta=f"{correct_answers/total_tests*100:.1f}%"
                    )
                
                with col3:
                    st.metric(
                        "Success Status",
                        f"{success_status}/{total_tests}",
                        delta=f"{success_status/total_tests*100:.1f}%"
                    )
                
                with col4:
                    avg_retries = df['Retries'].mean()
                    st.metric("Avg Retries", f"{avg_retries:.1f}")
                
                # Category breakdown
                if test_category == "All":
                    st.markdown("### 📈 Category Breakdown")
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        easy_df = df[df['Category'] == 'EASY']
                        easy_correct = len(easy_df[easy_df['Correct'] == '✅'])
                        st.info(f"**Easy Tests:** {easy_correct}/{len(easy_df)} correct ({easy_correct/len(easy_df)*100:.1f}%)")
                    
                    with col2:
                        tricky_df = df[df['Category'] == 'TRICKY']
                        tricky_correct = len(tricky_df[tricky_df['Correct'] == '✅'])
                        st.info(f"**Tricky Tests:** {tricky_correct}/{len(tricky_df)} correct ({tricky_correct/len(tricky_df)*100:.1f}%)")
                
                # Results table
                st.markdown("### 📋 Detailed Results")
                display_df = df[['Test #', 'Category', 'Description', 'Correct', 'Status', 'Retries']].copy()
                st.dataframe(display_df, use_container_width=True, height=400)
                
                # Individual test details
                st.markdown("### 🔍 Test Details")
                test_num = st.selectbox(
                    "Select a test to view details:",
                    options=df['Test #'].tolist(),
                    format_func=lambda x: f"Test #{x}: {df[df['Test #'] == x]['Description'].iloc[0]}"
                )
                
                selected_test = df[df['Test #'] == test_num].iloc[0]
                
                st.markdown(f"#### Test #{test_num}: {selected_test['Description']}")
                st.write(f"**Question:** {selected_test['Question']}")
                st.write(f"**Answer:** {selected_test['Answer']}")
                st.write(f"**Expected:** {selected_test['Expected']}")
                st.write(f"**Result:** {selected_test['Correct']}")
                
                if 'Full Result' in selected_test:
                    with st.expander("View Full Result"):
                        st.json(selected_test['Full Result'])
                
                # Export results
                st.markdown("---")
                col1, col2 = st.columns([1, 3])
                with col1:
                    if st.button("💾 Export Results (JSON)"):
                        json_str = json.dumps(st.session_state.test_results, indent=2)
                        st.download_button(
                            label="Download JSON",
                            data=json_str,
                            file_name=f"test_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                            mime="application/json"
                        )
    
    # Tab 3: History
    with tab3:
        st.markdown("### 📜 Query History")
        
        if not st.session_state.history:
            st.info("No queries in history yet. Ask some questions to see them here!")
        else:
            st.info(f"Total queries: {len(st.session_state.history)}")
            
            # Display history in reverse chronological order
            for i, entry in enumerate(reversed(st.session_state.history), 1):
                with st.expander(f"🕒 {entry['timestamp']} - {entry['question'][:50]}..."):
                    st.write(f"**Question:** {entry['question']}")
                    st.write(f"**Answer:** {entry['result']['answer']}")
                    st.write(f"**Status:** {entry['result']['status']}")
                    
                    with st.expander("View Full Details"):
                        st.json(entry['result'])
            
            # Export history
            if st.button("💾 Export History"):
                json_str = json.dumps(st.session_state.history, indent=2)
                st.download_button(
                    label="Download History (JSON)",
                    data=json_str,
                    file_name=f"query_history_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                    mime="application/json"
                )

if __name__ == "__main__":
    main()
