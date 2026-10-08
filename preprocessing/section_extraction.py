import re


SECTION_NAMES = {
    "summary": [
        "professional summary",
        "summary",
        "profile",
        "objective",
        "career objective"
    ],

    "skills": [
        "technical skills",
        "skills",
        "technical expertise",
        "core skills"
    ],

    "experience": [
        "experience",
        "work experience",
        "professional experience",
        "internship",
        "internships"
    ],

    "projects": [
        "projects",
        "academic projects",
        "personal projects",
        "project experience"
    ],

    "education": [
        "education",
        "academic background",
        "educational background"
    ],

    "certifications": [
        "certifications",
        "certificates",
        "certification"
    ]
}


def normalize_heading(text):
    """Normalize a possible section heading."""

    text = text.lower().strip()

    text = re.sub(
        r"[^a-z\s]",
        "",
        text
    )

    text = re.sub(
        r"\s+",
        " ",
        text
    )

    return text


def identify_section(line):
    """Identify a resume section heading."""

    normalized = normalize_heading(line)

    for section, headings in SECTION_NAMES.items():

        if normalized in headings:
            return section

    return None


def clean_section_line(line):
    """
    Clean an individual resume line
    while preserving the line boundary.
    """

    line = re.sub(
        r"[ \t]+",
        " ",
        line
    )

    line = re.sub(
        r"\s+([,.;:])",
        r"\1",
        line
    )

    return line.strip()


def extract_sections(text):
    """
    Split resume text into logical sections
    while preserving individual evidence lines.
    """

    sections = {}

    current_section = "other"
    sections[current_section] = []

    for line in text.split("\n"):

        line = clean_section_line(line)

        if not line:
            continue

        section = identify_section(line)

        if section:

            current_section = section

            if current_section not in sections:
                sections[current_section] = []

            continue

        sections[current_section].append(line)

    # Preserve individual lines instead of joining everything
    for section in sections:

        sections[section] = "\n".join(
            sections[section]
        )

    return sections