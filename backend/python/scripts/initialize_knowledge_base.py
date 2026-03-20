"""Script to initialize the knowledge base with Atharva's portfolio data."""
import json
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from langchain_core.documents import Document
from rag.retriever import retriever


def load_portfolio_data(filepath: str) -> dict:
    """Load portfolio data from JSON file."""
    with open(filepath, 'r') as f:
        return json.load(f)


def create_documents_from_portfolio(data: dict) -> list:
    """Create Document objects from portfolio data."""
    documents = []

    # About / summary
    documents.append(Document(
        page_content=f"""Name: {data['name']}
Title: {data['title']}
About: {data['about']}
Portfolio: {data.get('portfolio_url', '')}
Years of Experience: {data['stats']['years_experience']}
Projects Built: {data['stats']['projects_built']}
Hackathon Prizes: {data['stats']['hackathon_prizes']}""",
        metadata={"source": "portfolio", "type": "about", "name": data['name']}
    ))

    # Experience
    for exp in data.get("experience", []):
        highlights = "\n".join(f"- {h}" for h in exp.get("highlights", []))
        tech = ", ".join(exp.get("tech", []))
        documents.append(Document(
            page_content=f"""Company: {exp['company']}
Role: {exp['role']}
Duration: {exp['duration']}
Location: {exp.get('location', '')}
Highlights:
{highlights}
Technologies: {tech}""",
            metadata={"source": "portfolio", "type": "experience", "company": exp['company'], "role": exp['role']}
        ))

    # Skills
    for category, items in data.get("skills", {}).items():
        category_name = category.replace("_", " ").title()
        documents.append(Document(
            page_content=f"Skill Category: {category_name}\nSkills: {', '.join(items)}",
            metadata={"source": "portfolio", "type": "skills", "category": category_name}
        ))

    # Projects
    for project in data.get("projects", []):
        content = f"Project: {project['name']}\n"
        if "award" in project:
            content += f"Award: {project['award']}\n"
        content += f"Description: {project['description']}\n"
        if "features" in project:
            content += "Features:\n" + "\n".join(f"- {f}" for f in project["features"]) + "\n"
        if "tech_stack" in project:
            content += f"Tech Stack: {', '.join(project['tech_stack'])}\n"
        if "metrics" in project:
            content += "Metrics:\n" + "\n".join(f"- {k}: {v}" for k, v in project["metrics"].items()) + "\n"
        if "links" in project:
            content += "Links:\n" + "\n".join(f"- {k}: {v}" for k, v in project["links"].items()) + "\n"

        documents.append(Document(
            page_content=content,
            metadata={"source": "portfolio", "type": "project", "name": project['name']}
        ))

    # Education
    for edu in data.get("education", []):
        coursework = ", ".join(edu.get("coursework", []))
        documents.append(Document(
            page_content=f"""Degree: {edu['degree']}
Institution: {edu['institution']}
Location: {edu.get('location', '')}
Graduation: {edu['graduation']}
GPA: {edu['gpa']}
Coursework: {coursework}""",
            metadata={"source": "portfolio", "type": "education", "institution": edu['institution']}
        ))

    # Contact
    contact = data.get("contact", {})
    documents.append(Document(
        page_content=f"""Contact Information for {data['name']}:
Email: {contact.get('email', '')}
Phone: {contact.get('phone', '')}
Address: {contact.get('address', '')}
Visa Status: {contact.get('visa_status', '')}
Sponsorship: {contact.get('sponsorship', '')}
LinkedIn: {contact.get('linkedin', '')}
GitHub: {contact.get('github', '')}
Portfolio: {contact.get('portfolio', '')}""",
        metadata={"source": "portfolio", "type": "contact"}
    ))

    return documents


def main():
    """Initialize knowledge base."""
    print("Initializing knowledge base with Atharva's portfolio data...")

    data_dir = Path(__file__).parent.parent.parent.parent / "data"
    data_file = data_dir / "sample_portfolio_data.json"

    if not data_file.exists():
        print(f"Error: Data file not found at {data_file}")
        return

    portfolio_data = load_portfolio_data(str(data_file))
    print(f"Loaded portfolio data for: {portfolio_data.get('name', 'Unknown')}")

    documents = create_documents_from_portfolio(portfolio_data)
    print(f"Created {len(documents)} documents")

    num_chunks = retriever.process_and_store_documents(documents)
    print(f"Stored {num_chunks} chunks in vector database")

    try:
        stats = retriever.vector_store.get_stats()
        print(f"\nVector store stats:")
        print(f"  Total vectors: {stats['total_vectors']}")
    except Exception:
        pass

    print("\nKnowledge base initialized successfully!")


if __name__ == "__main__":
    main()
