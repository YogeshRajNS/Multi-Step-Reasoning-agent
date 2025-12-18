# Multi-Step Reasoning Agent with Self-Checking

A sophisticated reasoning agent that solves structured word problems through a three-phase approach: planning, execution, and verification. The agent uses Google's Gemini AI to break down complex problems, solve them step-by-step, and verify its own work before presenting the final answer.

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Google AI](https://img.shields.io/badge/Powered%20by-Google%20Gemini-4285F4.svg)](https://ai.google.dev/)

## 🌟 Features

- **Three-Phase Problem Solving**: Separates planning, execution, and verification for robust reasoning
- **Self-Verification**: Automatically checks its own work through multiple validation steps
- **Automatic Retry Logic**: Retries failed solutions up to a configurable number of times
- **Structured Output**: Returns well-formatted JSON responses with answer, reasoning, and metadata
- **Multiple Interfaces**: CLI, programmatic API, and test suite
- **Comprehensive Testing**: Includes 13 test cases covering easy and tricky problems

## 📋 Table of Contents

- [Problem Domain](#-problem-domain)
- [Architecture](#-architecture)
- [Installation](#-installation)
- [Quick Start](#-quick-start)
- [Usage Examples](#-usage-examples)
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

## 🚀 Installation

### Prerequisites

- Python 3.8 or higher
- Google AI Studio API key (free tier available)

### Step 1: Clone the Repository

```bash
git clone https://github.com/yourusername/reasoning-agent.git
cd reasoning-agent
```

### Step 2: Install Dependencies

```bash
pip install google-generativeai python-dotenv
```

Or use the requirements file:

```bash
pip install -r requirements.txt
```

### Step 3: Set Up API Key

#### Option A: Using Environment Variable

```bash
export GOOGLE_API_KEY='your-api-key-here'
```

#### Option B: Using .env File (Recommended)

Create a `.env` file in the project root:

```bash
GOOGLE_API_KEY=your-api-key-here
```

#### Getting a Free API Key

1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Click "Create API Key"
3. Copy the generated key
4. Set it using one of the methods above

## 🏃 Quick Start

### CLI Interface

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

### Programmatic Usage

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

### Single Test Question

```bash
python test_agent.py "What is 20% of 80?"
```

## 📚 Usage Examples

### Example 1: Time Calculation

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

### Example 2: Multi-Step Problem

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
      }
    ],
    "retries": 0
  }
}
```

### Example 3: Constraint Matching

**Question**: "A meeting needs 60 minutes. Free slots: 09:00-09:30, 09:45-10:30, 11:00-12:00. Which slots fit?"

**Response**:
```json
{
  "answer": "09:45-10:30 and 11:00-12:00",
  "status": "success",
  "reasoning_visible_to_user": "09:00-09:30 is only 30 minutes. 09:45-10:30 is 45 minutes. 11:00-12:00 is 60 minutes.",
  "metadata": {
    "retries": 0
  }
}
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
- Requires JSON output with specific fields
- Emphasizes showing intermediate work
- Requests double-checking of arithmetic

**Design Rationale**:
- **Why JSON?** Enables programmatic parsing and structured data
- **Why intermediate work?** Provides transparency for verification
- **Why multiple reminders?** Gemini sometimes adds explanatory text

**Challenges Faced**:
- Gemini often wrapped JSON in markdown code blocks
- Solution: Implemented robust regex-based JSON extraction

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
1. **Correctness**: Re-solve independently
2. **Arithmetic**: Verify all calculations
3. **Logic**: Check reasoning soundness
4. **Constraints**: Validate problem requirements
5. **Units**: Ensure consistency

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

## 🧪 Testing

### Running the Full Test Suite

```bash
python test_agent.py
```

### Test Categories

#### Easy Tests (8 questions)
- Basic time differences
- Simple arithmetic
- Straightforward geometry
- Percentage calculations

#### Tricky Tests (5 questions)
- Multi-constraint problems
- Problems requiring working backwards
- Non-integer solutions (edge cases)
- Compound percentages
- Relative motion

### Test Output

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
    "full_result": { ... }
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

### 3. Retry Logic

**Configuration**: Max 2 retries (total 3 attempts)

**Rationale**:
- Balance between accuracy and speed
- Prevents infinite loops
- Most problems solve in 1-2 attempts
- After 3 attempts, failure is likely systematic

### 4. JSON-Based Communication

**Why JSON?**
- Machine-readable structured data
- Easy integration with other systems
- Type-safe parsing
- Standard format for APIs

**Challenges**:
- LLMs often add markdown formatting
- Requires robust extraction logic
- Error handling for malformed JSON

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

## ⚠️ Limitations & Future Improvements

### Current Limitations

1. **API Rate Limits**
   - Free tier: 15 requests/minute
   - Can hit limits during extensive testing
   - **Mitigation**: Implemented exponential backoff

2. **JSON Parsing Brittleness**
   - LLMs sometimes produce invalid JSON
   - **Mitigation**: Multi-layer extraction with fallbacks

3. **Verification False Negatives**
   - Occasionally flags correct answers as wrong
   - **Mitigation**: Multiple retry attempts

4. **Limited Error Recovery**
   - After max retries, provides no partial solution
   - **Future**: Return best-effort answer with warnings

5. **Domain-Specific**
   - Optimized for math/logic word problems
   - May struggle with open-ended questions
   - **Future**: Add problem type classification

### Future Improvements

#### Short-Term (1-2 weeks)

- [ ] **Add Caching**: Cache plans for similar questions
- [ ] **Better Error Messages**: More helpful failure explanations
- [ ] **Async API Calls**: Parallel execution for faster responses
- [ ] **More Test Cases**: Expand to 50+ diverse questions
- [ ] **Logging System**: Add structured logging with timestamps

#### Medium-Term (1-2 months)

- [ ] **Web Interface**: Simple Flask/FastAPI web UI
- [ ] **Problem Classification**: Detect problem type and adapt strategy
- [ ] **Few-Shot Learning**: Add relevant examples to prompts dynamically
- [ ] **Confidence Scores**: Add uncertainty estimation
- [ ] **Multi-Model Support**: Add OpenAI, Anthropic as alternatives

#### Long-Term (3-6 months)

- [ ] **Tool Usage**: Let agent use Python, calculators, search
- [ ] **Chain-of-Thought Visualization**: Show reasoning graph
- [ ] **Fine-Tuning**: Train on problem-solving dataset
- [ ] **Interactive Clarification**: Ask user for ambiguity resolution
- [ ] **Benchmarking**: Compare against standard reasoning benchmarks

### Known Issues

1. **Unicode Characters**: Some test cases have encoding issues (em-dashes)
2. **Time Zone Handling**: Assumes all times are in same zone
3. **Ambiguous Questions**: No clarification mechanism
4. **No Unit Conversion**: Doesn't convert between units (e.g., minutes ↔ hours)

## 🤝 Contributing

Contributions are welcome! Areas where help is needed:

- Additional test cases (especially edge cases)
- Support for more LLM providers
- Web interface development
- Documentation improvements
- Bug fixes and error handling

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Built for interview assignment demonstrating multi-step reasoning
- Powered by Google Gemini 2.5 Flash
- Inspired by research in AI reasoning and verification systems


