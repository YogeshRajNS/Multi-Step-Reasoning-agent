# Multi-Step Reasoning Agent with Self-Checking

A sophisticated reasoning agent that solves structured word problems through a three-phase approach: planning, execution, and verification. The agent uses Google's Gemini AI to break down complex problems, solve them step-by-step, and verify its own work before presenting the final answer.

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Google AI](https://img.shields.io/badge/Powered%20by-Google%20Gemini-4285F4.svg)](https://ai.google.dev/)
[![Streamlit](https://img.shields.io/badge/Frontend-Streamlit-FF4B4B.svg)](https://streamlit.io/)

## 🌟 Features

### Core Agent Capabilities
- **Three-Phase Problem Solving**: Separates planning, execution, and verification for robust reasoning
- **Self-Verification**: Automatically checks its own work through multiple validation steps
- **Automatic Retry Logic**: Retries failed solutions up to a configurable number of times
- **Structured Output**: Returns well-formatted JSON responses with answer, reasoning, and metadata

### Multiple Interfaces
- **🖥️ CLI Interface**: Interactive command-line interface for quick testing
- **🌐 Web Interface**: Beautiful Streamlit-based web UI with rich visualizations
- **📚 Programmatic API**: Use the agent in your own Python applications
- **🧪 Test Suite**: Comprehensive testing with 13 predefined test cases

### Streamlit Web UI Features
- **Interactive Question Interface**: Ask questions with example prompts
- **Test Suite Runner**: Run and analyze predefined test cases
- **Query History**: Track all your questions and answers
- **Performance Metrics**: Real-time statistics and visualizations
- **Export Functionality**: Download results in JSON format
- **Responsive Design**: Works on desktop, tablet, and mobile

## 📋 Table of Contents

- [Problem Domain](#-problem-domain)
- [Architecture](#-architecture)
- [Installation](#-installation)
- [Quick Start](#-quick-start)
- [Usage Examples](#-usage-examples)
  - [Web Interface (Streamlit)](#web-interface-streamlit)
  - [CLI Interface](#cli-interface)
  - [Programmatic Usage](#programmatic-usage)
- [Prompt Design](#-prompt-design)
- [Testing](#-testing)
- [Output Format](#-output-format)
- [Design Decisions](#-design-decisions)
- [Limitations & Future Improvements](#-limitations--future-improvements)

## 🎯 Problem Domain

The agent specializes in solving structured word problems involving:

- **Time Calculations**: Journey durations, meeting schedules, time slot matching
- **Arithmetic & Logic**: Multi-step calculations, percentage problems, constraints
- **Geometry**: Area, perimeter, and basic geometric calculations
- **Age Problems**: Working backwards from future conditions
- **Relative Motion**: Speed, distance, and time problems

### Example Questions

```
"If a train leaves at 14:30 and arrives at 18:05, how long is the journey?"
"Alice has 3 red apples and twice as many green apples. How many total?"
"A meeting needs 60 minutes. Free slots: 09:00-09:30, 09:45-10:30, 11:00-12:00. Which fit?"
"Bob is twice as old as Alice. In 5 years, Bob will be 25. How old is Alice now?"
```

## 🏗️ Architecture

The agent implements a modular three-phase architecture:

```
┌─────────────────────────────────────────────────────────────┐
│                     User Question                           │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│  Phase 1: PLANNER                                           │
│  • Analyzes the question                                    │
│  • Creates step-by-step solution plan                       │
│  • Identifies required information and operations           │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│  Phase 2: EXECUTOR                                          │
│  • Follows the plan step-by-step                            │
│  • Performs calculations and logical reasoning              │
│  • Produces intermediate work and final answer              │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│  Phase 3: VERIFIER                                          │
│  • Re-solves problem independently                          │
│  • Checks arithmetic accuracy                               │
│  • Validates logical consistency                            │
│  • Verifies constraint satisfaction                         │
└─────────────────────┬───────────────────────────────────────┘
                      │
              ┌───────┴────────┐
              │                │
          Pass?              Fail?
              │                │
              ▼                ▼
        ┌─────────┐      ┌──────────┐
        │ Success │      │  Retry   │
        │ Return  │      │ (max 2x) │
        └─────────┘      └──────────┘
```

### Key Components

#### 1. **ReasoningAgent** (Main Class)
- Orchestrates the three-phase solving process
- Manages LLM API calls with error handling
- Implements retry logic with configurable attempts

#### 2. **Phase Separation**
- **`plan(question)`**: Creates solution strategy
- **`execute(question, plan)`**: Implements the plan
- **`verify(question, solution)`**: Validates the solution

#### 3. **Data Structures**
- **`Check`**: Represents individual verification checks
- **`AgentResponse`**: Standardized response format with answer, status, and metadata

#### 4. **Streamlit Frontend**
- **Interactive UI**: Three-tab interface (Ask Question, Run Tests, History)
- **Real-time Updates**: Live progress tracking and status indicators
- **Data Visualization**: Performance metrics and test result analytics
- **Export Features**: Download results and history in JSON format

## 🚀 Installation

### Prerequisites

- Python 3.8 or higher
- Google AI Studio API key (free tier available)

### Step 1: Clone or Download

Download all project files:
- `reasoning_agent.py` - Core reasoning logic
- `test_agent.py` - Test suite definitions
- `streamlit_app.py` - Web interface
- `requirements.txt` - Python dependencies

### Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

Dependencies include:
- `streamlit>=1.28.0` - Web interface framework
- `google-generativeai>=0.3.0` - Google Gemini API
- `python-dotenv>=1.0.0` - Environment variable management
- `pandas>=2.0.0` - Data manipulation for test results

### Step 3: Set Up API Key

#### Option A: Using Environment Variable

```bash
export GEMINI_API_KEY='your-api-key-here'
```

#### Option B: Using .env File (Recommended)

Create a `.env` file in the project root:

```bash
GEMINI_API_KEY=your-api-key-here
```

#### Option C: Enter in Web Interface

You can also enter your API key directly in the Streamlit app's sidebar.

#### Getting a Free API Key

1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Click "Create API Key"
3. Copy the generated key
4. Set it using one of the methods above

## 🏃 Quick Start

### 🌐 Web Interface (Streamlit) - **RECOMMENDED**

Launch the interactive web application:

```bash
streamlit run streamlit_app.py
```

Or use the included launcher script:

```bash
chmod +x run_streamlit.sh
./run_streamlit.sh
```

The app will open in your default browser at `http://localhost:8501`

**Web Interface Features:**

1. **Ask Questions Tab** 🤔
   - Type or select example questions
   - Get detailed answers with reasoning
   - View verification checks
   - See execution plans
   - Export individual results

2. **Run Tests Tab** 🧪
   - Run Easy, Tricky, or All test suites
   - Live progress tracking
   - Comprehensive metrics dashboard
   - Detailed test result analysis
   - Export test results to JSON

3. **History Tab** 📜
   - Browse all past queries
   - Filter and search history
   - View detailed breakdowns
   - Export complete history

### 💻 CLI Interface

Run the interactive command-line interface:

```bash
python reasoning_agent.py
```

Example session:

```
Multi-Step Reasoning Agent (Powered by Google Gemini)
==================================================
Type your question or 'quit' to exit.

Question: If a train leaves at 14:30 and arrives at 18:05, how long is the journey?

Processing...

==================================================
ANSWER: 3 hours and 35 minutes
STATUS: success

REASONING: The journey duration is calculated by finding the time 
difference between departure (14:30) and arrival (18:05).
==================================================

[Metadata: 0 retries, 5 checks performed]
```

### 📝 Programmatic Usage

```python
from reasoning_agent import ReasoningAgent

# Initialize the agent
agent = ReasoningAgent(max_retries=2)

# Solve a question
result = agent.solve("What is 25% of 80?")

# Access the results
print(f"Answer: {result.answer}")
print(f"Status: {result.status}")
print(f"Reasoning: {result.reasoning_visible_to_user}")

# Access metadata
print(f"Retries: {result.metadata['retries']}")
print(f"Checks: {len(result.metadata['checks'])}")

# Convert to dictionary
result_dict = result.to_dict()
```

### 🧪 Run Test Suite

Run all test cases from command line:

```bash
python test_agent.py
```

Or run a single custom question:

```bash
python test_agent.py "What is 20% of 80?"
```

## 📚 Usage Examples

### Web Interface (Streamlit)

#### 1. Initialize the Agent

1. Open the sidebar (click arrow if collapsed)
2. Enter your Google Gemini API key
3. Adjust max retries (default: 2)
4. Click "🚀 Initialize Agent"
5. Wait for "✅ Agent Ready" status

#### 2. Ask a Question

Navigate to **"🤔 Ask Question"** tab:

1. Type your question or click an example
2. Click "🧮 Solve"
3. View results:
   - ✅/❌ Status indicator
   - Final answer
   - Step-by-step reasoning
   - Verification checks with pass/fail
   - Execution plan
   - Performance metadata
   - Full JSON response

#### 3. Run Test Suite

Navigate to **"🧪 Run Tests"** tab:

1. Select category (Easy, Tricky, or All)
2. Click "▶️ Run Test Suite"
3. Watch live progress
4. View summary metrics:
   - Total tests run
   - Correct answers percentage
   - Success rate
   - Average retries
5. Analyze individual test results
6. Export to JSON if needed

#### 4. Review History

Navigate to **"📜 History"** tab:

- View all past queries with timestamps
- Expand entries for full details
- Export complete history
- Clear history from sidebar

### CLI Interface

#### Example 1: Time Calculation

**Question**: "A meeting starts at 10:00 and lasts 45 minutes. When does it end?"

**Response**:
```json
{
  "answer": "10:45",
  "status": "success",
  "reasoning_visible_to_user": "Starting from 10:00 and adding 45 minutes gives us 10:45.",
  "metadata": {
    "plan": "1. Parse start time\n2. Add duration\n3. Format result",
    "checks": [
      {
        "check_name": "Correctness Check",
        "passed": true,
        "details": "Answer verified by independent calculation"
      }
    ],
    "retries": 0
  }
}
```

#### Example 2: Multi-Step Problem

**Question**: "Bob is twice as old as Alice. In 5 years, Bob will be 25. How old is Alice now?"

**Response**:
```json
{
  "answer": "10 years old",
  "status": "success",
  "reasoning_visible_to_user": "Working backwards: If Bob is 25 in 5 years, he's 20 now. Since Bob is twice Alice's age, Alice is 10.",
  "metadata": {
    "plan": "1. Find Bob's current age\n2. Use ratio to find Alice's age\n3. Verify relationship",
    "checks": [
      {
        "check_name": "Correctness Check",
        "passed": true,
        "details": "Logic and arithmetic verified"
      },
      {
        "check_name": "Arithmetic Check",
        "passed": true,
        "details": "All calculations correct"
      }
    ],
    "retries": 0
  }
}
```

#### Example 3: Constraint Matching

**Question**: "A meeting needs 60 minutes. Free slots: 09:00-09:30, 09:45-10:30, 11:00-12:00. Which slots fit?"

**Response**:
```json
{
  "answer": "11:00-12:00 (45 minutes is insufficient for 09:45-10:30)",
  "status": "success",
  "reasoning_visible_to_user": "09:00-09:30 is only 30 minutes. 09:45-10:30 is 45 minutes. Only 11:00-12:00 provides the full 60 minutes needed.",
  "metadata": {
    "retries": 1
  }
}
```

### Programmatic API

#### Basic Usage

```python
from reasoning_agent import ReasoningAgent

# Create agent with custom retry limit
agent = ReasoningAgent(max_retries=3)

# Solve a problem
result = agent.solve("If I buy 3 books at $12 each, how much do I spend?")

# Check if solution was verified
if result.status == "success":
    print(f"Verified Answer: {result.answer}")
else:
    print(f"Could not verify after {result.metadata['retries']} retries")
```

#### Batch Processing

```python
questions = [
    "What is 15 + 27?",
    "If a train travels 60 km in 30 minutes, what's its speed?",
    "A rectangle has length 10 and width 6. What's its area?"
]

results = []
for q in questions:
    result = agent.solve(q)
    results.append({
        'question': q,
        'answer': result.answer,
        'verified': result.status == 'success'
    })

# Analyze results
success_rate = sum(1 for r in results if r['verified']) / len(results)
print(f"Success Rate: {success_rate*100:.1f}%")
```

#### Error Handling

```python
from reasoning_agent import ReasoningAgent

try:
    agent = ReasoningAgent()
    result = agent.solve("Complex question here...")
    
    if result.status == "success":
        print(f"Answer: {result.answer}")
    else:
        # Handle failed verification
        print(f"Verification failed: {result.reasoning_visible_to_user}")
        
except ValueError as e:
    print(f"Configuration error: {e}")
except Exception as e:
    print(f"Unexpected error: {e}")
```

## 🎨 Prompt Design

### Design Philosophy

The prompts are designed with three core principles:

1. **Separation of Concerns**: Each phase (plan, execute, verify) has a distinct prompt
2. **Structured Outputs**: All prompts explicitly request JSON format
3. **Self-Contained**: Each prompt includes sufficient context and examples

### 1. Planner Prompt

**Purpose**: Generate a step-by-step solution strategy

**Key Elements**:
- Asks for numbered list format
- Emphasizes logical breakdown
- Includes verification as final step

**Design Rationale**:
- **Why numbered lists?** Easy to parse and follow sequentially
- **Why emphasize extraction?** Separates parsing from computation
- **Why include verification?** Primes the model to think about correctness

**Example Output**:
```
1. Parse the departure time (14:30)
2. Parse the arrival time (18:05)
3. Calculate the time difference
4. Format as hours and minutes
5. Verify the calculation
```

### 2. Executor Prompt

**Purpose**: Follow the plan and produce a detailed solution

**Key Elements**:
- Requires JSON output with specific fields: `answer`, `reasoning`, `intermediate_work`
- Emphasizes showing intermediate work
- Requests double-checking of arithmetic
- Multiple reminders to output ONLY JSON

**Design Rationale**:
- **Why JSON?** Enables programmatic parsing and structured data
- **Why intermediate work?** Provides transparency for verification
- **Why multiple reminders?** Gemini sometimes adds explanatory text

**Challenges Faced**:
- Gemini often wrapped JSON in markdown code blocks (```json...```)
- Solution: Implemented robust regex-based JSON extraction
- Handles multiple variations of markdown formatting

### 3. Verifier Prompt

**Purpose**: Validate the solution through independent checking

**Key Elements**:
- Lists 5 specific check types
- Requires JSON array format
- Emphasizes independent re-solving

**Design Rationale**:
- **Why 5 checks?** Covers different error types (arithmetic, logic, constraints, units)
- **Why independent re-solving?** Catches systematic errors
- **Why strict format?** Enables automated pass/fail decisions

**Verification Checks**:
1. **Correctness Check**: Re-solve independently and compare
2. **Arithmetic Check**: Verify all calculations step-by-step
3. **Logic Check**: Check reasoning soundness and flow
4. **Constraint Check**: Validate all problem requirements are met
5. **Units Check**: Ensure units are consistent and correct

### Prompt Evolution

**What Didn't Work**:
- ❌ Single monolithic prompt → Too complex, mixed concerns
- ❌ Conversational prompts → Inconsistent output formats
- ❌ No output format specification → Hard to parse responses
- ❌ Implicit verification → Model skipped checking steps

**What Worked**:
- ✅ Separate prompts per phase → Clear responsibilities
- ✅ Explicit JSON schemas → Reliable parsing
- ✅ Multiple format reminders → Reduced markdown wrapping
- ✅ System + user prompt split → Better role definition
- ✅ Examples in documentation → Clearer expectations

### JSON Parsing Strategy

Implemented multi-layer extraction to handle Gemini's output variations:

```python
1. Strip whitespace
2. Look for ```json...``` blocks
3. Look for ```...``` blocks  
4. Regex search for {...} or [...]
5. Fallback to direct parsing
6. Error handling with partial results
```

This robust approach handles:
- Plain JSON responses
- JSON wrapped in markdown code blocks
- JSON with explanatory text before/after
- Malformed JSON with graceful degradation

## 🧪 Testing

### Running the Full Test Suite

#### Via Web Interface (Recommended)

1. Launch Streamlit app: `streamlit run streamlit_app.py`
2. Initialize the agent with your API key
3. Navigate to "🧪 Run Tests" tab
4. Select test category
5. Click "▶️ Run Test Suite"
6. View live progress and results

#### Via Command Line

```bash
python test_agent.py
```

### Test Categories

#### Easy Tests (8 questions)
- Basic time differences
- Simple arithmetic (addition, subtraction, multiplication)
- Straightforward geometry (perimeter, area)
- Percentage calculations
- Division with remainders

#### Tricky Tests (5 questions)
- Multi-constraint problems (time slot matching)
- Problems requiring working backwards (age problems)
- Non-integer solutions (edge cases)
- Compound percentages (not additive)
- Relative motion (catching up problems)

### Test Output

#### CLI Output

```
======================================================================
Test #1 [EASY]: Basic time difference calculation
======================================================================
Question: If a train leaves at 14:30 and arrives at 18:05, how long is the journey?

Answer: 3 hours and 35 minutes
Status: success
Reasoning: The journey takes 3 hours and 35 minutes...

Metadata:
  - Retries: 0
  - Checks performed: 5
  - Check results:
    ✓ Correctness Check: Answer verified independently
    ✓ Arithmetic Check: All calculations correct
    ✓ Logic Check: Reasoning is sound

✓ Expected answer validation: PASS

======================================================================
TEST SUMMARY
======================================================================

Total Tests: 13
Successful Status: 12/13 (92.3%)
Correct Answers: 11/13 (84.6%)
Errors: 0/13

Easy Tests: 7/8 correct
Tricky Tests: 4/5 correct

Detailed results saved to: test_results.json
```

#### Web Interface Output

The Streamlit interface provides:
- **Live Progress**: Real-time test execution with progress bar
- **Summary Metrics**: Success rate, accuracy, average retries
- **Category Breakdown**: Easy vs Tricky performance comparison
- **Interactive Table**: Sortable, filterable results table
- **Individual Details**: Expandable view for each test
- **Export Options**: Download results as JSON

### Test Results Format

The test suite generates a `test_results.json` file with detailed information:

```json
[
  {
    "test_num": 1,
    "category": "EASY",
    "description": "Basic time difference calculation",
    "question": "If a train leaves at 14:30...",
    "answer": "3 hours and 35 minutes",
    "status": "success",
    "answer_correct": true,
    "retries": 0,
    "checks_passed": true,
    "full_result": {
      "answer": "3 hours and 35 minutes",
      "status": "success",
      "reasoning_visible_to_user": "...",
      "metadata": { ... }
    }
  }
]
```

## 📤 Output Format

### Standard Response Schema

```json
{
  "answer": "string - Final user-facing answer",
  "status": "success | failed",
  "reasoning_visible_to_user": "string - Brief explanation without raw chain-of-thought",
  "metadata": {
    "plan": "string - Internal planning steps",
    "checks": [
      {
        "check_name": "string - Name of the check",
        "passed": "boolean - Check result",
        "details": "string - Explanation"
      }
    ],
    "retries": "integer - Number of retry attempts"
  }
}
```

### Response Fields Explained

- **answer**: Concise, direct answer to the question
- **status**: Either "success" (verified) or "failed" (verification failed after max retries)
- **reasoning_visible_to_user**: User-friendly explanation (not raw chain-of-thought)
- **metadata.plan**: The step-by-step plan created by the planner
- **metadata.checks**: List of all verification checks performed
- **metadata.retries**: How many times the agent had to retry due to failed verification

## 🧠 Design Decisions

### 1. Why Google Gemini?

**Chosen**: Google Gemini 2.5 Flash

**Reasons**:
- Free tier with generous quota (15 requests/minute)
- Fast response times (~1-2 seconds)
- Good at structured reasoning tasks
- Strong JSON generation capabilities
- Easy to integrate via `google-generativeai` library

**Alternatives Considered**:
- OpenAI GPT-4: More expensive, requires paid API
- Anthropic Claude: Excellent reasoning but cost concerns
- Local models: Lower quality for complex reasoning

### 2. Three-Phase Architecture

**Benefits**:
- Clear separation of concerns
- Each phase can be tested independently
- Easy to swap out components
- Transparent reasoning process
- Facilitates debugging

**Trade-offs**:
- More API calls (3 per solution attempt)
- Slightly slower than single-shot
- More complex error handling

**Why it's worth it**:
- Significantly better verification accuracy
- Easier to identify where failures occur
- More maintainable and extensible code

### 3. Retry Logic

**Configuration**: Max 2 retries (total 3 attempts)

**Rationale**:
- Balance between accuracy and speed
- Prevents infinite loops
- Most problems solve in 1-2 attempts
- After 3 attempts, failure is likely systematic

**Customization**:
Users can adjust via:
- CLI: `ReasoningAgent(max_retries=N)`
- Web UI: Slider in sidebar (0-5 retries)

### 4. JSON-Based Communication

**Why JSON?**
- Machine-readable structured data
- Easy integration with other systems
- Type-safe parsing
- Standard format for APIs
- Enables web interface data display

**Challenges**:
- LLMs often add markdown formatting
- Requires robust extraction logic
- Error handling for malformed JSON

**Solution**:
Multi-layer parsing strategy with regex fallbacks and graceful degradation

### 5. Verification Approach

**Multi-Check Strategy**:
Rather than a single pass/fail, we perform 5 distinct checks:

1. **Correctness**: Independent re-solving
2. **Arithmetic**: Calculation verification
3. **Logic**: Reasoning validation
4. **Constraints**: Requirement checking
5. **Units**: Consistency validation

**Why Multiple Checks?**
- Catches different error types
- More robust than single check
- Provides detailed failure information
- Helps with debugging
- Enables targeted improvements

### 6. Streamlit for Web Interface

**Why Streamlit?**
- Rapid development (built in days, not weeks)
- Pure Python (no HTML/CSS/JavaScript needed)
- Built-in components for data visualization
- Easy deployment
- Active community and documentation

**Key Features Used**:
- `st.tabs()`: Multi-page interface
- `st.sidebar`: Configuration panel
- `st.session_state`: Persistent data
- `st.dataframe()`: Interactive tables
- `st.progress()`: Live updates
- Custom CSS: Enhanced styling

## 📁 Project Structure

```
multi-step-reasoning-agent/
│
├── reasoning_agent.py      # Core agent implementation
│   ├── ReasoningAgent class
│   ├── AgentResponse dataclass
│   ├── Check dataclass
│   └── CLI interface
│
├── test_agent.py           # Test suite
│   ├── EASY_TESTS list
│   ├── TRICKY_TESTS list
│   ├── Test runner functions
│   └── Result validation
│
├── streamlit_app.py        # Web interface
│   ├── UI configuration
│   ├── Agent initialization
│   ├── Question interface
│   ├── Test runner interface
│   ├── History tracker
│   └── Export functionality
│
├── requirements.txt        # Python dependencies
├── .env                    # Environment variables (create this)
└── README.md              # This file
```

## ⚠️ Limitations & Future Improvements

### Current Limitations

1. **API Rate Limits**
   - Free tier: 15 requests/minute
   - Can hit limits during extensive testing
   - **Mitigation**: Implemented exponential backoff
   - **Future**: Add request queuing system

2. **JSON Parsing Brittleness**
   - LLMs sometimes produce invalid JSON
   - **Mitigation**: Multi-layer extraction with fallbacks
   - **Future**: Fine-tune prompts further

3. **Verification False Negatives**
   - Occasionally flags correct answers as wrong
   - **Mitigation**: Multiple retry attempts
   - **Future**: Implement confidence scoring

4. **Limited Error Recovery**
   - After max retries, provides no partial solution
   - **Future**: Return best-effort answer with warnings

5. **Domain-Specific**
   - Optimized for math/logic word problems
   - May struggle with open-ended questions
   - **Future**: Add problem type classification

6. **No Concurrent Requests**
   - Tests run sequentially
   - **Future**: Add async/parallel execution
   - Would significantly speed up test suites

### Future Improvements

#### Short-Term (1-2 weeks)

- [ ] **Add Caching**: Cache plans for similar questions
- [ ] **Better Error Messages**: More helpful failure explanations
- [ ] **Async API Calls**: Parallel execution for faster responses
- [ ] **More Test Cases**: Expand to 50+ diverse questions
- [ ] **Logging System**: Add structured logging with timestamps
- [ ] **Mobile Optimization**: Improve Streamlit UI for mobile devices

#### Medium-Term (1-2 months)

- [ ] **Authentication**: Add user accounts to Streamlit app
- [ ] **Problem Classification**: Detect problem type and adapt strategy
- [ ] **Few-Shot Learning**: Add relevant examples to prompts dynamically
- [ ] **Confidence Scores**: Add uncertainty estimation
- [ ] **Multi-Model Support**: Add OpenAI, Anthropic as alternatives
- [ ] **Custom Test Upload**: Let users upload their own test suites
- [ ] **Result Analytics**: Advanced statistics and visualizations
- [ ] **Dark Mode**: Theme toggle for the web interface

#### Long-Term (3-6 months)

- [ ] **Tool Usage**: Let agent use Python, calculators, search
- [ ] **Chain-of-Thought Visualization**: Show reasoning graph
- [ ] **Fine-Tuning**: Train on problem-solving dataset
- [ ] **Interactive Clarification**: Ask user for ambiguity resolution
- [ ] **Benchmarking**: Compare against standard reasoning benchmarks
- [ ] **API Deployment**: RESTful API with FastAPI
- [ ] **Database Integration**: Store results in PostgreSQL/MongoDB
- [ ] **Team Collaboration**: Multi-user features in web app

### Known Issues

1. **Unicode Characters**: Some test cases have encoding issues (em-dashes)
   - **Impact**: Minor display issues
   - **Workaround**: Use standard ASCII hyphens

2. **Time Zone Handling**: Assumes all times are in same zone
   - **Impact**: May produce incorrect results for cross-timezone problems
   - **Future**: Add timezone parameter

3. **Ambiguous Questions**: No clarification mechanism
   - **Impact**: May misinterpret vague questions
   - **Workaround**: Be specific in questions

4. **No Unit Conversion**: Doesn't convert between units
   - **Impact**: Mixed units (minutes vs hours) may confuse
   - **Future**: Add unit conversion layer

5. **Session State Reset**: Streamlit resets on browser refresh
   - **Impact**: History and settings lost
   - **Future**: Add persistent storage (database or cookies)

## 🎯 Use Cases

### Educational
- **Math Tutoring**: Step-by-step problem solving
- **Logic Training**: Understanding complex reasoning
- **Test Preparation**: Practice with verified solutions

### Business
- **Schedule Optimization**: Find meeting time slots
- **Resource Allocation**: Calculate requirements
- **Financial Analysis**: Percentage and compound calculations

### Development
- **API Integration**: Embed reasoning in applications
- **Automated Verification**: Check calculation results
- **Batch Processing**: Solve multiple problems efficiently

## 📊 Performance Benchmarks

Based on the default 13-question test suite:

- **Average Success Rate**: ~85-92%
- **Easy Test Accuracy**: ~88-100%
- **Tricky Test Accuracy**: ~60-80%
- **Average Solve Time**: ~8-12 seconds per question (3 API calls)
- **Average Retries**: ~0.3-0.8 per question
- **API Usage**: 3-9 requests per question (depending on retries)

## 🔒 Security Considerations

### API Key Safety
- Never commit API keys to version control
- Use environment variables or .env files
- Web UI stores keys in session state only (not persisted)
- Consider using secrets management in production

### Input Validation
- No arbitrary code execution
- All inputs sanitized before API calls
- Rate limiting to prevent abuse
- Error messages don't expose sensitive info

### Data Privacy
- No data stored permanently by default
- Test results saved locally only
- No telemetry or external logging
- User queries not shared with third parties (except Google Gemini API)

## 🤝 Contributing

Contributions are welcome! Areas where help is needed:

- Additional test cases (especially edge cases)
- Support for more LLM providers
- Mobile app development
- Documentation improvements
- Bug fixes and error handling
- Performance optimizations
- UI/UX enhancements

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Built as a demonstration of multi-step AI reasoning
- Powered by Google Gemini 2.5 Flash
- Frontend built with Streamlit
- Inspired by research in AI reasoning and verification systems


## 🔗 Resources

- [Google AI Studio](https://makersuite.google.com/app/apikey) - Get your free API key
- [Gemini Documentation](https://ai.google.dev/) - Learn about Gemini API
- [Streamlit Documentation](https://docs.streamlit.io/) - Build web apps with Python

---
