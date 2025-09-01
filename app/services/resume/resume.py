import re
import difflib
from typing import Dict, List, Union, Optional
from docx import Document
from docx.text.paragraph import Paragraph

# Canonical sections and their aliases
CANONICAL_SECTIONS = {
    "Summary": [
        "summary", "profile", "professional summary", "profile summary",
        "objective", "about me", "career summary"
    ],
    "Skills": [
        "skills", "technical skills", "core competencies", "key skills",
        "technical expertise", "technologies", "tools", "tech stack"
    ],
    "Experience": [
        "experience", "professional experience", "work experience",
        "employment history", "career history", "internships"
    ],
    "Projects": [
        "projects", "personal projects", "academic projects", "relevant projects"
    ],
    "Education": [
        "education", "academic background", "academics", "qualifications"
    ],
    "Certifications": [
        "certifications", "licenses", "certificates", "courses", "training"
    ],
    "Achievements": [
        "achievements", "awards", "honors", "accomplishments"
    ],
    "Publications": [
        "publications", "research", "papers", "articles"
    ],
    "Volunteer": [
        "volunteer", "volunteer experience", "community service"
    ],
    "Links": [
        "links", "profiles", "online profiles", "social", "portfolio",
        "github", "linkedin", "website"
    ],
    "Contact": [
        "contact", "contact information", "details", "personal info"
    ],
}

# Prebuild alias → canonical map
ALL_ALIASES = {alias: canon
               for canon, aliases in CANONICAL_SECTIONS.items()
               for alias in aliases}

BULLET_PREFIX = re.compile(r"^(\u2022|•|-|–|—|\*|\u00B7|\>)\s+")

def _clean_line(s: str) -> str:
    s = s.strip()
    s = BULLET_PREFIX.sub("", s)
    return s.strip()

def _canonical_from_text(text: str) -> Optional[str]:
    """Map a heading text to a canonical section name using fuzzy matching."""
    base = text.strip().rstrip(":").lower()
    if not base:
        return None

    # Exact alias
    if base in ALL_ALIASES:
        return ALL_ALIASES[base]

    # Fuzzy match to aliases
    close = difflib.get_close_matches(base, ALL_ALIASES.keys(), n=1, cutoff=0.8)
    if close:
        return ALL_ALIASES[close[0]]

    # Fuzzy match to canonical section names
    close_canon = difflib.get_close_matches(base, [c.lower() for c in CANONICAL_SECTIONS.keys()],
                                            n=1, cutoff=0.8)
    if close_canon:
        return close_canon[0].title()

    return None

def parse_resume_docx(file) -> Dict[str, Union[str, List[str]]]:
    """
    Parse a DOCX resume into JSON.
    Only canonical sections are returned; unmatched content goes to 'Other'.
    """
    doc = Document(file)

    # Initialize result with canonical buckets
    result: Dict[str, Union[str, List[str]]] = {
        "Summary": "",
        "Skills": [],
        "Experience": [],
        "Projects": [],
        "Education": [],
        "Certifications": [],
        "Achievements": [],
        "Publications": [],
        "Volunteer": [],
        "Links": [],
        "Contact": [],
        "Other": []
    }

    current_section: Optional[str] = None

    for para in doc.paragraphs:
        text = (para.text or "").strip()
        if not text:
            continue

        # Detect heading
        canon = _canonical_from_text(text)
        if canon:
            current_section = canon
            continue

        # Otherwise, content
        cleaned = _clean_line(text)
        if not cleaned:
            continue

        if not current_section:
            result["Other"].append(cleaned)
            continue

        if current_section == "Summary":
            result["Summary"] = (result["Summary"] + " " + cleaned).strip()
        elif current_section == "Skills":
            # Split by commas or semicolons
            skills = [s.strip() for s in re.split(r"[,;/]", cleaned) if s.strip()]
            result["Skills"].extend(skills)
        else:
            result[current_section].append(cleaned)

    # Deduplicate skills
    seen = set()
    unique_skills = []
    for s in result["Skills"]:
        key = s.lower()
        if key not in seen:
            seen.add(key)
            unique_skills.append(s)
    result["Skills"] = unique_skills

    return result
