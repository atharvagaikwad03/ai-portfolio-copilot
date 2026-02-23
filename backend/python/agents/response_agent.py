"""Response agent for generating contextual responses."""
from typing import Dict, Optional, Any
import json
from pathlib import Path
from agents.base_agent import BaseAgent


class ResponseAgent(BaseAgent):
    """Agent responsible for generating natural language responses."""
    
    def __init__(self):
        system_prompt = """You are the AI Portfolio Copilot for Atharva Gaikwad's personal portfolio website (atharvagaikwad03.github.io).

You are a friendly, professional chatbot that helps visitors learn about Atharva. Here is key information about him:

ABOUT:
Atharva Gaikwad is a Software Engineer & Full-Stack Developer currently pursuing his M.S. in Computer Science at Syracuse University (Expected May 2026, GPA 3.7/4.0). He has 2+ years of experience and has built 10+ projects. He specializes in mobile development, web applications, and blockchain solutions.

EXPERIENCE:
1. Software Developer Engineer at iConsult Collaborative, Syracuse University (Oct 2024 - Jul 2025)
   - Led front-end development for Yoga4Philly's platform using React.js and Angular
   - Translated Figma prototypes into production-ready interfaces with CI/CD pipelines
   - Designed modular UI components achieving 25% improvement in responsiveness

2. Software Engineer at Cerence AI (Jan 2023 - Jul 2024)
   - Enhanced app functionality by 20% using OkHttp, Dagger, and Retrofit
   - Engineered Firebase and RoomDB solutions, improving real-time data retrieval by 35%
   - Applied MediaBrowserService for media playback, cutting download times by 30%

3. Software Engineer Intern at Cerence AI (May 2022 - Jan 2023)
   - Improved app stability, reducing issue resolution time by 15%
   - Mobile app feature development with Roku BrightScript for TV interfaces

SKILLS:
- Languages: Python, Java, JavaScript, TypeScript, Kotlin, C++, HTML/CSS, Solidity, SQL
- Frameworks: React.js, Angular, Node.js, Flask, Django, Express.js, Socket.io
- Cloud & DevOps: AWS, Google Cloud, Firebase, Docker, CI/CD, Git
- Databases: MongoDB, PostgreSQL, Firebase Realtime DB, RoomDB
- Mobile: Android Studio, Xcode, React Native, Roku SDK
- Tools: VS Code, Postman, UI/UX Design, Unit Testing, Agile/Scrum

PROJECTS:
- Free Flow: ETHGlobal New York 2025 Hackathon Winner (Flow Builder Pool Prize). Interactive 2D multiplayer virtual environment with DeFi on Flow blockchain. Features real-time multiplayer with Socket.io, AI-powered DeFi with GOAT SDK + OpenAI, voice integration with ElevenLabs TTS.
- AI Portfolio Copilot: Multi-agent chatbot using Python, LangChain, Pinecone RAG architecture.

EDUCATION:
- M.S. Computer Science, Syracuse University (Expected May 2026, GPA 3.7/4.0)
- B.Tech Information Technology, University of Pune (May 2023, GPA 3.4/4.0)

CONTACT:
- Email: atgaikwa@syr.edu
- LinkedIn: linkedin.com/in/atharvagaikwad3/
- GitHub: github.com/atharvagaikwad03
- Portfolio: atharvagaikwad03.github.io

GUIDELINES:
- Be conversational, friendly, and professional
- Answer questions about Atharva's background, skills, experience, projects, and education
- If asked something outside the portfolio, politely redirect to portfolio topics
- Keep responses concise but informative
- Refer to Atharva in third person (e.g. "Atharva has experience in...")
- If you don't know something specific, say so honestly
"""
        super().__init__(
            name="ResponseAgent",
            system_prompt=system_prompt,
            temperature=0.7
        )
        self.portfolio_data = self._load_portfolio_data()

    def _load_portfolio_data(self) -> Dict[str, Any]:
        """Load local portfolio data for offline fallback responses."""
        data_path = Path(__file__).resolve().parents[3] / "data" / "sample_portfolio_data.json"
        try:
            with open(data_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {}

    def _fallback_response(self, user_input: str, error: str) -> str:
        """Generate a deterministic response when LLM calls fail."""
        query = user_input.lower()
        data = self.portfolio_data or {}
        name = data.get("name", "Atharva Gaikwad")
        contact = data.get("contact", {})
        projects = data.get("projects", [])
        experience = data.get("experience", [])
        education = data.get("education", [])
        skills = data.get("skills", {})

        if any(k in query for k in ["contact", "email", "linkedin", "github", "reach"]):
            return (
                f"I am currently in offline fallback mode (reason: {error}).\n\n"
                f"You can contact {name} here:\n"
                f"- Email: {contact.get('email', 'N/A')}\n"
                f"- LinkedIn: {contact.get('linkedin', 'N/A')}\n"
                f"- GitHub: {contact.get('github', 'N/A')}\n"
                f"- Portfolio: {contact.get('portfolio', data.get('portfolio_url', 'N/A'))}"
            )

        if any(k in query for k in ["project", "portfolio copilot", "free flow", "built"]):
            lines = [f"I am currently in offline fallback mode (reason: {error}).", "", f"{name}'s key projects:"]
            for project in projects[:3]:
                desc = project.get("description", "")
                lines.append(f"- {project.get('name', 'Project')}: {desc}")
            return "\n".join(lines)

        if any(k in query for k in ["experience", "work", "company", "intern"]):
            lines = [f"I am currently in offline fallback mode (reason: {error}).", "", f"{name}'s experience:"]
            for exp in experience[:3]:
                lines.append(f"- {exp.get('role', 'Role')} at {exp.get('company', 'Company')} ({exp.get('duration', 'N/A')})")
            return "\n".join(lines)

        if any(k in query for k in ["education", "degree", "university", "gpa", "study"]):
            lines = [f"I am currently in offline fallback mode (reason: {error}).", "", f"{name}'s education:"]
            for edu in education:
                lines.append(
                    f"- {edu.get('degree', 'Degree')} at {edu.get('institution', 'Institution')} "
                    f"({edu.get('graduation', 'N/A')}, GPA {edu.get('gpa', 'N/A')})"
                )
            return "\n".join(lines)

        if any(k in query for k in ["skill", "tech", "stack", "language", "framework"]):
            categories = {
                "programming_languages": "Languages",
                "frameworks": "Frameworks",
                "cloud_devops": "Cloud/DevOps",
                "databases": "Databases",
                "mobile_development": "Mobile",
            }
            lines = [f"I am currently in offline fallback mode (reason: {error}).", "", f"{name}'s skills include:"]
            for key, label in categories.items():
                items = skills.get(key, [])
                if items:
                    lines.append(f"- {label}: {', '.join(items[:8])}")
            return "\n".join(lines)

        return (
            f"I am currently in offline fallback mode (reason: {error}).\n\n"
            f"{name} is a {data.get('title', 'Software Engineer')} with {data.get('stats', {}).get('years_experience', '2+')} years of experience, "
            f"and has built {data.get('stats', {}).get('projects_built', '10+')} projects. "
            f"You can ask about projects, skills, experience, education, or contact details."
        )
    
    def process(self, user_input: str, context: Optional[Dict] = None) -> Dict[str, Any]:
        """Generate response based on query and retrieved context."""
        if context and context.get("formatted_context"):
            prompt = f"""User Query: {user_input}

Additional Retrieved Context:
{context['formatted_context']}

Generate a helpful response about Atharva based on the query and any additional context above."""
        else:
            prompt = f"""User Query: {user_input}

Generate a helpful response about Atharva based on the query. Use the portfolio information from your system prompt."""
        
        messages = self._build_messages(prompt)
        
        try:
            response = self._invoke_llm(messages)
            response_text = response.content
            
            self.add_to_history(user_input, response_text)
            
            return {
                "agent": self.name,
                "response": response_text,
                "query": user_input,
                "used_context": bool(context and context.get("formatted_context")),
                "success": True
            }
        except Exception as e:
            fallback = self._fallback_response(user_input, str(e))
            return {
                "agent": self.name,
                "response": fallback,
                "query": user_input,
                "success": True,
                "fallback_used": True,
                "error": str(e)
            }
