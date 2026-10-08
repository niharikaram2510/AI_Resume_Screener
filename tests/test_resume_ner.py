from preprocessing.text_extraction import extract_text
from preprocessing.text_cleaning import clean_text

from models.resume_ner import extract_resume_entities
from models.resume_ner import extract_skills


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
# Transformer NER
# -----------------------------

entities = extract_resume_entities(
    resume_text
)


skills = extract_skills(
    resume_text
)


# -----------------------------
# Display Entities
# -----------------------------

print("\n==============================================")
print("          RESUME TRANSFORMER NER")
print("==============================================")


print("\nDetected Entities:\n")

for entity in entities:

    print(
        entity["entity_group"],
        "→",
        entity["word"],
        "| Score:",
        round(entity["score"], 3)
    )


# -----------------------------
# Display Skills
# -----------------------------

print("\n==============================================")
print("          DETECTED SKILLS")
print("==============================================")

for skill in skills:

    print("•", skill)


print("\n==============================================")