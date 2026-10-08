from preprocessing.text_extraction import extract_text
from preprocessing.text_cleaning import clean_text

from matching.resume_skill_matcher import (
    match_resume_to_role
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
# Match Resume
# -----------------------------

result = match_resume_to_role(
    resume_text,
    job_role
)


# -----------------------------
# Display
# -----------------------------

print("\n==============================================")
print("          RESUME SKILL MATCHING")
print("==============================================")


print("\nJob Role:")
print(result["job_role"])


print("\nDetected Skills:")

for skill in result["detected_skills"]:

    print("•", skill)


print("\n----------------------------------------------")

print("\nMatched Skills:")

for item in result["matched_skills"]:

    print(
        f"✓ {item['skill']} "
        f"({item['importance']})"
    )


print("\n----------------------------------------------")

print("\nMissing Skills:")

for item in result["missing_skills"]:

    print(
        f"✗ {item['skill']} "
        f"({item['importance']})"
    )


print("\n----------------------------------------------")

print(
    "\nWeighted Skill Score:",
    result["skill_score"],
    "%"
)


print("\n==============================================")