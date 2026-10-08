from models.embedding_model import model
from preprocessing.section_extraction import extract_sections


# -----------------------------------------
# Career-stage scoring weights
# -----------------------------------------

def calculate_career_stage_weights(career_stage):

    if career_stage == "Experienced":
        return {
            "skills": 0.40,
            "experience": 0.25,
            "projects": 0.15,
            "education": 0.10,
            "certifications": 0.10
        }

    if career_stage == "Early Career / Fresher":
        return {
            "skills": 0.45,
            "experience": 0.20,
            "projects": 0.20,
            "education": 0.10,
            "certifications": 0.05
        }

    return {
        "skills": 0.50,
        "experience": 0.00,
        "projects": 0.25,
        "education": 0.15,
        "certifications": 0.10
    }


# -----------------------------------------
# Career-stage detection
# -----------------------------------------

def detect_career_stage(sections):

    experience = sections.get(
        "experience",
        ""
    ).lower()

    internship_terms = [
        "intern",
        "internship",
        "trainee",
        "apprentice"
    ]

    professional_terms = [
        "software engineer",
        "machine learning engineer",
        "data scientist",
        "data analyst",
        "developer",
        "engineer",
        "manager",
        "professional experience",
        "work experience"
    ]

    has_internship = any(
        term in experience
        for term in internship_terms
    )

    has_professional_experience = any(
        term in experience
        for term in professional_terms
    )

    if has_professional_experience and not has_internship:
        return "Experienced"

    if has_internship:
        return "Early Career / Fresher"

    return "Fresher"


# -----------------------------------------
# Basic keyword section score
# -----------------------------------------

def section_score(
    section_text,
    required_terms
):

    if not section_text:
        return 0

    if not required_terms:
        return 100

    text = section_text.lower()

    matched = sum(
        1
        for term in required_terms
        if term.lower() in text
    )

    return round(
        (matched / len(required_terms)) * 100,
        2
    )


# -----------------------------------------
# Semantic skill relevance
# -----------------------------------------

def semantic_skill_relevance(
    section_text,
    required_skills
):
    """
    Uses MiniLM to measure how relevant
    the resume section is to the required
    skills of the selected job role.
    """

    if not section_text:
        return 0

    if not required_skills:
        return 0

    section_embedding = model.encode(
        section_text
    )

    skill_embeddings = model.encode(
        required_skills
    )

    scores = []

    for skill_embedding in skill_embeddings:

        similarity = (
            section_embedding @ skill_embedding
        )

        similarity = max(
            0,
            min(
                1,
                float(similarity)
            )
        )

        scores.append(similarity)

    if not scores:
        return 0

    # Average relevance to required skills
    score = (
        sum(scores) / len(scores)
    ) * 100

    return round(
        score,
        2
    )


# -----------------------------------------
# Combined section relevance
# -----------------------------------------

def calculate_section_relevance(
    section_text,
    required_skills
):
    """
    Combines:
    1. Exact skill evidence
    2. Transformer semantic relevance
    """

    if not section_text:
        return 0

    # Exact skill evidence
    keyword_score = section_score(
        section_text,
        required_skills
    )

    # Transformer semantic evidence
    semantic_score = semantic_skill_relevance(
        section_text,
        required_skills
    )

    # Hybrid score
    score = (
        keyword_score * 0.60
        +
        semantic_score * 0.40
    )

    return round(
        score,
        2
    )


# -----------------------------------------
# Calculate all section scores
# -----------------------------------------

def calculate_section_scores(
    resume_text,
    required_skills,
    job_role
):

    sections = extract_sections(
        resume_text
    )

    # Experience relevance
    experience_score = calculate_section_relevance(
        sections.get(
            "experience",
            ""
        ),
        required_skills
    )

    # Project relevance
    project_score = calculate_section_relevance(
        sections.get(
            "projects",
            ""
        ),
        required_skills
    )

    # Education
    education_text = sections.get(
        "education",
        ""
    )

    education_score = (
        100
        if education_text
        else 0
    )

    # Certifications
    certification_text = sections.get(
        "certifications",
        ""
    )

    certification_score = (
        100
        if certification_text
        else 0
    )

    return {
        "experience": experience_score,
        "projects": project_score,
        "education": education_score,
        "certifications": certification_score
    }


# -----------------------------------------
# Overall score
# -----------------------------------------

def calculate_overall_score(
    skill_score,
    experience_score,
    project_score,
    education_score,
    certification_score,
    career_stage
):

    scores = {
        "skills": skill_score,
        "experience": experience_score,
        "projects": project_score,
        "education": education_score,
        "certifications": certification_score
    }

    weights = calculate_career_stage_weights(
        career_stage
    )

    total = 0

    for section in scores:

        total += (
            scores[section]
            * weights[section]
        )

    return round(
        total,
        2
    )


# -----------------------------------------
# Experience display label
# -----------------------------------------

def get_experience_label(
    career_stage
):

    labels = {

        "Experienced":
            "Professional Experience",

        "Early Career / Fresher":
            "Internships & Early Career Experience",

        "Fresher":
            "Academic & Project Experience"
    }

    return labels.get(
        career_stage,
        "Experience"
    )