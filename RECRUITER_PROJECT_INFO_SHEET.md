# AI Portfolio Copilot - Recruiter Prep Sheet

## What This Project Is

AI Portfolio Copilot is a personal website chatbot for my portfolio. A visitor can ask questions like:

- "Tell me about your projects"
- "What skills do you have?"
- "What is your LinkedIn?"
- "What is your visa status?"

The chatbot responds with information about me, my experience, my projects, my contact details, and my work authorization details.

## 30-Second Explanation

I built a portfolio chatbot that acts like an interactive guide for my website. Instead of making visitors read static sections, they can ask questions in natural language and get answers about my background, projects, skills, contact information, and work authorization. The system has a Node.js frontend gateway, a Python backend, and a chatbot layer that can use AI when available but still works with local fallback logic when the AI provider is unavailable.

## Simple Non-Technical Explanation

Think of it like a smart FAQ assistant for my portfolio website.

- A visitor types a question in the chat box.
- My backend decides what the question is about.
- If it is a common question, like contact info or skills, the bot answers directly from my stored portfolio data.
- If it is a broader question, the system can use AI and retrieval logic to build a better response.
- I also added graceful fallback behavior, so the chatbot still gives helpful answers even if the external AI API is down or quota-limited.

## Problem It Solves

Traditional portfolio sites are static. Recruiters or hiring managers have to scan multiple sections to find what they need.

This project solves that by:

- making my portfolio conversational
- reducing friction for recruiters
- helping users quickly get relevant answers
- handling both simple factual questions and broader portfolio questions

## What I Built

### User-facing features

- Web chat interface
- Answers about projects, skills, education, work experience, contact info, and work authorization
- Direct clickable links for LinkedIn, GitHub, and portfolio
- Fast local responses for common questions

### Backend features

- Python API for chat processing
- Node.js server as the frontend-facing gateway
- Multi-agent structure for query understanding, retrieval, response generation, and evaluation
- Local portfolio data source
- Vector-store-based retrieval layer
- Fallback handling when the LLM provider is unavailable

## Tech Stack

- Python
- FastAPI
- Node.js
- Express
- LangChain
- ChromaDB
- HTML/CSS/JavaScript frontend

## Architecture Overview

### High-level flow

1. User sends a message from the chat UI.
2. Node.js receives the request and forwards it to the Python backend.
3. Python orchestrates the chatbot flow.
4. For common questions, the system uses local portfolio data directly.
5. For broader questions, the system can use LLM + retrieval logic.
6. The final answer is returned to the UI.

### Main code areas

- Frontend chat UI: `/frontend/example.html`
- Node gateway: `/backend/nodejs/server.js`
- Python API: `/backend/python/api/server.py`
- Orchestration: `/backend/python/agents/orchestrator.py`
- Query handling: `/backend/python/agents/query_agent.py`
- Response generation: `/backend/python/agents/response_agent.py`
- Retrieval layer: `/backend/python/rag/retriever.py`
- Portfolio data: `/data/sample_portfolio_data.json`

## My Ownership / Contributions

I owned the project end to end:

- reviewed and understood the repo structure
- fixed chatbot failures
- improved reliability when the AI provider was unavailable
- added local-first handling for common portfolio questions
- added direct clickable contact links
- added contact, phone, address, visa, and sponsorship responses
- verified the app end-to-end through the real chat route
- pushed the changes to GitHub

## Where I Used AI In Development

I used an AI coding assistant during development, mainly as a debugging and implementation partner.

### Specific ways I used AI

- to inspect and summarize the codebase faster
- to identify why the chatbot was failing at runtime
- to help trace issues related to OpenAI model access and quota failures
- to help implement fallback logic for common portfolio questions
- to help add direct LinkedIn, GitHub, and portfolio link responses
- to help add phone, address, visa status, and sponsorship responses
- to help draft and refine regression tests

### What AI specifically helped with

- narrowing down the root cause quickly
- proposing code changes for error handling and local fallback behavior
- suggesting safer response routing for common questions
- catching a real bug where substring matching caused the sponsorship query to trigger the greeting branch because "sponsorship" contains "hi"

### What I accepted vs changed

I did not blindly accept AI output. I reviewed the logic and adjusted it where needed.

- I kept the general fallback architecture because it solved the real runtime issue.
- I refined the behavior so user-facing responses would not expose provider errors.
- I corrected the string-matching bug after verification showed incorrect behavior.
- I verified the final result through actual API calls and full app testing.

## Good Honest Answer If They Ask "How Did You Use AI?"

I used AI as a development assistant, not as a replacement for engineering judgment. It helped me inspect the codebase, narrow down runtime failures, and draft implementation changes faster. I still reviewed the code, adjusted the logic, caught edge cases during testing, and validated the final behavior end to end.

## Good Honest Answer If They Ask "What Did You Learn?"

I learned that AI is most useful when the problem is well-scoped and I treat it like a collaborator for iteration, not an autopilot. It helped me move faster on debugging and boilerplate changes, but correctness still came from testing, reviewing the behavior, and making final decisions myself.

## Good Honest Answer If They Ask "What Was The Hard Part?"

The hard part was making the chatbot reliable even when the external LLM provider was unavailable. The initial implementation depended too much on the AI provider. I improved that by introducing local-first handling for common portfolio questions and a fallback path so the product still works for users even when the provider fails.

## Demo Flow For Screen Share

If I need to walk through the project quickly, I can do this:

1. Show the chat UI.
2. Ask a project question like "Tell me about your projects."
3. Ask a contact question like "What is your LinkedIn?"
4. Click the returned link.
5. Ask "What is your visa status?" or "Will you need sponsorship?"
6. Briefly show the backend flow:
   - frontend sends request
   - Node proxies request
   - Python backend handles query
   - response agent returns local or AI-assisted answer

## Good Plain-English Walkthrough

If asked to explain the code simply:

"The frontend is just a chat box. The Node layer is the middleman that receives requests from the browser. The Python backend contains the chatbot logic. Inside that backend, one part figures out what the user is asking, another part can retrieve supporting information, and another part produces the final answer. For common factual questions, I made it answer directly from my stored portfolio data so it is faster and more reliable."

## If They Ask Why This Is A Good Example Of Using AI

This project is a good example because AI was used in two ways:

- inside the product, where the chatbot can use LLM-style logic for richer answers
- during development, where I used an AI assistant to debug problems, accelerate implementation, and improve reliability

That makes it a strong example of both AI-enabled software and AI-assisted engineering work.

## Real Project Highlights To Mention

- multi-agent style backend structure
- fallback logic for reliability
- direct recruiter-friendly contact answers
- clickable external profile links
- work authorization details included in chatbot responses
- end-to-end debugging and production-style validation

## Copy/Paste Prompt For Normal ChatGPT

Use this prompt with normal ChatGPT:

---
I have a recruiter conversation about a project I built called AI Portfolio Copilot. Please help me prepare to explain it clearly in simple terms, answer follow-up questions confidently, and describe how I used AI during development.

Project summary:

AI Portfolio Copilot is a portfolio website chatbot. A visitor can ask questions about my projects, skills, experience, contact information, GitHub, LinkedIn, portfolio, visa status, and sponsorship details. The app has a Node.js gateway, a Python FastAPI backend, a multi-agent chatbot structure, and a retrieval layer. For common factual questions, the chatbot now answers directly from local portfolio data for speed and reliability. For broader questions, it can use AI and retrieval logic. I also added graceful fallback behavior so the chatbot still works even if the external AI provider fails.

Tech stack:
- Python
- FastAPI
- Node.js
- Express
- LangChain
- ChromaDB
- HTML/CSS/JavaScript

My contributions:
- fixed chatbot failures
- added local-first fallback logic
- added direct LinkedIn, GitHub, and portfolio links
- added email, phone, address, visa, and sponsorship responses
- tested the project end to end

How I used AI during development:
- used an AI coding assistant to inspect the codebase
- debug runtime issues
- draft and refine implementation changes
- improve fallback behavior
- add test coverage
- I still reviewed, edited, and verified the final output myself

Please help me with:
1. a 30-second version
2. a 2-minute version
3. likely recruiter questions and strong answers
4. a simple explanation of where AI was used
5. a mock recruiter Q&A
---

## Fast Talking Points

- This is a conversational portfolio assistant.
- It helps recruiters find information faster than a static site.
- I built the backend flow and improved reliability.
- I used AI both in the product and in the development process.
- I used engineering judgment to review, adjust, and verify the AI-assisted changes.
