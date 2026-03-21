"""Response agent for generating contextual responses."""
from typing import Dict, Optional, Any
import json
import re
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
- Email: gaikwadatharva394@gmail.com
- Phone: +1 (315) 575-8511
- Address: 1020 Westcott St, Syracuse, New York 13210
- Visa Status: F1 OPT
- Sponsorship: Sponsorship needed in future after end of STEM Extension
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

    def _contains_any(self, query: str, terms: list[str]) -> bool:
        """Match whole words/phrases to avoid accidental substring hits."""
        return any(re.search(rf"\b{re.escape(term)}\b", query) for term in terms)

    def _should_answer_locally(self, user_input: str) -> bool:
        """Use local portfolio data for common site-chat questions."""
        query = user_input.lower()
        local_tokens = [
            "hello", "hi", "hey", "good morning", "good evening",
            "who are you", "who is atharva", "tell me about yourself", "tell me about atharva",
            "project", "free flow", "portfolio copilot", "built",
            "skill", "skills", "tech", "stack", "language", "framework",
            "experience", "work", "company", "intern", "job",
            "education", "degree", "university", "gpa", "study",
            "contact", "email", "linkedin", "github", "reach",
            "phone", "cell", "number", "call", "address", "location",
            "visa", "opt", "sponsorship", "stem extension", "work authorization",
        ]
        return self._contains_any(query, local_tokens)

    def _fallback_response(self, user_input: str) -> str:
        """Generate a deterministic response when LLM calls fail."""
        query = user_input.lower()
        data = self.portfolio_data or {}
        name = data.get("name", "Atharva Gaikwad")
        contact = data.get("contact", {})
        projects = data.get("projects", [])
        experience = data.get("experience", [])
        education = data.get("education", [])
        skills = data.get("skills", {})

        def format_experience(company_query: str) -> Optional[str]:
            for exp in experience:
                company_name = exp.get("company", "")
                if company_query in company_name.lower():
                    highlights = exp.get("highlights", [])
                    role = exp.get("role", "Role")
                    duration = exp.get("duration", "Duration")
                    lines = [f"{role} at {company_name} ({duration})"]
                    for h in highlights[:4]:
                        lines.append(f"- {h}")
                    return "\n".join(lines)
            return None

        def format_projects() -> str:
            if not projects:
                return "No projects found."
            lines = []
            for project in projects:
                name_line = project.get("name", "Project")
                desc = project.get("description", "")
                features = project.get("features", [])
                links = project.get("links", {})
                lines.append(name_line)
                if desc:
                    lines.append(f"  • {desc}")
                if features:
                    for f in features[:4]:
                        lines.append(f"  - {f}")
                if links:
                    for label, url in links.items():
                        lines.append(f"  - {label.title()} link: {url}")
                lines.append("")
            return "\n".join(lines).strip()

        def format_skills() -> str:
            if not skills:
                return "No skills found."
            ordered = [
                ("Programming Languages", skills.get("programming_languages", [])),
                ("Frameworks", skills.get("frameworks", [])),
                ("Cloud/DevOps", skills.get("cloud_devops", [])),
                ("Databases", skills.get("databases", [])),
                ("Mobile", skills.get("mobile_development", [])),
                ("Tools/Practices", skills.get("tools_practices", [])),
            ]
            lines = []
            for label, items in ordered:
                if items:
                    lines.append(f"{label}: {', '.join(items)}")
            return "\n".join(lines)

        if self._contains_any(query, ["hello", "hi", "hey", "good morning", "good evening"]):
            return (
                f"Hi, I'm the portfolio copilot for {name}. "
                "You can ask about projects, skills, experience, education, or contact details."
            )

        if self._contains_any(query, ["linkedin"]):
            return (
                f"You can view {name}'s LinkedIn here:\n"
                f"{contact.get('linkedin', 'N/A')}"
            )

        if self._contains_any(query, ["github"]):
            return (
                f"You can view {name}'s GitHub here:\n"
                f"{contact.get('github', 'N/A')}"
            )

        if self._contains_any(query, ["portfolio"]) and not self._contains_any(query, ["portfolio copilot", "project"]):
            return (
                f"You can view {name}'s portfolio here:\n"
                f"{contact.get('portfolio', data.get('portfolio_url', 'N/A'))}"
            )

        if self._contains_any(query, ["email", "mail"]):
            return (
                f"You can reach {name} by email here:\n"
                f"{contact.get('email', 'N/A')}"
            )

        if self._contains_any(query, ["phone", "cell", "number", "call"]):
            return (
                f"You can reach {name} by phone here:\n"
                f"{contact.get('phone', 'N/A')}"
            )

        if self._contains_any(query, ["address", "location", "where are you located", "where are you based"]):
            return (
                f"{name}'s address is:\n"
                f"{contact.get('address', 'N/A')}"
            )

        if self._contains_any(query, ["visa", "opt", "work authorization"]):
            return (
                f"{name}'s visa status is:\n"
                f"{contact.get('visa_status', 'N/A')}"
            )

        if self._contains_any(query, ["sponsorship", "stem extension"]):
            return (
                f"Sponsorship details for {name}:\n"
                f"{contact.get('sponsorship', 'N/A')}"
            )

        cerence_exp = format_experience("cerence")
        iconsult_exp = format_experience("iconsult")
        if self._contains_any(query, ["cerence", "cerence ai"]) and cerence_exp:
            return cerence_exp
        if self._contains_any(query, ["iconsult", "iconsult collaborative", "yoga4philly"]) and iconsult_exp:
            return iconsult_exp

        if self._contains_any(query, ["project", "portfolio copilot", "free flow", "built"]):
            return format_projects()

        if self._contains_any(query, ["skill", "skills", "tech", "stack", "language", "framework"]):
            return format_skills()

        if self._contains_any(query, ["contact", "email", "linkedin", "github", "reach"]):
            return (
                f"You can contact {name} here:\n"
                f"- Email: {contact.get('email', 'N/A')}\n"
                f"- Phone: {contact.get('phone', 'N/A')}\n"
                f"- Address: {contact.get('address', 'N/A')}\n"
                f"- Visa Status: {contact.get('visa_status', 'N/A')}\n"
                f"- Sponsorship: {contact.get('sponsorship', 'N/A')}\n"
                f"- LinkedIn: {contact.get('linkedin', 'N/A')}\n"
                f"- GitHub: {contact.get('github', 'N/A')}\n"
                f"- Portfolio: {contact.get('portfolio', data.get('portfolio_url', 'N/A'))}"
            )

        if self._contains_any(query, ["experience", "work", "company", "intern"]):
            lines = [f"{name}'s experience:"]
            for exp in experience[:3]:
                lines.append(f"- {exp.get('role', 'Role')} at {exp.get('company', 'Company')} ({exp.get('duration', 'N/A')})")
            return "\n".join(lines)

        if self._contains_any(query, ["education", "degree", "university", "gpa", "study"]):
            lines = [f"{name}'s education:"]
            for edu in education:
                lines.append(
                    f"- {edu.get('degree', 'Degree')} at {edu.get('institution', 'Institution')} "
                    f"({edu.get('graduation', 'N/A')}, GPA {edu.get('gpa', 'N/A')})"
                )
            return "\n".join(lines)

        return (
            f"{name} is a {data.get('title', 'Software Engineer')} with {data.get('stats', {}).get('years_experience', '2+')} years of experience, "
            f"and has built {data.get('stats', {}).get('projects_built', '10+')} projects. "
            f"You can ask about projects, skills, experience, education, or contact details."
        )
    
    def process(self, user_input: str, context: Optional[Dict] = None) -> Dict[str, Any]:
        """Generate response based on query and retrieved context."""
        if self._should_answer_locally(user_input):
            response_text = self._fallback_response(user_input)
            self.add_to_history(user_input, response_text)
            return {
                "agent": self.name,
                "response": response_text,
                "query": user_input,
                "used_context": False,
                "success": True,
                "fallback_used": True,
            }

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
            fallback = self._fallback_response(user_input)
            return {
                "agent": self.name,
                "response": fallback,
                "query": user_input,
                "success": True,
                "fallback_used": True,
                "error": str(e)
            }
