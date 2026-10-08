from preprocessing.text_extraction import extract_text
from preprocessing.text_cleaning import clean_text
from preprocessing.section_extraction import extract_sections
from preprocessing.data_loader import get_required_skills

from matching.resume_skill_matcher import (
    match_resume_to_role
)

from scoring.score_calculator import (
    detect_career_stage,
    calculate_section_scores,
    calculate_overall_score,
    get_experience_label
)


# -----------------------------
# Load Resume
# -----------------------------

file_path = "data/resumes/sample_resume.pdf"

with open(file_path, "rb") as file:

    resume_text = extract_text(file)

resume_text = clean_text(
    resume_text
)


# -----------------------------
# Job Role
# -----------------------------

job_role = "Machine Learning Engineer"


# -----------------------------
# Sections
# -----------------------------

sections = extract_sections(
    resume_text
)


# -----------------------------
# Career Stage
# -----------------------------

career_stage = detect_career_stage(
    sections
)


# -----------------------------
# Skill Matching
# -----------------------------

skill_result = match_resume_to_role(
    resume_text,
    job_role
)

skill_score = skill_result[
    "skill_score"
]


# -----------------------------
# Required Skills
# -----------------------------

required_skills = get_required_skills(
    job_role
)


# -----------------------------
# Section Scores
# -----------------------------

section_scores = calculate_section_scores(
    resume_text,
    required_skills,
    job_role
)


# -----------------------------
# Overall Score
# -----------------------------

overall_score = calculate_overall_score(
    skill_score,
    section_scores["experience"],
    section_scores["projects"],
    section_scores["education"],
    section_scores["certifications"],
    career_stage
)


# -----------------------------
# Display
# -----------------------------

print("\n==============================================")
print("          ADAPTIVE RESUME SCORE")
print("==============================================")

print(
    "\nJob Role:",
    job_role
)

print(
    "Career Stage:",
    career_stage
)

print(
    "Experience Type:",
    get_experience_label(
        career_stage
    )
)

print("\n----------------------------------------------")

print(
    "Skill Match:",
    skill_score,
    "%"
)

print(
    "Experience:",
    section_scores["experience"],
    "%"
)

print(
    "Projects:",
    section_scores["projects"],
    "%"
)

print(
    "Education:",
    section_scores["education"],
    "%"
)

print(
    "Certifications:",
    section_scores["certifications"],
    "%"
)

print("\n----------------------------------------------")

print(
    "OVERALL SCORE:",
    overall_score,
    "%"
)

print("\n==============================================")