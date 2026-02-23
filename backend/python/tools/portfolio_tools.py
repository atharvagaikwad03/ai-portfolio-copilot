"""Tools available to agents for portfolio-related operations."""
import json
from langchain_core.tools import tool


PORTFOLIO_DATA = {
    "name": "Atharva Gaikwad",
    "title": "Software Engineer & Full-Stack Developer",
    "email": "atgaikwa@syr.edu",
    "linkedin": "https://www.linkedin.com/in/atharvagaikwad3/",
    "github": "https://github.com/atharvagaikwad03",
    "portfolio": "https://atharvagaikwad03.github.io"
}


@tool
def get_project_info(project_name: str) -> str:
    """Get detailed information about a specific project. Input should be the project name."""
    projects = {
        "free flow": {
            "name": "Free Flow",
            "award": "ETHGlobal New York 2025 - Flow Builder Pool Prize Winner",
            "description": "Interactive 2D multiplayer virtual environment inspired by the NYC skyline. Gamified social space bridging gaming, social platforms, and decentralized web for DeFi on the Flow blockchain.",
            "features": [
                "Real-time multiplayer with Socket.io",
                "AI-Powered DeFi with GOAT SDK + OpenAI",
                "Voice integration with ElevenLabs TTS",
                "Smart contracts on Flow blockchain"
            ],
            "links": {
                "ethglobal": "https://ethglobal.com/showcase/free-flow-u3xg9",
                "github": "https://github.com/atharvagaikwad03"
            }
        },
        "ai portfolio copilot": {
            "name": "AI Portfolio Copilot",
            "description": "Multi-agent autonomous chatbot for personal website using Python, LangChain, and Pinecone with RAG architecture.",
            "tech_stack": ["Python", "LangChain", "Pinecone", "Node.js", "FastAPI"],
            "metrics": {
                "user_engagement_increase": "30%",
                "query_response_time_reduction": "40%",
                "intent_recognition_accuracy": "95%"
            }
        }
    }
    project = projects.get(project_name.lower())
    if project:
        return json.dumps(project, indent=2)
    return f"No detailed information found for project: {project_name}. Known projects: Free Flow, AI Portfolio Copilot."


@tool
def search_skills(skill: str) -> str:
    """Search for information about specific technical skills. Input should be the skill name."""
    skills_db = {
        "python": "Proficient in Python for AI/ML, web development (Flask, Django), and automation",
        "java": "Extensive Java experience building enterprise Android applications at Cerence AI",
        "javascript": "Strong JavaScript/TypeScript skills with React.js, Angular, Node.js, Express.js",
        "kotlin": "Kotlin experience for modern Android development",
        "react": "Led front-end development using React.js at iConsult Collaborative for Yoga4Philly platform",
        "angular": "Used Angular for front-end development at iConsult Collaborative",
        "node.js": "Skilled in Node.js and Express.js for backend development and API creation",
        "firebase": "Engineered Firebase solutions improving real-time data retrieval by 35% at Cerence AI",
        "android": "Built enterprise Android applications at Cerence AI using Android Studio, Dagger, Retrofit",
        "blockchain": "Won ETHGlobal NY 2025 hackathon with Flow blockchain project (Free Flow)",
        "solidity": "Smart contract development experience with Solidity for blockchain projects",
        "aws": "Experience with AWS cloud services for scalable application deployment",
        "docker": "Docker experience for containerization and DevOps workflows",
        "langchain": "Built multi-agent AI systems using LangChain with RAG architecture",
        "socket.io": "Real-time multiplayer synchronization using Socket.io in Free Flow project",
        "sql": "Database management with PostgreSQL, MongoDB, and Firebase Realtime DB"
    }
    skill_info = skills_db.get(skill.lower())
    if skill_info:
        return skill_info
    return f"Atharva's full skill set includes: Python, Java, JavaScript, TypeScript, Kotlin, C++, React.js, Angular, Node.js, Flask, Django, AWS, Firebase, Docker, MongoDB, PostgreSQL, Android Studio, React Native, and more."


@tool
def get_contact_info() -> str:
    """Get Atharva's contact information and social media links."""
    return json.dumps({
        "name": "Atharva Gaikwad",
        "email": "atgaikwa@syr.edu",
        "linkedin": "https://www.linkedin.com/in/atharvagaikwad3/",
        "github": "https://github.com/atharvagaikwad03",
        "portfolio": "https://atharvagaikwad03.github.io"
    }, indent=2)


@tool
def get_experience_info(company: str = "") -> str:
    """Get Atharva's work experience. Optionally filter by company name."""
    experience = [
        {
            "company": "iConsult Collaborative",
            "role": "Software Developer Engineer",
            "location": "Syracuse University",
            "duration": "Oct 2024 - Jul 2025",
            "highlights": [
                "Led front-end development for Yoga4Philly using React.js and Angular",
                "Translated Figma prototypes into production-ready interfaces with CI/CD",
                "Designed modular UI components achieving 25% improvement in responsiveness"
            ]
        },
        {
            "company": "Cerence AI",
            "role": "Software Engineer",
            "duration": "Jan 2023 - Jul 2024",
            "highlights": [
                "Enhanced app functionality by 20% using OkHttp, Dagger, and Retrofit",
                "Engineered Firebase and RoomDB solutions improving real-time data retrieval by 35%",
                "Applied MediaBrowserService cutting download times by 30%"
            ]
        },
        {
            "company": "Cerence AI",
            "role": "Software Engineer Intern",
            "duration": "May 2022 - Jan 2023",
            "highlights": [
                "Improved app stability, reducing issue resolution time by 15%",
                "Mobile app feature development with Roku BrightScript"
            ]
        }
    ]
    if company:
        filtered = [e for e in experience if company.lower() in e["company"].lower()]
        return json.dumps(filtered, indent=2) if filtered else f"No experience found at {company}"
    return json.dumps(experience, indent=2)


@tool
def get_education_info() -> str:
    """Get Atharva's education background."""
    return json.dumps([
        {
            "degree": "M.S. Computer Science",
            "institution": "Syracuse University",
            "location": "Syracuse, New York",
            "graduation": "Expected May 2026",
            "gpa": "3.7/4.0",
            "coursework": ["Computer Architecture", "Operating Systems", "Database Management", "Mobile App Programming", "Design & Analysis of Algorithms", "Natural Language Processing", "Internet of Things"]
        },
        {
            "degree": "B.Tech Information Technology",
            "institution": "University of Pune",
            "graduation": "May 2023",
            "gpa": "3.4/4.0",
            "coursework": ["Engineering Mathematics", "Cloud Computing", "Data Structures & Algorithms", "Web Development"]
        }
    ], indent=2)


@tool
def format_portfolio_summary() -> str:
    """Get a summary of Atharva's portfolio and experience."""
    return """Atharva Gaikwad - Software Engineer & Full-Stack Developer
- M.S. Computer Science at Syracuse University (GPA 3.7, Expected May 2026)
- 2+ years of experience, 10+ projects built, 1 hackathon prize
- Software Developer Engineer at iConsult Collaborative (Syracuse University)
- Former Software Engineer at Cerence AI (1.5+ years)
- ETHGlobal New York 2025 Hackathon Winner (Free Flow - Flow blockchain)
- Skills: Python, Java, JavaScript, React.js, Angular, Node.js, Firebase, Android, Blockchain
- Specializes in mobile development, web applications, and blockchain solutions
- Portfolio: atharvagaikwad03.github.io
- Email: atgaikwa@syr.edu"""


portfolio_tools = [get_project_info, search_skills, get_contact_info, get_experience_info, get_education_info, format_portfolio_summary]
